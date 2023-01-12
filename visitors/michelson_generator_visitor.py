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

    @visitor.on(IfStatementNode)
    def visit(self, node: IfStatementNode):

        self.code += "IF {\n"
        for st in node.then_clause:
            self.visit(st)
        self.code += "}\n"
        if not node.else_clause is None:
            self.code += '{\n'

            for st in node.else_clause:
                self.visit(st)

            self.code += '}\n'
