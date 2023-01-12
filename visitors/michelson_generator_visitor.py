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
            # self.code += ""
            # handle parameters
            # self.code += "( "
            if len(entry_node.params) >= 1:
                self.code += f"parameter "
                close = []
                for i, param in enumerate(entry_node.params):
                    if len(entry_node.params) > 1 and i != len(entry_node.params)-1:
                        self.code += f"( or {param}"
                        close.append(")")
                for c in close:
                    self.code += c

                self.code += ";\n"
            else:
                self.code += f"unit;\n"

            # process storage
            self.code += "storage"
            if len(node.storage[i].storage_list) > 0:
                close = []
                for i, s in enumerate(node.storage[i].storage_list):
                    if i != len(node.storage[i].storage_list)-1:
                        self.code += f"( or {s} "
                        close.append(")")
                for c in close:
                    self.code += c
                self.code += ";\n"
            else:
                self.code += "unit;\n"

            self.code += "code{"

            # self.code is for contract and no idea where is the entrypoint self.code
            for st in node.self.code.statements:
                self.visit(st)

            self.code += "}\n"

        self.code += "}"

    @visitor.on(PushValueNode)
    def visit(self, node: PushValueNode):
        if str(node.type) == 'num':
            tp = 'int'
        else:
            tp = node.type
        self.code += f"PUSH {tp} {node.value};\n"

    @visitor.on(PushVariableNode)
    def visit(self, node: PushVariableNode):
        # TODO GET VALUE of ID
        if str(node.type) == 'num':
            tp = 'int'
        else:
            tp = node.type
        self.code += f"PUSH {tp} {node.id};\n"

    @visitor.on(PlusNode)
    def visit(self, node: PlusNode):
        self.code += "ADD;\n"

    @visitor.on(StarNode)
    def visit(self, node: StarNode):
        self.code += "MUL\n"

    @visitor.on(MinusNode)
    def visit(self, node: MinusNode):
        self.code += "SUB;\n"

    @visitor.on(DivNode)
    def visit(self, node: DivNode):
        self.code += "EDIV;\n"

    @visitor.on(EqualNode)
    def visit(self, node: EqualNode):
        self.code += "EQ;\n"

    @visitor.on(InequalityNode)
    def visit(self, node: InequalityNode):
        self.code += "NEQ;\n"

    @visitor.on(GreaterThanNode)
    def visit(self, node: GreaterThanNode):
        self.code += "GT;\n"

    @visitor.on(GreaterThanEqualNode)
    def visit(self, node: GreaterThanEqualNode):
        self.code += "GE;\n"

    @visitor.on(LessThanNode)
    def visit(self, node: LessThanNode):
        self.code += "LT;\n"

    @visitor.on(LessThanEqualNode)
    def visit(self, node: LessThanEqualNode):
        self.code += "LE;\n"

    # this is wrong
    @visitor.on(WhileDeclarationNode)
    def visit(self, node: WhileDeclarationNode):
        self.code += "WHILE ("
        self.visit(node.expr)
        self.code += ") DO\n"

        for st in node.body:
            self.visit(st)

        self.code += "END\n"
