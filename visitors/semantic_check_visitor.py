from parser.tzscript_ast import *
from visitors.scope import Scope
import visitors.visitor_d as visitor
from enum import Enum


class LevelRepresentatives(Enum):
    '''
    Enum to represent the level of a node in the TzScript ast
    '''
    Program = 0
    EntryPoint = 1
    Function = 2


class Parent:
    def __init__(self, level: LevelRepresentatives, id: str) -> None:
        self.level = level
        self.id = id


class SemanticCheckerVisitor(object):
    def __init__(self):
        self.errors = []

    @visitor.on('node')
    def visit(self, node, scope, parent):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None, parent=None):
        if scope is None:
            scope = Scope()
        else:
            scope = Scope(parent=scope)

        self.iterations = 1
        scope.main_level = True
        parent = Parent(LevelRepresentatives.Program, node.idx)

        for child in node.statements:
            new_scope = self.visit(child, scope, parent)
            if new_scope is not None:
                scope = new_scope

        self.iterations += 1

        for child in node.statements:
            new_scope = self.visit(child, scope, parent)
            if new_scope is not None:
                scope = new_scope

        return self.errors

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope: Scope, parent):
        if self.iterations == 1:
            if scope.is_local_var(node.id) and self.iterations == 1:
                self.errors.append((f'Variable  is used', node))

        scope.define_variable(node.id)
        self.visit(node.expr, scope, parent)
        return scope

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope, parent):

        if scope.is_func_defined(node.id, len(node.params)):
            if self.iterations == 1:
                self.errors.append((f'Function name {node.id} is used', node))
        if scope.is_entry_in_scope and self.iterations == 1:
            self.errors.append(
                (f'Function {node.id} is defined after entry point', node))
        scope.define_function(node.id, len(node.params))
        new_scope = scope.create_child_scope()
        new_parent = Parent(LevelRepresentatives.Function, node.id)

        for arg in node.params:
            # print(arg.id, 'arg id')
            scope_update = self.visit(arg, new_scope, new_parent)
            if scope_update is not None:
                new_scope = scope_update
        # print(new_scope.local_vars,'var')
        for body in node.body:
            scope_update = self.visit(body, new_scope, new_parent)
            if scope_update is not None:
                new_scope = scope_update
        for idx, s in enumerate(node.body):
            if idx + 1 >= len(node.body):
                break
            if type(node.body[idx]) is not IfNode and type(node.body[idx+1]) is ElseNode:
                self.errors.append(
                    (f'Before else there can only be one if', node))

        return scope

    @visitor.when(EntryDeclarationNode)
    def visit(self, node: EntryDeclarationNode, scope: Scope, parent):
        if scope.is_func_defined(node.id, node.params) and self.iterations == 1:
            self.errors.append((f'Entry name  is used', node))

        if parent.level == LevelRepresentatives.EntryPoint and self.iterations == 1:
            self.errors.append(
                (f'Entry  statament is not allowed inside entry statament', node))
        new_parent = Parent(LevelRepresentatives.EntryPoint, node.id)
        scope.is_entry_in_scope = True
        scope.define_function(node.id, len(node.params))
        scope_copied = self.copy_scope(scope)

        for arg in node.params:
            # print(arg.id, 'arg id')
            new_scope = self.visit(arg, scope_copied, new_parent)
            if new_scope is not None:
                scope_copied = new_scope
        # new_scope = scope.create_child_scope()
        for child in node.body:
            self.visit(child, scope_copied, new_parent)

        return scope

    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode, scope: Scope, parent):
        if not node.lex.isnumeric() and self.iterations == 1:
            self.errors.append((f'Value is not Numeric', node))
        # if parent.level == LevelRepresentatives.Program and self.iterations == 1:
        #     self.errors.append(
        #         (f'In the corpus of the program declare entry functions or variables not this constant {node.lex}', node))

        return None

    @visitor.when(ConstantStringNode)
    def visit(self, node: ConstantStringNode, scope: Scope, parent):
        pass

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope, parent):
        if not scope.is_local_var(node.lex) and self.iterations == 1:
            self.errors.append((f'Invalid variable {node.lex}',node))
        # if parent.level == LevelRepresentatives.Program and self.iterations == 1:
        #     self.errors.append(
        #         (f'In the corpus of the program declare entry functions or variables not this constant ',node))

    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope, parent):
        if not scope.is_func_defined(node.id, len(node.args)):

            if self.iterations == 2:
                self.errors.append(
                    (f'Function {node.id} is not defined', node))
        if parent.level == LevelRepresentatives.Program and self.iterations == 1:
            self.errors.append(
                (f'In the corpus of the program declare entry functions or variables not this call ', node))

        for child in node.args:
            new_scope = self.visit(child, scope, parent)

            if new_scope is not None:
                scope = new_scope

    @visitor.when(BinaryNode)
    def visit(self, node: BinaryNode, scope: Scope, parent):
        self.visit(node.left, scope, parent)
        self.visit(node.right, scope, parent)
        if parent.level == LevelRepresentatives.Program and self.iterations == 1:
            self.errors.append(
                (f'In the corpus of the program declare entry functions or variables not this operation', node))

    @visitor.when(IfNode)
    def visit(self, node: IfNode, scope: Scope, parent):
        print(parent == LevelRepresentatives.Function)
        # new_scope = scope.create_child_scope()
        scope_copied = self.copy_scope(scope)

        if scope.main_level and self.iterations == 1:
            self.errors.append(
                (f'If statement is not allowed in main level', node))
        if parent.level == LevelRepresentatives.Program and self.iterations == 1:
            self.errors.append(
                (f'In the corpus of the program declare entry functions or variables not this statament if', node))
        scope.is_if_in_scope = True
        self.visit(node.expr, scope_copied, parent)
        for child in node.statements:
            self.visit(child, scope_copied, parent)

    @visitor.when(ElseNode)
    def visit(self, node: ElseNode, scope: Scope, parent):
        scope_copied = self.copy_scope(scope)
        if not scope.is_if_in_scope and self.iterations == 1:
            self.errors.append(
                (f'Else statement is not allowed without if statement',node))
        else:
            scope.is_if_in_scope = False
        if parent.level == LevelRepresentatives.Program and self.iterations == 1:
            self.errors.append(
                (f'In the corpus of the program declare entry functions or variables not this else',node))
        for child in node.statements:
            self.visit(child, scope_copied, parent)

    @visitor.when(VarCallNode)
    def visit(self, node: VarCallNode, scope: Scope, parent):
        # print('estoy en', node.id, scope.local_vars)
        self.visit(node.expr, scope, parent)
        if not scope.is_local_var(node.id) and self.iterations == 1:
            self.errors.append((f'Variable  is not defined',node))

    @visitor.when(ReturnStatementNode)
    def visit(self, node: ReturnStatementNode, scope: Scope, parent):
        if parent.level == LevelRepresentatives.Program and self.iterations == 1:
            self.errors.append(
                (f'In the corpus of the program declare entry functions or variables not this return ',node))
        if not parent.level == LevelRepresentatives.Function and self.iterations == 1:
            # print('entre')
            print(parent)
            self.errors.append(
                (f'Return statement is only allowed in a funcion',node))
        self.visit(node.expr, scope, parent)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, scope: Scope, parent):

        scope.define_variable(node.id)
        return scope

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope, parent):
        scope_copied = self.copy_scope(scope)
        if parent.level == LevelRepresentatives.Program and self.iterations == 1:
            self.errors.append(
                (f'In the corpus of the program declare entry functions or variables not this while',node))
        if scope.main_level and self.iterations == 1:
            self.errors.append(
                (f'While statement is not allowed in main level',node))
        self.visit(node.expr, scope_copied, parent)
        for child in node.statements:
            self.visit(child, scope_copied, parent)



    def copy_scope(self, scope: Scope):
        scope_copied = Scope()

        for f in scope.local_funcs:
            scope_copied.local_funcs.append(f)
        for v in scope.local_vars:
            scope_copied.local_vars.append(v)
        
        return scope_copied