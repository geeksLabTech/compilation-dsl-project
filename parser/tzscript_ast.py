from lib2to3.pgen2 import token
from operator import le
from time import sleep
from lexer.lex_token import Token
from utils import is_valid_tezos_address


class Node:
    def accept(self, visitor):
        pass


class ProgramNode(Node):
    def __init__(self, idx: Token, params, statements):
        self.id_line = idx.line_no
        self.idx = idx.lex
        self.params = params
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_program(self)


class DeclarationNode(Node):
    pass


class ExpressionNode(Node):
    pass


class IfNode(Node):
    def __init__(self, if_keyword: Token, then_keyword: Token, expr, then_statements,else_statements) -> None:
        self.if_line = if_keyword.line_no
        self.then_line = then_keyword.line_no
        # self.else_line = else_keyword.line_no
        self.expr = expr
        self.then_statements = then_statements
        self.else_statements = else_statements
        
    def accept(self, visitor):
        return visitor.visit_if_node(self)


class ReturnStatementNode(Node):
    def __init__(self, return_keyword: Token, expr) -> None:
        self.return_line = return_keyword.line_no
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_return_statement(self)


class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx: Token, typex: Token, expr):
        self.id_line = idx.line_no
        self.id = idx.lex
        self.type = typex.tzscript_type
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_var_declaration_node(self)

class DeclarationStorageNode(ExpressionNode):
    def __init__(self, idx: Token, typex: Token):
        self.id_line = idx.line_no
        self.id = idx.lex
        self.type = typex.tzscript_type


    def accept(self, visitor):
        return visitor.visit_declaration_storage_node(self)


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx: Token, params, return_type: Token, body):
        self.id_line = idx.line_no
        self.id = idx.lex
        self.params = params
        self.type = return_type.tzscript_type
        self.body = body

    def accept(self, visitor):
        return visitor.visit_func_declaration_node(self)


class WhileNode(Node):
    def __init__(self, while_keyword: Token, exp, statements):
        self.while_line = while_keyword.line_no
        self.expr = exp
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_while_node(self)


class EntryDeclarationNode(DeclarationNode):
    def __init__(self, idx: Token, params, body):
        self.id_line = idx.line_no
        self.id = idx.lex
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_entry_declaration_node(self)


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx: Token, typex: Token):
        self.id_line = idx.line_no
        self.id = idx.lex
        self.type = typex.tzscript_type

    def accept(self, visitor):
        return visitor.visit_attr_declaration_node(self)


class AtomicNode(ExpressionNode):
    def __init__(self, token: Token):
        self.line = token.line_no
        self.lex = token.lex

    def accept(self, visitor):
        return visitor.visit_atomic_node(self)


class BinaryNode(ExpressionNode):
    def __init__(self, keyword: Token, left, right):
        self.keyword_line = keyword.line_no
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_node(self)

class ComparisonNode(BinaryNode):
    def __init__(self, keyword: Token, left, right):
        super().__init__(keyword, left, right)

class ArithmeticNode(BinaryNode):
    pass


class CallNode(ExpressionNode):
    def __init__(self, idx: Token, args):
        self.id_line = idx.line_no
        self.id = idx.lex
        self.args = args

    def accept(self, visitor):
        return visitor.visit_call_node(self)


class VarCallNode(DeclarationNode):
    def __init__(self, idx: Token, expr) -> None:
        self.id_line = idx.line_no
        self.id = idx.lex
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_var_call_node(self)


class EqualNode(ComparisonNode):
    def __init__(self, keyword: Token, left, right):
        super().__init__(keyword, left, right)

    def accept(self, visitor):
        return visitor.visit_arith_node(self, "==")


class InequalityNode(ComparisonNode):
    # class IniquelatyNode(ExpressionNode):
    def __init__(self, keyword: Token, left, right):
        super().__init__(keyword, left, right)

    def accept(self, visitor):
        return visitor.visit_arith_node(self, "!=")


class LessThanNode(ComparisonNode):
    def __init__(self, keyword: Token, left, right):
        super().__init__(keyword, left, right)

    def accept(self, visitor):
        return visitor.visit_arith_node(self, "<")


class LessThanEqualNode(ComparisonNode):
    def __init__(self, keyword: Token, left, right):
        super().__init__(keyword, left, right)

    def accept(self, visitor):
        return visitor.visit_arith_node(self, "<=")


class GreaterThanNode(ComparisonNode):
    def __init__(self, keyword: Token, left, right):
        super().__init__(keyword, left, right)

    def accept(self, visitor):
        return visitor.visit_arith_node(self, ">")


class GreaterThanEqualNode(ComparisonNode):
    def __init__(self, keyword: Token, left, right):
        super().__init__(keyword, left, right)

    def accept(self, visitor):
        return visitor.visit_arith_node(self, ">=")


class TrueNode(AtomicNode):
    def accept(self, visitor):
        return visitor.visit_true_node(self)


class FalseNode(AtomicNode):
    def accept(self, visitor):
        return visitor.visit_false_node(self)


class ConstantStringNode(AtomicNode):
    def __init__(self, token: Token):
        super().__init__(token)
        self.type = token.tzscript_type

    def accept(self, visitor):
        return visitor.visit_address_node(self)


class ConstantNumNode(AtomicNode):
    def __init__(self, token: Token):
        super().__init__(token)
        self.type = 'num'

    def accept(self, visitor):
        return visitor.visit_constant_num_node(self)


class VariableNode(AtomicNode):
    def __init__(self, token: Token):
        super().__init__(token)

    def accept(self, visitor):
        return visitor.visit_variable_node(self)


class PlusNode(ArithmeticNode):
    def __init__(self, keyword: Token, left, right):
        super().__init__(keyword, left, right)

    def accept(self, visitor):
        return visitor.visit_arith_node(self, '+')


class MinusNode(ArithmeticNode):
    def __init__(self, keyword: Token, left, right):
        super().__init__(keyword, left, right)

    def accept(self, visitor):
        return visitor.visit_arith_node(self, '-')


class StarNode(ArithmeticNode):
    def __init__(self, keyword: Token, left, right):
        super().__init__(keyword, left, right)

    def accept(self, visitor):
        return visitor.visit_arith_node(self, '*')


class DivNode(ArithmeticNode):
    def __init__(self, keyword: Token, left, right):
        super().__init__(keyword, left, right)

    def accept(self, visitor):
        return visitor.visit_arith_node(self, '//')
