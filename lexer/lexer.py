from unittest import result
from automata import automata_union, nfa_to_dfa, DFA
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
            # print('regex', regex)
            # print('here')
            ast = self.parser.get_ast(tokenized_regex)
            # print('aki')
            # print('ast', ast)
            nfa = ast.evaluate()
            print('finales nfa', nfa.finals)
            for x in nfa.finals:
                nfa.tags[x] = (token_type, n)
            print(f'{n} nfa , {nfa.transitions}')
            regexs.append((token_type, nfa))
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
    
    def _build_automaton(self) -> DFA:
        nfa = self.regexs[0][1]
        for i in range(1, len(self.regexs)):
            # print('akiiiii')
            nfa = automata_union(nfa, self.regexs[i][1])
        
        result = nfa_to_dfa(nfa)
        print('pase')
        # print('nfa before dfa, ', nfa.transitions)
        print('final dfa, ', result.transitions)
        test = result.transitions[0]['h']
        print('dfa tansitions', test)
        print(result.transitions[test[0]])
        return nfa_to_dfa(nfa)
    
    def _walk(self, string):
        # print('automaton', self.automaton.transitions)
        print('string to matche, ', string)
        # print('test', self.automaton.recognize('let'))
        print('rec', self.automaton.recognize(string))
        _, last_idx_matched, last_state = self.automaton.recognize(string)
        if last_state in self.automaton.finals:
            matched_lex = string[0:last_idx_matched]
            token_type = self.target_grammar[matched_lex]
            print()
            print('matched', matched_lex)
            print('last', last_idx_matched)
            print('token', token_type)
            print()
            return last_idx_matched-1, matched_lex, token_type
        
        self.errors.append(f'Error recognizing token at position {last_idx_matched} in string: {string}')
        return last_idx_matched, None, None
    
    def _tokenize(self, text: str):
        iterations = 0
        text = text.replace(' ', '')
        text = text.replace('\n', '')
        last_idx_matched, lex, token_type = self._walk(text)
        while last_idx_matched != len(text)-1:
            if lex is not None:
                yield lex, token_type

            next_idx_to_start = last_idx_matched+1
            text = text[next_idx_to_start:]
            last_idx_matched, lex, token_type = self._walk(text)
            iterations+=1
            # print('last, ', last_idx_matched)
            if iterations == 20:
                break
        yield '$', self.eof
    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]

