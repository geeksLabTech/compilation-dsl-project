from parser.tzscript_ast import *
from visitors.visitor import Visitor


class TypeCheckVisitor(Visitor):
    def __init__(self):
        self.errors = []
        self.symbol_table = {}  # symbol table to store variable and function types

    def visit_program(self, node: ProgramNode):
        # check types for program node
        for statement in node.statements:
            statement.accept(self)
        return self.errors

    def visit_if_node(self, node: IfNode):
        # check types for if node
        # check that the expression is of a boolean type
        if not self.is_boolean_type(node.expr):
            self.errors.append("If statement expression must be of type boolean")
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
            f_type = self.symbol_table[node.expr.id]
            if not type(f_type) is str:
                f_type = self.symbol_table[node.expr.id]['return']

            if not node.type == f_type:
                print(
                    f"Incompatible types in variable declaration: expected {node.type}, got {f_type}")
        if node.type == 'nat':
            if type(node.expr) is MinusNode and type(node.expr.left) is ConstantNumNode and type(node.expr.right) is ConstantNumNode:
                if int(node.expr.left.lex) < int(node.expr.right.lex):
                    self.errors.append(
                        f"Value {int(node.expr.left.lex) - int(node.expr.right.lex)} cannot be assigned to 'nat' type varible")

        elif 'type' in node.expr.__dict__:
            # print("there")
            if not self.is_compatible_type(node, node.expr):
                self.errors.append(
                    f"Incompatible types in variable declaration: expected {node.type}, got {node.expr.type}")

        self.symbol_table[node.id] = node.type

    def visit_assign_node(self, node: AssignNode):
        # check types for assignment node
        # check that the variable being assigned to is in the symbol table
        if node.id not in self.symbol_table:
            raise NameError(f"Variable {node.id} not defined")
        # check that the type of the expression is compatible with the variable's type
        if not self.is_compatible_type(node, node.expr):
            self.errors.append(
                f"Incompatible types in assignment: expected {self.symbol_table[node.id]}, got {node.expr.type}")

    def visit_func_declaration_node(self, node: FuncDeclarationNode):
        # check types for function declaration node
        # add function to symbol table
        self.symbol_table[node.id] = {'return': node.type}
        # check types for function body
        for param in node.params:
            self.symbol_table[node.id][param.id] = param.type

        for statement in node.body:
            statement.accept(self)

    def visit_call_node(self, node: CallNode):
        for a in node.args:
            a.accept(self)

    def visit_var_call_node(self, node: VarCallNode):
        # print(self.symbol_table[node.id], self.get_type(node.expr))
        if not self.symbol_table[node.id] == self.get_type(node.expr):
            self.errors.append(
                f"Unable to assign {self.get_type(node.expr)} to {self.symbol_table[node.id]}")

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
            self.errors.append(
                f"Incompatible types in binary operation: {left} and {right}")

    def is_boolean_type(self, node: Node):

        boolean_nodes = [LessThanEqualNode, LessThanNode,
                         GreaterThanEqualNode, GreaterThanNode, EqualNode]

        if type(node) in boolean_nodes:

            node.left.accept(self)
            node.right.accept(self)

            return True

    def visit_return_statement(self, node: ReturnStatementNode):
        node.expr.accept(self)

    def visit_arith_node(self, node: Node, oper: str):
        if not self.get_type(node.left) == self.get_type(node.right):
            if not self.is_compatible_type(node.left, node.right):
                self.errors.append(
                    f"Cannot permform {oper} operation between {self.get_type(node.left)} and {self.get_type(node.right)}")

    def is_compatible_type(self, left, right):

        if left.type == right.type:
            return True
        if left.type == 'num' and (right.type == 'nat' or right.type == 'int'):
            return True
        if right.type == 'num':
            if left.type == 'nat' and int(right.lex) > 0:
                return True
            if left.type == 'int':
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
            return None
