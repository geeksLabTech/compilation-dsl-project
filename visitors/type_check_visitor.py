import hashlib
import base58
from parser.tzscript_ast import *
from visitors.visitor import Visitor
from utils import is_valid_tezos_address


class TypeCheckVisitor(Visitor):
    def __init__(self):
        self.errors = []
        self.func = []
        self.it = 1
        self.symbol_table = {}  # symbol table to store variable and function types

    def visit_program(self, node: ProgramNode):
        # check types for program node
        for statement in node.statements:
            statement.accept(self)
        self.it += 1
        for statement in node.statements:
            statement.accept(self)

        return self.errors

    def visit_if_node(self, node: IfNode):
        # check types for if node
        # check that the expression is of a boolean type
        if not self.is_boolean_type(node.expr):
            self.errors.append(
                ("If statement expression must be of type boolean", nodes))
        node.expr.accept(self)
        for statement in node.statements:
            statement.accept(self)

    def visit_else_node(self, node: ElseNode):
        # check types for else node
        for statement in node.statements:
            statement.accept(self)

    def visit_var_declaration_node(self, node: VarDeclarationNode):
        # check types for variable declaration node
        # check that the type of the expression is compatible with the declared type
        # print(node.id, node.expr)
        if type(node.expr) is CallNode:
            # print("here")
            if not node.expr.id in self.symbol_table:
                self.symbol_table[node.expr.id] = {'return': '?'}
            f_type = self.symbol_table[node.expr.id]
            if not type(f_type) is str:
                f_type = self.symbol_table[node.expr.id]['return']

            if not node.type == f_type:
                if self.it == 2 and f_type == '?':
                    self.errors.append(
                        (f'Undefined Function {node.expr.id}', node))
                if f_type != '?':
                    if node.type == 'address':
                        self.errors.append(("Invalid Tezos Address", node))
                    else:
                        self.errors.append(
                            (f"Incompatible types in variable declaration: expected {node.type}, got {f_type}", node))

        if node.type == 'nat':
            if type(node.expr) is MinusNode and type(node.expr.left) is ConstantNumNode and type(node.expr.right) is ConstantNumNode:
                if self.it == 1 and int(node.expr.left.lex) < int(node.expr.right.lex):
                    self.errors.append(
                        (f"Value {int(node.expr.left.lex) - int(node.expr.right.lex)} cannot be assigned to 'nat' type variable", node))

        elif 'type' in node.expr.__dict__:
            # print("there")
            if self.it == 1 and not self.is_compatible_type(node, node.expr):
                if node.type == 'address':
                    self.errors.append(("Invalid Tezos Address", node))
                else:
                    self.errors.append(
                        (f"Incompatible types in variable declaration: expected {node.type}, got {node.expr.type}", node))
        node.expr.accept(self)
        self.symbol_table[node.id] = node.type

    def visit_assign_node(self, node: AssignNode):
        # check types for assignment node
        # check that the variable being assigned to is in the symbol table
        if node.id not in self.symbol_table:
            raise NameError((f"Variable {node.id} not defined", node))
        # check that the type of the expression is compatible with the variable's type
        if not self.is_compatible_type(node, node.expr):
            if "type" in node.__dict__ and node.type == 'address':
                self.errors.append(("Invalid Tezos Address", node))
            else:
                self.errors.append(
                    (f"Incompatible types in assignment: expected {self.symbol_table[node.id]}, got {node.expr.type}", node))

    def visit_func_declaration_node(self, node: FuncDeclarationNode):
        # check types for function declaration node
        # add function to symbol table
        self.symbol_table[node.id] = {'return': node.type}
        self.func.append(node.id)
        # check types for function body
        for param in node.params:
            self.symbol_table[node.id][param.id] = param.type

        ret_type = None
        for statement in node.body:
            statement.accept(self)

        self.func.pop(-1)
        # if not ret_type == self.symbol_table[node.id]['return']:
        #     self.errors.append(
        #         f"Invalid return type for function call {node.id} expected {self.symbol_table[node.id]['return']}, got {ret_type}")

    def visit_call_node(self, node: CallNode):
        ret_type = None
        for a in node.args:
            a.accept(self)

    def visit_var_call_node(self, node: VarCallNode):
        if not self.symbol_table[node.id] == self.get_type(node.expr) and not self.is_compatible_type(node, node.expr) and self.it == 2:
            # print(self.symbol_table[node.id], self.get_type(node.expr))
            if not (self.get_type(node.expr) in ['num', 'int'] and self.symbol_table[node.id] in ['num', 'int']):
                self.errors.append(
                    (f"Unable to assign {self.get_type(node.expr)} to {self.symbol_table[node.id]}", node))

    def visit_constant_num_node(self, node: ConstantNumNode):
        pass

    def visit_entry_declaration_node(self, node: EntryDeclarationNode):
        for p in node.params:
            p.accept(self)
        for st in node.body:
            st.accept(self)

    def visit_attr_declaration_node(self, node: AttrDeclarationNode):
        # check types for attribute declaration node
        self.symbol_table[node.id] = node.type

    def visit_atomic_node(self, node: AtomicNode):
        # check types for atomic node
        pass

    def visit_binary_node(self, node: BinaryNode):
        # check types for binary node
        # check that operand types are compatible with the operation
        left = self.get_type(node.left)
        right = self.get_type(node.rigt)

        if not self.is_compatible_type(left, right):
            if "type" in node.__dict__ and node.type == 'address':
                self.errors.append(("Invalid Tezos Address", node))
            else:
                self.errors.append(
                    (f"Incompatible types in binary operation: {left} and {right}", node))

    def is_boolean_type(self, node: Node):

        boolean_nodes = [LessThanEqualNode, LessThanNode,
                         GreaterThanEqualNode, GreaterThanNode, EqualNode]

        if type(node) in boolean_nodes:

            node.left.accept(self)
            node.right.accept(self)

            return True

    def visit_address_node(self, node: ConstantStringNode):
        if node.type == 'address' and type(node.lex) is str:
            if not is_valid_tezos_address(node.lex[1:-1]):
                self.errors.append(("Invalid tezos address", node))

    def visit_variable_node(self, node: VariableNode):
        pass

    def visit_return_statement(self, node: ReturnStatementNode):
        if 'type' in node.expr.__dict__:
            if node.expr.type != self.symbol_table[self.func[-1]] and self.it == 1:
                self.errors.append(
                    (f"Invalid return type for function call {self.func[-1]} expected {self.symbol_table[self.func[-1]]['return']}, got {node.expr.type}", node))

    def visit_while_node(self, node: WhileNode):
        node.expr.accept(self)
        for st in node.statements:
            st.accept(self)

    def visit_arith_node(self, node: Node, oper: str):

        if type(node.left) is ConstantNumNode or type(node.right) is ConstantNumNode:
            if type(node.left) is ConstantStringNode or type(node.right) is ConstantStringNode:
                if type(node.left) != type(node.right) and self.it == 1:
                    self.errors.append(
                        (f"Cannot permform '{oper}' operation between {self.get_type(node.left)} and {self.get_type(node.right)}", node))
                    return

        if not self.get_type(node.left) == self.get_type(node.right):
            node.right.accept(self)
            node.left.accept(self)
            if not self.is_compatible_type(node.left, node.right) and self.it == 1:
                self.errors.append(
                    (f"Cannot permform '{oper}' operation between {self.get_type(node.left)} and {self.get_type(node.right)}", node))

    def is_compatible_type(self, left, right):
        left_type = self.get_type(left)
        right_type = self.get_type(right)

        if left_type == right_type:
            return True
        if left_type == 'int' and (right_type == 'num' or right_type == 'nat'):
            return True
        if left_type == 'num' and (right_type == 'nat' or right_type == 'int'):
            return True
        if right_type == 'num':
            if left_type == 'nat' and int(right.lex) > 0:
                return True
            if left_type == 'int':
                return True
            else:
                False
        # TODO get compatibility list
        return False

    def get_type(self, node):
        if type(node) is CallNode:
            return self.symbol_table[node.id]['return']
        if type(node) is VariableNode:
            if node.lex in self.symbol_table:
                return self.symbol_table[node.lex]
        if 'type' in node.__dict__:
            return node.type
        else:
            if type(node) in [PlusNode, MinusNode, StarNode, DivNode]:
                return 'num'
            elif type(node) in [LessThanEqualNode, LessThanNode, GreaterThanNode, GreaterThanEqualNode, EqualNode]:
                return 'bool'
            return None
