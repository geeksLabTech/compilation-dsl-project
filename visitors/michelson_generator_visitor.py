# from parser.tzscript_ast import *
from intermediate_ast.high_level_ir_ast import *
import visitors.visitor_d as visitor


class MichelsonGenerator(object):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.on(ContractNode)
    def visit(self, node: ContractNode):
        code = ""

        for i, entry_node in enumerate(node.entrypoints.entrypoint_list):
            code += f"parameter {entry_node.i} "
            # handle parameters
            for param in entry_node.params:
                code += f"({param.id}:{param.type})"
            code += "\n"

        for
        
        code += "}"
