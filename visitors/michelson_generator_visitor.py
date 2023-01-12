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
            code += f"entrypoint {entry_node.i} "
            # handle parameters
            code += "( "
            if len(entry_node.params) >= 1:
                for param in entry_node.params:
                    code += f"parameter {param.type}; "
            else:
                code += f"unit;"

            if node.storage[i].storage_list:
                for param in entry_node.params:
                    code += f"{param.type}"
            elif len(entry_node.params) == 1:
                param = entry_node.params[0]
                code += f"storage {param.type}; "
            else:
                code += f"unit"
            code += ")\n"

            code += "code{"

            # code is for contract and no idea where is the entrypoint code
            for st in node.code.statements:
                self.visit(st)

            code += "}\n"

        code += "}"
