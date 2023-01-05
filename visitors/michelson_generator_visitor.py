from visitors.visitor import Visitor
from parser.tzscript_ast import *

class MichelsonGeneratorVisitor(Visitor):
    def __init__(self):
        self.result = []
    
    def visit_program(self, node: ProgramNode):
        self.result.append("parameter (pair")
        for param in node.params:
            self.result.append(param.accept(self))
        self.result.append(")")
        self.result.append("storage (pair")
        for statement in node.statements:
            self.result.append(statement.accept(self))
        self.result.append(")")
        return "\n".join(self.result)

    def visit_if_node(self, node: IfNode):
        self.result.append("if")
        self.result.append(node.expr.accept(self))
        self.result.append("then")
        for statement in node.statements:
            self.result.append(statement.accept(self))
        self.result.append("else")
        return "\n".join(self.result)

    def visit_else_node(self, node: ElseNode):
        for statement in node.statements:
            self.result.append(statement.accept(self))
        return "\n".join(self.result)

    def visit_var_declaration_node(self, node: VarDeclarationNode):
        self.result.append(f"{node.id} : {node.type}")
        self.result.append(node.expr.accept(self))
        return "\n".join(self.result)

    def visit_assign_node(self, node: AssignNode):
        self.result.append(f"{node.id} <- {node.expr.accept(self)}")
        return "\n".join(self.result)

    def visit_func_declaration_node(self, node: FuncDeclarationNode):
        self.result.append(f"{node.id} (pair")
        for param in node.params:
            self.result.append(param.accept(self))
        self.result.append(") : {node.type}")
        for statement in node.body:
            self.result.append(statement.accept(self))
        return "\n".join(self.result)

    def visit_attr_declaration_node(self, node: AttrDeclarationNode):
        self.result.append(f"{node.id} : {node.type}")
        return "\n".join(self.result)

    def visit_atomic_node(self, node: AtomicNode):
        return node.lex

    def visit_binary_node(self, node: BinaryNode):
        return f"{node.left.accept(self)} {node.right.accept(self)}"

    def visit_call_node(self, node: CallNode):
        func_name = node.id
        args_code = []
        for arg in node.args:
            arg_code = arg.accept(self)
            args_code.append(arg_code)

        return f"{func_name} {' '.join(args_code)}"
