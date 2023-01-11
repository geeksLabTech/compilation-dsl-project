from visitors.visitor import Visitor
from parser.tzscript_ast import *


class IndexVisitor(Visitor):
    def __init__(self, index_list):
        self.index_list = index_list
        self.final_dict = {}
        self.last_index = 0

    def visit_program(self, node: ProgramNode):
        if str(self.index_list[self.last_index][0]) == 'contract':
            self.final_dict[node] = self.index_list[self.last_index][1]
        self.last_index += 2

        for arg in node.params:
            # print("arg:")
            # print(arg)
            arg.accept(self)
        for st in node.statements:
            st.accept(self)
        return self.final_dict

    def visit_if_node(self, node: IfNode):
        if str(self.index_list[self.last_index][0]) == "if":
            self.final_dict[node] = self.index_list[self.last_index][1]
        else:
            print(self.index_list[self.last_index][0], "if")
        self.last_index += 1

        for i in node.statements:
            i.accept(self)

    def visit_else_node(self, node: ElseNode):
        if str(self.index_list[self.last_index][0]) == "else":
            self.final_dict[node] = self.index_list[self.last_index][1]
        else:
            print(self.index_list[self.last_index][0], "else")
        self.last_index += 1

    def visit_return_statement_node(self, node: ReturnStatementNode):
        if str(self.index_list[self.last_index][0]) == "return":
            self.final_dict[node] = self.index_list[self.last_index][1]
        else:
            print(self.index_list[self.last_index][0], "return")
        self.last_index += 1

    def visit_var_declaration_node(self, node: VarDeclarationNode):
        if str(self.index_list[self.last_index][0]) == "let":
            self.final_dict[node] = self.index_list[self.last_index][1]
            # self.last_index += 5
        else:
            print(self.index_list[self.last_index][0], "let")
        self.last_index += 5
        node.expr.accept(self)

    def visit_assign_node(self, node: AssignNode):
        if str(self.index_list[self.last_index][0]) == "id" and str(self.index_list[self.last_index+1][0]) == id:
            self.final_dict[node] = self.index_list[self.last_index][1]
        else:
            print(self.index_list[self.last_index][0], "id")
        self.last_index += 3

    def visit_func_declaration_node(self, node: FuncDeclarationNode):
        if str(self.index_list[self.last_index][0]) == "func":
            self.final_dict[node] = self.index_list[self.last_index][1]
            # self.last_index += 1
        else:
            print(self.index_list[self.last_index][0], "func")
        self.last_index += 2

        for arg in node.params:
            arg.accept(self)

        for st in node.body:
            st.accept(self)

    def visit_while_node(self, node: WhileNode):
        if str(self.index_list[self.last_index][0]) == "while":
            self.final_dict[node] = self.index_list[self.last_index][1]
            # self.last_index += 1
        else:
            print(self.index_list[self.last_index][0], "while")
        self.last_index += 1

    def visit_entry_declaration_node(self, node: EntryDeclarationNode):
        if str(self.index_list[self.last_index][0]) == "entry":
            self.final_dict[node] = self.index_list[self.last_index][1]
            # self.last_index += 1
        else:
            print(self.index_list[self.last_index][0], "entry")

        self.last_index += 2

        for arg in node.params:
            arg.accept(self)

        for st in node.body:
            st.accept(self)

    def visit_attr_declaration_node(self, node: AttrDeclarationNode):
        if str(self.index_list[self.last_index][0]) == "id":
            self.final_dict[node] = self.index_list[self.last_index][1]
            # self.last_index += 1
        else:
            print(self.index_list[self.last_index][0], "id")
        self.last_index += 2

    def visit_atomic_node(self, node: AtomicNode):
        self.last_index += 1

    def visit_binary_node(self, node: BinaryNode):
        self.last_index += 1
        node.left.accept(self)
        node.right.accept(self)

    def visit_call_node(self, node: CallNode):
        print(self.last_index)
        if str(self.index_list[self.last_index][0]) == "id":
            for arg in node.args:
                arg.accept(self)
            self.final_dict[node] = self.index_list[self.last_index][1]
            # self.last_index += 1
        else:
            print(self.index_list[self.last_index][0], "id")
        self.last_index += 1
        for arg in node.args:
            self.last_index += 1
            arg.accept(self)

    def visit_var_call_node(self, node: VarCallNode):
        if str(self.index_list[self.last_index][0] == 'id'):
            if str(self.index_list[self.last_index+1][0] == '='):
                self.final_dict[node] = self.index_list[self.last_index][1]
        self.last_index += 2
        node.expr.accept(self)

    def visit_arith_node(self, node: EqualNode, oper):
        print(self.last_index)
        if str(self.index_list[self.last_index+1][0]) == str(oper):
            self.final_dict[node] = self.index_list[self.last_index][1]
        else:
            print(self.index_list[self.last_index+1][0], oper)
        self.last_index += 3

    def visit_true_node(self, node: TrueNode):
        pass

    def visit_false_node(self, node: FalseNode):
        pass

    def visit_constant_string_node(self, node: ConstantStringNode):
        pass

    def visit_constant_num_node(self, node: ConstantNumNode):
        pass

    def visit_variable_node(self, node: VariableNode):
        self.final_dict[node] = self.index_list[self.last_index][1]
        # self.last_index += 1
