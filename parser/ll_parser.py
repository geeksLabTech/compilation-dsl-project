
from typing import Callable, Iterable, Iterator
from grammar import AttributeProduction, Grammar, Sentence, Symbol, NonTerminal, Terminal, Production, EOF
from lexer.lex_token import Token
from parser.utils import ContainerSet, compute_firsts, compute_follows, compute_local_first


class LLParser:
    def __init__(self, grammar: Grammar) -> None:
        self.grammar = grammar
        self.parser: Callable[[list[Terminal]], list[Production]] = self.build_parser(grammar)

    def build_parser(self, grammar: Grammar):
        firsts = compute_firsts(grammar)
        follows = compute_follows(grammar, firsts)
        parsing_table = self.build_parsing_table(grammar, firsts, follows)
        # print('parsing table ', parsing_table)
        def parser(w: list[Terminal]) -> list[Production]:
            assert grammar.startSymbol is not None, 'Start symbol cannot be None'
            stack: list[NonTerminal|Terminal] = [grammar.startSymbol]
            cursor = 0
            output: list[Production] = []
            # parsing w...
            while True:
                top = stack.pop()
                assert top is not None, 'Stack is empty'
                a = w[cursor]
                
                if top == a:
                    cursor += 1
                elif top.IsNonTerminal:
                    try:
                        # print('top, a', top, a)
                        production = parsing_table[top, a][0]
                    except KeyError:
                        raise Exception("No se puede reconocer la cadena")
                    
                    output+=[production]
                    # print('production', production)
                    for symbol in reversed(production.Right):
                        stack.append(symbol)
                        
                if len(stack)==0:
                    break

            # left parse is ready!!!
            return output
        
        return parser

    def get_ast(self, tokens: list[Token]):
        terminals = [t.token_type for t in tokens]
        print('tokens', tokens)
        print('left_parse')
        x = self.parser(terminals)
        for y in x:
            print(y)
        print('done')
        left_parse = iter(self.parser(terminals))
        tokens_iter = iter(tokens)
        result = self.__build_ast(next(left_parse), left_parse, tokens_iter)
        # print('last_token', next(tokens_iter))
        assert isinstance(next(tokens_iter).token_type, EOF)
        return result

    def __build_ast(self, production: AttributeProduction, left_parse, tokens, inherited_value=None):
        head, body=production
        attributes=production.attributes
        synteticed=[None]*(len(body)+1)
        inherited=[None]*(len(body)+1)
        inherited[0]=inherited_value
        for i,symbol in enumerate(body,1):
            if symbol.IsTerminal:
                assert inherited[i]is None
                synteticed[i]=next(tokens).lex
            else:
                next_production=next(left_parse)
                assert symbol==next_production.Left
                P=attributes[i]
                if P is not None:
                    inherited[i]=P(inherited,synteticed)
                synteticed[i]=self.__build_ast(next_production,left_parse,tokens,inherited[i])
                
        
        P=attributes[0]
        if P is not None and P(inherited,synteticed) is None:
            print('mirala')
            print(production)
            print('infraganti')
        print('Node build', P(inherited,synteticed) if P is not None else None)
        return P(inherited,synteticed) if P is not None else None

    def build_parsing_table(self, G: Grammar, firsts: dict[Symbol | Sentence, ContainerSet], follows: dict[Symbol | Sentence, ContainerSet]):
        # init parsing table
        M: dict[tuple[NonTerminal, Terminal], list[Production]] = {}
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            firsts_X = firsts[X]
            
            if alpha.IsEpsilon:
                follows_X = follows[X]
                for f in follows_X:
                    try:
                        value = M[X,f]
                    except KeyError:
                        M[X,f] = []
                    M[X, f].append(production)
                    
            else:
                for f in firsts[alpha]:
                    if f.IsEpsilon: continue
                        
                    try:
                        value = M[X,f]
                    except KeyError:
                        M[X,f] = []
                        
                    if alpha[0].IsTerminal and alpha[0] == f:
                        M[X, f].append(production)
                        break
                    if alpha[0].IsNonTerminal:
                        M[X, f].append(production)
        
        # parsing table is ready!!!
        return M     

