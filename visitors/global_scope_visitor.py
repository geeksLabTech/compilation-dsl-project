import visitors.visitor as visitor
from parser.tzscript_ast import *
from visitors.scope import Scope

class GlobalScopeVisitor:
    def __init__(self) -> None:
        self.scope = Scope()
        self.errors = []

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        
        for child in node.statements:
            self.visit(child)

        return self.scope, self.errors

    @visitor.when(EntryDeclarationNode)
    def visit(self, node: EntryDeclarationNode):
        if self.scope.is_entry_defined(node.id, len(node.params)):
            self.errors.append(f'Entry point {node.id} is already defined, error in line {node.id_line}')
        else:
            self.scope.define_entry(node.id, node.params)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode):
        if self.scope.is_func_defined(node.id, len(node.params)):
            self.errors.append(f'Function {node.id} is already defined, error in line {node.id_line}')
        else:
            self.scope.define_function(node.id, node.params, node.type)

    @visitor.when(DeclarationStorageNode)
    def visit(self, node: DeclarationStorageNode):
        if self.scope.is_local_var(node.id):
            self.errors.append(f'Variable {node.id} is already defined, error in line {node.id_line}')
        else:
            self.scope.define_variable(node.id, node.type)