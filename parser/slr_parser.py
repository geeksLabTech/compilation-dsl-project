from parser.utils import compute_firsts, compute_follows, compute_local_first
from grammar import Grammar, Sentence, Symbol, Item, EOF
from automata import State


class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w, get_shift_reduce=False):
        stack = [0]
        cursor = 0
        output = []
        operations = []
        while True:
            state = stack[-1]
            lookahead = w[cursor]

            if(state, lookahead) not in self.action:
                excepted_char = ''

                for (state1, i) in self.action.keys():
                    if i.IsTerminal and state1 == state:
                        excepted_char += str(i) + ' '
                parsed = ' '.join([str(m)
                                    for m in stack if not str(m).isnumeric()])
                message_error = f'It was expected "{excepted_char}" received "{lookahead}" after {parsed}'
                print("\nError. Aborting...")
                print('')
                print("\n", message_error)
                # print(w[cursor-1])
                return None

            if self.action[state, lookahead] == self.OK:
                action = self.OK
            else:
                action, tag = self.action[state, lookahead]
            # print('action, tsg', action)
            if action == self.SHIFT:
                operations.append(self.SHIFT)
                stack += [lookahead, tag]
                cursor += 1
            elif action == self.REDUCE:
                operations.append(self.REDUCE)
                output.append(tag)
                # print('tag', tag)
                head, body = tag
                for symbol in reversed(body):
                    # print('stack', stack)
                    stack.pop()

                    assert stack.pop() == symbol
                    state = stack[-1]
                    # print(self.goto,'goto')
                    # print('output', output)
                goto = self.goto[state, head]
                stack += [head, goto]
            elif action == self.OK:
                stack.pop()
                assert stack.pop() == self.G.startSymbol
                assert len(stack) == 1
                return output if not get_shift_reduce else(output, operations)
            else:
                raise Exception('Invalid action!!!')


class SLR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        automaton = self._build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i
        for i, production in enumerate(G.Productions, 1):
            production.j = i
        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state

                if len(item.production.Right) == item.pos:
                    # print('elif')
                    if item.production.Left == G.startSymbol:
                        self.action[node.idx, G.EOF] = self.OK
                    else:
                        for terminal_follow in follows[item.production.Left]:
                            tag = None
                            for production in G.Productions:
                                if production == item.production:
                                    tag = production
                            self.action[node.idx,
                                        terminal_follow] = self.REDUCE, tag

                elif item.production.Right[item.pos].IsTerminal:
                    next_node = node.get(item.NextSymbol.Name)
                    self.action[node.idx,
                                item.NextSymbol] = self.SHIFT, next_node.idx

                else:
                    next_node = node.get(item.NextSymbol.Name)
                    self.goto[node.idx, item.NextSymbol] = next_node.idx

    def _build_LR0_automaton(self, G):
        assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

        start_production = G.startSymbol.productions[0]
        start_item = Item(start_production, 0)

        automaton = State(start_item, True)

        pending = [start_item]
        visited = {start_item: automaton}

        while pending:

            current_item = pending.pop()
            if current_item.IsReduceItem:
                continue

            next_symbol = current_item.NextSymbol
            transitions = {}
            epsilon_transitions = set()

            if current_item.NextSymbol.IsNonTerminal:
                for prod in next_symbol.productions:
                    item = Item(prod, 0)
                    if item not in visited:
                        visited[item] = State(item, True)
                        pending.append(item)
                    # '' denota epsilon-transicion
                    epsilon_transitions.add(visited[item])

                next_item = current_item.NextItem()
                state = State(next_item, True)
                transitions[str(next_symbol)] = state
                if next_item not in visited:
                    visited[next_item] = state
                    pending.append(next_item)

            else:
                item = current_item.NextItem()
                state = State(item, True)
                if item not in visited:
                    visited[item] = state
                    pending.append(item)
                transitions[str(next_symbol)] = state

            for x in transitions:
                visited[current_item].add_transition(x, transitions[x])

            for x in epsilon_transitions:
                visited[current_item].epsilon_transitions.add(x)

        return automaton

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value


def build_slr_ast(right_parse, operations, tokens):
    if not right_parse or not operations or not tokens:
        return

    right_parse = iter(right_parse)
    tokens = iter(tokens)
    stack = []
    for operation in operations:
        if operation == ShiftReduceParser.SHIFT:
            token = next(tokens)
            stack.append(token)
        elif operation == ShiftReduceParser.REDUCE:
            production = next(right_parse)
            head, body = production
            attributes = production.attributes
            assert all(
                rule is None for rule in attributes[1:]), 'There must be only synteticed attributes.'
            rule = attributes[0]

            if len(body):
                synteticed = [None] + stack[-len(body):]
                value = rule(None, synteticed)
                stack[-len(body):] = [value]
            else:
                stack.append(rule(None, None))
        else:
            raise Exception('Invalid action!!!')

    assert len(stack) == 1
    last_token = next(tokens)
    # print(last_token)
    # print(next(last_token))
    assert isinstance(last_token.token_type, EOF)
    return stack[0]
