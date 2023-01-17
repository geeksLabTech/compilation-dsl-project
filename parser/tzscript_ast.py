from utils import is_valid_tezos_address


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


class StorageNode(Node):
    def __init__(self, statements) -> None:
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_storage_node(self)


class ReturnStatementNode(Node):
    def __init__(self, expr) -> None:
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_return_statement(self)


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


class WhileNode(Node):
    def __init__(self, exp, statements):
        self.expr = exp
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_while_node(self)


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
        return visitor.visit_attr_declaration_node(self)


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

class ComparisonNode(BinaryNode):
    pass 

class ArithmeticNode(BinaryNode):
    pass


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


class EqualNode(ComparisonNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_arith_node(self, "==")


class InequalityNode(ComparisonNode):
    # class IniquelatyNode(ExpressionNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_arith_node(self, "!=")


class LessThanNode(ComparisonNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_arith_node(self, "<")


class LessThanEqualNode(ComparisonNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_arith_node(self, "<=")


class GreaterThanNode(ComparisonNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_arith_node(self, ">")


class GreaterThanEqualNode(ComparisonNode):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_arith_node(self, ">=")


class TrueNode(BinaryNode):
    def accept(self, visitor):
        return visitor.visit_true_node(self)


class FalseNode(BinaryNode):
    def accept(self, visitor):
        return visitor.visit_false_node(self)


class ConstantStringNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        # print(str(lex), "tz1QV341nbgxbyzd8SYU7fJtNScaLVPMZkGC")
        if not is_valid_tezos_address(str(lex)[1:-1]):
            self.type = 'string'
        else:
            self.type = 'address'

    def accept(self, visitor):
        return visitor.visit_address_node(self)


class ConstantNumNode(AtomicNode):
    def __init__(self, lex):
        self.lex = lex
        self.type = 'num'

    def accept(self, visitor):
        return visitor.visit_constant_num_node(self)


class VariableNode(AtomicNode):
    def __init__(self, lex):
        self.lex = lex

    def accept(self, visitor):
        return visitor.visit_variable_node(self)


class PlusNode(ArithmeticNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_arith_node(self, '+')


class MinusNode(ArithmeticNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_arith_node(self, '-')


class StarNode(ArithmeticNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_arith_node(self, '*')


class DivNode(ArithmeticNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_arith_node(self, '//')
