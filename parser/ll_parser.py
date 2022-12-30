

from typing import Callable, Iterable, Iterator
from grammar import AttributeProduction, Grammar, Sentence, Symbol, NonTerminal, Terminal, Production, EOF
from lex_token import Token
from utils import ContainerSet


class LLParser:
    def __init__(self, grammar: Grammar) -> None:
        self.grammar = grammar
        self.parser: Callable[[list[Terminal]], list[Production]] = self.build_parser(grammar)


    def build_parser(self, grammar: Grammar):
        firsts = self.compute_firsts(grammar)
        follows = self.compute_follows(grammar, firsts)
        parsing_table = self.build_parsing_table(grammar, firsts, follows)
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
                        production = parsing_table[top, a][0]
                    except KeyError:
                        raise Exception("No se puede reconocer la cadena")
                    
                    output+=[production]
                    for symbol in reversed(production.Right):
                        stack.append(symbol)
                        
                if len(stack)==0:
                    break

            # left parse is ready!!!
            return output
        
        return parser

    def get_ast(self, tokens: list[Token]):
        terminals = [t.token_type for t in tokens]
        left_parse = iter(self.parser(terminals))
        tokens_iter = iter(tokens)
        result = self.__build_ast(next(left_parse), left_parse, tokens_iter)
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
                    return P(inherited,synteticed) if P is not None else None

    # Computes First(alpha), given First(Vt) and First(Vn) 
    # alpha in (Vt U Vn)*
    def compute_local_first(self, firsts, alpha: Sentence):
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
    def compute_firsts(self, G: Grammar):
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
                local_first = self.compute_local_first(firsts, alpha)
                
                # update First(X) and First(alpha) from CurrentFirst(alpha)
                change |= first_alpha.hard_update(local_first)
                change |= first_X.hard_update(local_first)
                        
        # First(Vt) + First(Vt) + First(RightSides)
        return firsts

    def compute_follows(self, G: Grammar, firsts: dict[Symbol | Sentence, ContainerSet]):
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

