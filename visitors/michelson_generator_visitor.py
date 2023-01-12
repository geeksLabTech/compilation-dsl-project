# from parser.tzscript_ast import *
from intermediate_ast.high_level_ir_ast import *
import visitors.visitor_d as visitor


class MichelsonGenerator(object):
    def __init__(self):
        self.code = ''

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.on(ContractNode)
    def visit(self, node: ContractNode):
        self.code = ""

        for i, entry_node in enumerate(node.entrypoints.entrypoint_list):
            self.code += f"entrypoint {entry_node.i} "
            # handle parameters
            self.code += "( "
            if len(entry_node.params) >= 1:
                for param in entry_node.params:
                    self.code += f"parameter {param.type}; "
            else:
                self.code += f"unit;"

            if node.storage[i].storage_list:
                for param in entry_node.params:
                    self.code += f"{param.type}"
            elif len(entry_node.params) == 1:
                param = entry_node.params[0]
                self.code += f"storage {param.type}; "
            else:
                self.code += f"unit"
            self.code += ")\n"

            self.code += "self.code{"

            # self.code is for contract and no idea where is the entrypoint self.code
            for st in node.self.code.statements:
                self.visit(st)

            self.code += "}\n"

        self.code += "}"

    @visitor.on(PlusNode)
    def visit(self, node: PlusNode):
        self.code += "ADD;\nPAIR;\n"

    @visitor.on(StarNode)
    def visit(self, node: StarNode):
        self.code += "MUL\nPAIR;\n"

    @visitor.on(MinusNode)
    def visit(self, node: MinusNode):
        self.code += "SUB;\nPAIR;\n"

    @visitor.on(DivNode)
    def visit(self, node: DivNode):
        self.code += "EDIV;\nPAIR;\n"

    @visitor.on(EqualNode)
    def visit(self, node: EqualNode):
        self.code += "EQ;\nPAIR;\n"

    @visitor.on(InequalityNode)
    def visit(self, node: InequalityNode):
        self.code += "NEQ;\nPAIR;\n"

    @visitor.on(GreaterThanNode)
    def visit(self, node: GreaterThanNode):
        self.code += "GT;\nPAIR;\n"

    @visitor.on(GreaterThanEqualNode)
    def visit(self, node: GreaterThanEqualNode):
        self.code += "GE;\nPAIR;\n"

    @visitor.on(LessThanNode)
    def visit(self, node: LessThanNode):
        self.code += "LT;\nPAIR;\n"

    @visitor.on(LessThanEqualNode)
    def visit(self, node: LessThanEqualNode):
        self.code += "LE;\nPAIR;\n"

    @visitor.on(WhileDeclarationNode)
    def visit(self, node: WhileDeclarationNode):
        self.code += "WHILE ("
        self.visit(node.expr)
        self.code += ") DO\n"

        for st in node.body:
            self.visit(st)

        self.code += "END\n"
