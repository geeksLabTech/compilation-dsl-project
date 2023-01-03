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
        value_of_lchar : str = lvalue.transition[0][1]
        value_of_rchar: str = rvalue.transition[0][1]
        vocabularyIter = VocabularyIter(value_of_lchar)
        iterator = vocabularyIter.create_iter(vocabularyIter.vocabulary[value_of_lchar], vocabularyIter.vocabulary[value_of_rchar])
        automon_result = UnionNode(lvalue,rvalue)
        while True:
            try:
                value_of_char = iterator.next()
                automon_symbol = SymbolNode(value_of_char)
                automon_result = UnionNode(automon_symbol, automon_result)
            except StopIteration:
                break
        return automon_result
            

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