from visitors.visitor import Visitor

class StringReprVisitor(Visitor):
    def __init__(self):
        self.result = ""  # string representation of the AST

    def visit_program(self, node):
        self.result += f"program {node.idx}({', '.join(param.id for param in node.params)}):\n"
        for statement in node.statements:
            statement.accept(self)

    def visit_if_node(self, node):
        self.result += "    if "
        node.expr.accept(self)
        self.result += ":\n"
        for statement in node.statements:
            statement.accept(self)

    def visit_else_node(self, node):
        self.result += "    else:\n"
        for statement in node.statements:
            statement.accept(self)

    def visit_var_declaration_node(self, node):
        self.result += f"    {node.type} {node.id} = "
        node.expr.accept(self)
        self.result += "\n"

    def visit_assign_node(self, node):
        self.result += f"    {node.id} = "
        node.expr.accept(self)
        self.result += "\n"

    def visit_func_declaration_node(self, node):
        self.result += f"    def {node.id}({', '.join(param.id for param in node.params)})"
        if node.type:
            self.result += f" -> {node.type}"
        self.result += ":\n"
        for statement in node.body:
            statement.accept(self)

    def visit_attr_declaraion_node(self, node):
        self.result += f"    {node.type} {node.id}\n"
