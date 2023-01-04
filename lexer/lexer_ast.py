from base_ast import AtomicNode,UnaryNode,BinaryNode
from automata import automata_closure,automata_concatenation,automata_union,NFA
from lexer.vocabulary_iter import VocabularyIter

EPSILON = 'ε'

class EpsilonNode(AtomicNode):
    def evaluate(self):
        nfa = NFA(states=2, finals=[1], transitions={
            (0,'ε'):[1]
        })    
        return nfa

# EpsilonNode(EPSILON).evaluate()

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        
        nfa = NFA(states=2, finals=[1], transitions={
            (0,s):[1]
        })
        return nfa

# SymbolNode('a').evaluate()

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value : NFA):
        nfa = automata_closure(value)
        return nfa
    
# ClosureNode(SymbolNode('a')).evaluate()

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        nfa = automata_union(lvalue,rvalue)
        return nfa

# UnionNode(SymbolNode('a'), SymbolNode('b')).evaluate()

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        nfa = automata_concatenation(lvalue,rvalue)

        return nfa

# ConcatNode(SymbolNode('a'), SymbolNode('b')).evaluate()

class IntervalNode(BinaryNode):
    def operate(self, lvalue , rvalue):
        # print('operate transitions', lvalue.transitions)
        # print('operate right transitions', rvalue.transitions)
        
        value_of_lchar : str = list(lvalue.transitions[0].keys())[0]
        value_of_rchar: str = list(rvalue.transitions[0].keys())[0]
        vocabularyIter = VocabularyIter(value_of_lchar)
        iterator = vocabularyIter.create_iter(vocabularyIter.vocabulary[value_of_lchar], vocabularyIter.vocabulary[value_of_rchar])
        nfa_list = []
        while True:
            try:
                value_of_char = iterator.next()
                nfa = NFA(states=2, finals=[1], transitions={
                (0,value_of_char):[1]
                })
                nfa_list.append(nfa)
            except StopIteration:
                break
        
        first_nfa = nfa_list[0]
        for nfa in nfa_list[1:]:
            first_nfa = automata_union(first_nfa, nfa)
        print()
        print('first_nfa', first_nfa.transitions)
        print()
        return first_nfa
            

class QuestionNode(UnaryNode):
    def operate(self, value):
        nfa = NFA(states= 2, finals=[0,1], transitions={
            (0,'ε'):[0],
            (0,value):[1],
            })
        return nfa

class PlusNode(UnaryNode):
    def operate(self, value):
        nfa = NFA(states=2,finals=[1],transitions={
            (0,value):[1],
            (1,value):[1],
            })
        return nfa