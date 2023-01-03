from typing import Self

from grammar import Grammar, Sentence, Symbol


class ContainerSet:
    def __init__(self, *values, contains_epsilon=False):
        self.set = set(values)
        self.contains_epsilon = contains_epsilon

    def add(self, value):
        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)

    def extend(self, values):
        change = False
        for value in values:
            change |= self.add(value)
        return change

    def set_epsilon(self, value=True):
        last = self.contains_epsilon
        self.contains_epsilon = value
        return last != self.contains_epsilon

    def update(self, other: Self):
        n = len(self.set)
        self.set.update(other.set)
        return n != len(self.set)

    def epsilon_update(self, other: Self):
        return self.set_epsilon(self.contains_epsilon | other.contains_epsilon)

    def hard_update(self, other: Self):
        return self.update(other) | self.epsilon_update(other)

    def find_match(self, match):
        for item in self.set:
            if item == match:
                return item
        return None

    def __len__(self):
        return len(self.set) + int(self.contains_epsilon)

    def __str__(self):
        return '%s-%s' % (str(self.set), self.contains_epsilon)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.set)

    def __nonzero__(self):
        return len(self) > 0

    def __eq__(self, other: Self):
        if isinstance(other, set):
            return self.set == other
        return isinstance(other, ContainerSet) and self.set == other.set and self.contains_epsilon == other.contains_epsilon
    
    # Computes First(alpha), given First(Vt) and First(Vn) 
    # alpha in (Vt U Vn)*
def compute_local_first(firsts, alpha: Sentence):
    first_alpha = ContainerSet()
        
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False
        
    if alpha_is_epsilon:
        first_alpha.set_epsilon()

    else:
        for i, x in enumerate(alpha):
            if first_alpha.contains_epsilon:
                first_alpha.set_epsilon(False)
            if x.IsTerminal:
                first_alpha.update(ContainerSet(x))
                break
            else:
                first_alpha.hard_update(firsts[alpha[i]])
                if not first_alpha.contains_epsilon:
                    break
        
    # alpha = X1 ... XN
    # First(Xi) subconjunto First(alpha)
    # epsilon pertenece a First(X1)...First(Xi) ? First(Xi+1) subconjunto de First(X) y First(alpha)
    # epsilon pertenece a First(X1)...First(XN) ? epsilon pertence a First(X) y al First(alpha)
        
    return first_alpha

    # Computes First(Vt) U First(Vn) U First(alpha)
    # P: X -> alpha
def compute_firsts(G: Grammar):
    firsts: dict[Symbol | Sentence, ContainerSet] = {}
    change = True
        
    # init First(Vt)
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
            
    # init First(Vn)
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
        
    while change:
        change = False
            
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
                
            # get current First(X)
            first_X = firsts[X]
                    
            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
                
            # CurrentFirst(alpha)???
            local_first = compute_local_first(firsts, alpha)
                
            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                        
    # First(Vt) + First(Vt) + First(RightSides)
    return firsts

def compute_follows(G: Grammar, firsts: dict[Symbol | Sentence, ContainerSet]):
    follows: dict[Symbol|Sentence, ContainerSet] = { }
    change = True
        
    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
        
    assert G.startSymbol is not None, 'Grammar has no start symbol'

    follows[G.startSymbol] = ContainerSet(G.EOF)
        
    while change:
        change = False
            
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
                
            follow_X = follows[X]
                
            # X -> zeta Y beta
            # First(beta) - { epsilon } subset of Follow(Y)
            # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
            if alpha.IsEpsilon:
                continue

            for i, symbol in enumerate(alpha):
                if(symbol.IsTerminal): 
                    continue
                if(symbol.IsNonTerminal):
                    if( i + 1 < len(alpha)):
                        next_symbol = alpha[i+1]          
                        local_first = firsts[next_symbol]
                        change |= follows[symbol].update(local_first)
                        if local_first.contains_epsilon:
                            change |= follows[symbol].update(follow_X)
                        
                    else:
                        follows[alpha[-1]] = follow_X

    # Follow(Vn)
    return follows