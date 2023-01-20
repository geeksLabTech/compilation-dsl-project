

from grammar import Grammar, Item
from parser.utils import compute_firsts, compute_local_first, ContainerSet
from automata import State
from parser.slr_parser import ShiftReduceParser


def expand(item: Item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []
    
    lookaheads = ContainerSet()

    for x in item.Preview():
        lookaheads.update(compute_local_first(firsts, x))
        
    assert not lookaheads.contains_epsilon
    productions = next_symbol.productions
    return [Item(production, 0, lookaheads) for production in productions]
    


def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)
    
    return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }

def closure_lr1(items, firsts):
    closure = ContainerSet(*items)
    
    changed = True
    while changed:
        changed = False
        
        new_items = ContainerSet()
        
        for x in closure:
            expanded=expand(x, firsts)
            new_items.update(ContainerSet(*expanded))
                    
        changed = closure.update(new_items)
        
    return compress(closure)

def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)

def build_LR1_automaton(G: Grammar):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    
    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])
    
    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)
    pending = [ start ]
    visited = { start: automaton }
    
    while pending:
        current = pending.pop()
        
        current_state = visited[current]
                
        new_closure = closure_lr1(current_state.state, firsts)
        for new_item in new_closure:
            for symbol in G.terminals + G.nonTerminals:
                next_state = None
                if symbol.Name in current_state.transitions:
                    continue
                if new_item.NextSymbol == symbol:
                    next_state = goto_lr1(new_closure, symbol, firsts=firsts)
                    if next_state:
                        frozen = frozenset(next_state)
                        if not frozen in visited:
                            pending.append(frozen)
                            new_state = State(frozen, True)
                            visited[frozen] = new_state
                            current_state.add_transition(symbol.Name, new_state)
                        else:
                            current_state.add_transition(symbol.Name, visited[frozen])
                    
    return automaton

class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i
        
        for node in automaton:
            idx = node.idx
            for item in node.state: 
                if  item.NextSymbol and item.NextSymbol.IsTerminal:
                    if node.has_transition(item.NextSymbol.Name):
                        self._register(self.action, (idx, item.NextSymbol), (self.SHIFT,node.get(item.NextSymbol.Name).idx))
                    
                elif item.IsReduceItem and item.production.Left == G.startSymbol and not item.NextSymbol:
                    self._register(self.action, (idx, G.EOF), self.OK)

                elif not item.NextSymbol and not item.production.Left == G.startSymbol:
                    for lookahead in item.lookaheads:
                        self._register(self.action, (idx, lookahead), (self.REDUCE, item.production))
                
                elif item.NextSymbol and item.NextSymbol.IsNonTerminal:
                    if node.has_transition(item.NextSymbol.Name):
                        self._register(self.goto, (idx, item.NextSymbol), node.get(item.NextSymbol.Name).idx)
                    
        # print('action', self.action)
        # print('goto', self.goto)
        
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value