from unittest import result
from automata import automata_union, nfa_to_dfa, DFA,State, state_union
from grammar import Grammar, EOF, Terminal
from lexer.lex_token import Token, UnknownToken
from lexer.regex_grammar import REGEX_GRAMMAR
from parser.ll_parser import LLParser


class Lexer:
    def __init__(self, table: list[tuple[Terminal, str]], target_grammar: Grammar, eof):
        self.eof = eof
        self.target_grammar = target_grammar
        self.fixed_tokens = {lex: Token(lex, REGEX_GRAMMAR[lex]) for lex in r'| \ { } . ( ) [ ] ^ - , ? * + ε 0 1 2 3 4 5 6 7 8 9'.split() }
        self.parser = LLParser(REGEX_GRAMMAR)
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
        self.errors = []
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            # - Remember to tag the final states with the token_type and priority.
            # - <State>.tag might be useful for that purpose ;-)
            # print('checkeo del token type', type(token_type))
            tokenized_regex = self.__tokenize_regex(regex, REGEX_GRAMMAR)
            
            ast = self.parser.get_ast(tokenized_regex)

            nfa = ast.evaluate()
            state = State.from_nfa(nfa, (token_type, n))
            # print('finales nfa', nfa.finals)
            # for x in nfa.finals:
            #     nfa.tags[x] = (token_type, n)
            # print(f'{n} nfa , {nfa.transitions}')
            regexs.append((token_type, state))
        return regexs

    def __tokenize_regex(self, text, G, skip_whitespaces=True):
        tokens = []
        if len(text) == 1:
            tokens.append(Token(text, G['any_char']))
        else:
            for char in text:
                if skip_whitespaces and char.isspace():
                    continue
                if char in self.fixed_tokens:
                    tokens.append(self.fixed_tokens[char])
                else:
                    tokens.append(Token(char, G['any_char']))
            
        tokens.append(Token('$', G.EOF))
        return tokens
    
    def _build_automaton(self):
        state = self.regexs[0][1]
        for i in range(1, len(self.regexs)):
            # print('akiiiii')
            state = state_union(state, self.regexs[i][1])
        
        # state = State.from_nfa(nfa)
        print('LA verdadera', state.recognize('he'))
        result = state.to_deterministic()
        # test = result.transitions[0]['h']
        return result
    
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''
        last_idx_matched = 0
        print('transition:',self.automaton.transitions)
        print('estado inicial:' ,state.state)
        print('prueba', self.automaton.recognize('he'))
        print('string_to match ', string)
        for i, symbol in enumerate(string):
            if symbol in state.transitions:
                state = state.get(symbol)
                lex += symbol
                # last_idx_matched = i
                print('state', state)
                if state.final:
                    print('matched', lex)
                    last_idx_matched = i
                    final = state
                    final_lex = lex
            
        return final, final_lex, last_idx_matched
        # # print('automaton', self.automaton.transitions)
        # print('string to matche, ', string)
        # # print('test', self.automaton.recognize('let'))
        # print('rec', self.automaton.recognize(string))
        # _, last_idx_matched, last_state = self.automaton.recognize(string)
        # if last_state in self.automaton.finals:
        #     matched_lex = string[0:last_idx_matched]
        #     token_type = self.target_grammar[matched_lex]
        #     print()
        #     print('matched', matched_lex)
        #     print('last', last_idx_matched)
        #     print('token', token_type)
        #     print()
        #     return last_idx_matched-1, matched_lex, token_type
        
        # self.errors.append(f'Error recognizing token at position {last_idx_matched} in string: {string}')
        # return last_idx_matched, None, None
        
    
    def _tokenize(self, text: str):
        iterations = 0
        text = text.replace(' ', '')
        text = text.replace('\n', '')
        while len(text)>0:
            state, lex, idx = self._walk(text)
            if state is not None:
                token_type = state.tag[0]
                text = text[idx+1:]
                yield lex, token_type
            else:
                text = text[1:]
            iterations+=1
            if iterations == 20:
                break
        yield '$', self.eof
    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]

