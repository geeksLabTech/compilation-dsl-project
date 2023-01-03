from automata import automata_union, nfa_to_dfa, DFA
from grammar import Grammar, EOF, Terminal
from lexer.lex_token import Token, UnknownToken
from lexer.regex_grammar import REGEX_GRAMMAR
from parser.ll_parser import LLParser

class Lexer:
    def __init__(self, table: list[tuple[Terminal, str]], eof):
        self.eof = eof
        self.fixed_tokens = {lex: Token(lex, REGEX_GRAMMAR[lex]) for lex in r'| \ { } . ( ) [ ] ^ - , ? * + ε _ 0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split() }
        self.parser = LLParser(REGEX_GRAMMAR)
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
        self.errors = []
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            # - Remember to tag the final states with the token_type and priority.
            # - <State>.tag might be useful for that purpose ;-)
            tokenized_regex = self.__tokenize_regex(regex, REGEX_GRAMMAR)
            tokenized_regex.append(Token('$', EOF(REGEX_GRAMMAR)))
            print('here')
            ast = self.parser.get_ast(tokenized_regex)
            print('aki')
            nfa = ast.evaluate()
            for x in nfa.finals:
                x.tag = (token_type, n)
            regexs.append((token_type, nfa))
        return regexs

    def __tokenize_regex(self, text, G, skip_whitespaces=True):
        tokens = []
        for char in text:
            if skip_whitespaces and char.isspace():
                continue
            if char in self.fixed_tokens:
                tokens.append(self.fixed_tokens[char])
            else:
                raise Exception(f'Malformed regular expression: {char}')
            
        tokens.append(Token('$', G.EOF))
        return tokens
    
    def _build_automaton(self) -> DFA:
        nfa = self.regexs[0][1]
        for i in range(1, len(self.regexs)+1):
            nfa = automata_union(nfa, self.regexs[i][1])
        
        return nfa_to_dfa(nfa)
    
    def _walk(self, string):
        _, last_idx_matched, last_state = self.automaton.recognize(string)
        if last_state in self.automaton.finals:
            token_type = self.automaton.tags[last_state][0]
            matched_lex = token_type.name
            return last_idx_matched, matched_lex, token_type
        
        self.errors.append(f'Error recognizing token at position {last_idx_matched} in string: {string}')
        return last_idx_matched, None, None
    
    def _tokenize(self, text):
        last_idx_matched, lex, token_type = self._walk(text)
        while last_idx_matched != len(text)-1:
            if lex is not None:
                yield lex, token_type

            next_idx_to_start = last_idx_matched + 1
            last_idx_matched, lex, token_type = self._walk(text[next_idx_to_start:])
                
        yield '$', self.eof
    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]

