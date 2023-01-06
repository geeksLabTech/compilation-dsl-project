class Node:
    def accept(self, visitor):
        pass


class ProgramNode(Node):
    def __init__(self, idx, params, statements):
        self.idx = idx
        self.params = params
        self.statements = statements
    
    def accept(self, visitor):
        return visitor.visit_program(self)
        
class DeclarationNode(Node):
    pass
        
class ExpressionNode(Node):
    pass

class IfNode(Node):
    def __init__(self, expr, statements) -> None:
        self.expr = expr
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_if_node(self)

class ElseNode(Node):
    def __init__(self, statements) -> None:
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_else_node(self)

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, typex, expr):
        self.id = idx
        self.type = typex
        self.expr = expr
    
    def accept(self, visitor):
        return visitor.visit_var_declaration_node(self)

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr
    def accept(self, visitor):
        return visitor.visit_assign_node(self)
class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body
    def accept(self, visitor):
        return visitor.visit_func_declaration_node(self)

class EntryDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, body):
        self.id = idx
        self.params = params
        self.body = body
    def accept(self, visitor):
        return visitor.visit_entry_declaration_node(self)

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex):
        self.id = idx
        self.type = typex
    def accept(self, visitor):
        return visitor.visit_attr_declaraion_node(self)
    

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex
    def accept(self, visitor):
        return visitor.visit_atomic_node(self)

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def accept(self, visitor):
        return visitor.visit_binary_node(self)

class CallNode(ExpressionNode):
    def __init__(self, idx, args):
        self.id = idx
        self.args = args
    def accept(self, visitor):
        return visitor.visit_call_node(self)

class VarCallNode(DeclarationNode):
    def __init__(self, idx, expr) -> None:
        self.id = idx
        self.expr = expr
    
    def accept(self, visitor):
        return visitor.visit_var_call_node(self)

class ReturnNode(ExpressionNode):
    def __init__(self, expr) -> None:
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_return_node(self)
class TrueNode(ExpressionNode):
    def accept(self, visitor):
        return visitor.visit_true_node(self)

class FalseNode(ExpressionNode):
    def accept(self, visitor):
        return visitor.visit_false_node(self)

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