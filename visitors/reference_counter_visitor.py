
from intermediate_ast.high_level_ir_ast import *
import visitors.visitor as visitor


class References:
    def __init__(self):
        self.normal_references_count = 0
        self.references_in_cycles_count = 0

class ReferenceCounterVisitor(object):
    def __init__(self) -> None:
        self.reference_counter: dict[str, References] = {}

    @visitor.on('node')
    def visit(self, node, is_inside_cycle = False, checked_vars = None):
          pass

    @visitor.when(CodeNode)
    def visit(self , node: CodeNode , is_inside_cycle = False = 0, checked_vars = None):
        for s in node.statements:
            self.visit(s)
    

    @visitor.when(IfStatementNode)
    def visit(self , node: IfStatementNode , is_inside_cycle = False, checked_vars = None):
        for s in node.expr:
            last_checked = self.visit(s, is_inside_cycle, checked_vars)
            if last_checked is not None:
                checked_vars = last_checked

        for s in node.then_clause:
            last_checked = self.visit(s, is_inside_cycle, checked_vars)
            if last_checked is not None:
                checked_vars = last_checked

        for s in node.else_clause:
            last_checked = self.visit(s, is_inside_cycle, checked_vars)
            if last_checked is not None:
                checked_vars = last_checked
       
    
    @visitor.when(WhileDeclarationNode)
    def visit(self , node: WhileDeclarationNode , is_inside_cycle = False, checked_vars = None):
        checked_vars = {}
        for s in node.expr:
            last_checked = self.visit(s, True, checked_vars)
            if last_checked is not None:
                checked_vars = last_checked
        
        for s in node.body:
            last_checked = self.visit(s, True, checked_vars)
            if last_checked is not None:
                checked_vars = last_checked
        
        

    @visitor.when(IfEntryNode)
    def visit(self, node: IfEntryNode, is_inside_cycle = False, checked_vars = None):
        for s in node.statements:
            self.visit(s)

    @visitor.when(PushValueNode)
    def visit(self, node: PushValueNode, is_inside_cycle = False, checked_vars = None):
        pass

    @visitor.when(PushVariableNode)
    def visit(self, node: PushVariableNode, is_inside_cycle = False, checked_vars = None):
        pass

    @visitor.when(ReplaceVariableNode)
    def visit(self, node: ReplaceVariableNode, is_inside_cycle = False, checked_vars = None):
        if node.id not in self.reference_counter:
            self.reference_counter[node.id] = References()
        if is_inside_cycle:
            self.reference_counter[node.id].references_in_cycles_count += 1
        else:
            self.reference_counter[node.id].normal_references_count += 1

    @visitor.when(GetToTopNode)
    def visit(self, node: GetToTopNode, is_inside_cycle = False, checked_vars = None):
        if node.id not in self.reference_counter:
            self.reference_counter[node.id] = References()
        if is_inside_cycle:
            if node.id in checked_vars:
                return
            self.reference_counter[node.id].references_in_cycles_count += 1
            checked_vars[node.id] = True
            return checked_vars
        else:
            self.reference_counter[node.id].normal_references_count += 1

    @visitor.when(OperationNode)
    def visit(self, node: OperationNode, is_inside_cycle = False, checked_vars = None):
        pass

        

    

    