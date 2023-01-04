from abc import ABC, abstractmethod

import visitor

class Node(ABC):
    @abstractmethod
    def evaluate(self):
        raise NotImplementedError()
    
    def accept(self, visitor_):
        pass

class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex
    
    def accept(self, visitor_):
        return visitor_.visit(self)

class UnaryNode(Node):
    def __init__(self, node: Node):
        self.node = node

    def evaluate(self):
        value = self.node.evaluate()
        return self.operate(value)
    
    def accept(self, visitor_):
        return visitor_.visit(self)

    @abstractmethod
    def operate(self, value):
        raise NotImplementedError()

class BinaryNode(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)
    
    def accept(self, visitor_):
        return visitor_.visit(self)

    @abstractmethod
    def operate(self, lvalue, rvalue):
        raise NotImplementedError()

# def get_printer(AtomicNode=AtomicNode, UnaryNode=UnaryNode, BinaryNode=BinaryNode, ):

#     class PrintVisitor(object):
        
#     printer = PrintVisitor()
#     return (lambda ast: printer.visit(ast))