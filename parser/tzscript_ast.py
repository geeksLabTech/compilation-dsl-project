class Node:
    pass

class ProgramNode(Node):
    def __init__(self, idx, params, statements):
        self.idx = idx
        self.params = params
        self.statements = statements
        
class DeclarationNode(Node):
    pass
        
class ExpressionNode(Node):
    pass

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, typex, expr):
        self.id = idx
        self.type = typex
        self.expr = expr

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex):
        self.id = idx
        self.type = typex

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class CallNode(ExpressionNode):
    def __init__(self, idx, args):
        self.id = idx
        self.args = args

class ConstantNumNode(AtomicNode):
    pass

class VariableNode(AtomicNode):
    pass

class PlusNode(BinaryNode):
    pass

class MinusNode(BinaryNode):
    pass

class StarNode(BinaryNode):
    pass

class DivNode(BinaryNode):
    pass