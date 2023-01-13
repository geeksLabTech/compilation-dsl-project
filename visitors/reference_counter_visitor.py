from visitors.visitor import Visitor
from intermediate_ast.high_level_ir_ast import *
import visitors.visitor_d as visitor


class ReferenceCounterVisitor(object):
    def __init__(self) -> None:
        self.reference_counter: dict[str, int] = {}

    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(CodeNode)
    def visit(self , node: CodeNode , tabs = 0):
        for s in node.statements:
            self.visit(s)
    

    @visitor.when(IfStatementNode)
    def visit(self , node: IfStatementNode , tabs = 0):
        for s in node.expr:
            self.visit(s)

        for s in node.then_clause:
            self.visit(s)

        for s in node.else_clause:
            self.visit(s)
       
    
    @visitor.when(WhileDeclarationNode)
    def visit(self , node: WhileDeclarationNode , tabs = 0):
        for s in node.expr:
            self.visit(s)
        
        for s in node.body:
            self.visit(s)
        

    @visitor.when(IfEntryNode)
    def visit(self, node: IfEntryNode, tabs = 0):
        for s in node.statements:
            self.visit(s)

    @visitor.when(PushValueNode)
    def visit(self, node: PushValueNode, tabs = 0):
        pass

    @visitor.when(PushVariableNode)
    def visit(self, node: PushVariableNode, tabs = 0):
        pass

    @visitor.when(ReplaceVariableNode)
    def visit(self, node: ReplaceVariableNode, tabs=0):
        if node.id not in self.reference_counter:
            self.reference_counter[node.id] = 0
        self.reference_counter[node.id] += 1

    @visitor.when(GetToTopNode)
    def visit(self, node: GetToTopNode, tabs=0):
        if node.id not in self.reference_counter:
            self.reference_counter[node.id] = 0
        self.reference_counter[node.id] += 1

    @visitor.when(OperationNode)
    def visit(self, node: OperationNode, tabs = 0):
        pass

        

    

    