from parser.tzscript_ast import *
from visitors.scope import Scope
import visitors.visitor as visitor
from visitors.global_scope_visitor import GlobalScopeVisitor
from parser.tzscript_types import *

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
    def visit(self, node: ProgramNode, scope=None, parent=None):

        parent = Parent(LevelRepresentatives.Program, node.idx)

        global_scope, errors = GlobalScopeVisitor().visit(node)
        if len(errors) > 0:
            return errors

        for child in node.statements:
            self.visit(child, global_scope, parent)
            
        return self.errors


    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope: Scope, parent):
        if parent == LevelRepresentatives.Program:
            return
        
        if scope.is_local_var(node.id):
            self.errors.append(f'Variable {node.id} is used, error in line {node.id_line}')

        scope.define_variable(node.id, node.type)

        type = self.visit(node.expr, scope, parent)
        if type is None:
            return None 
        if not node.type.is_compatible(type):
            self.errors.append(f'Variable type {node.type.name.value} of {node.id} is not compatible with {type.name.value} at line {node.id_line}')
            return None
        return scope

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope, parent):
        new_scope = scope.create_child_scope()
        new_parent = Parent(LevelRepresentatives.Function, node.id)

        for arg in node.params:
            scope_update = self.visit(arg, new_scope, new_parent)
            if scope_update is not None:
                new_scope = scope_update
        
        for body in node.body:
            scope_update = self.visit(body, new_scope, new_parent)
            if scope_update is not None:
                new_scope = scope_update
        
        return scope

    @visitor.when(EntryDeclarationNode)
    def visit(self, node: EntryDeclarationNode, scope: Scope, parent):
        new_parent = Parent(LevelRepresentatives.EntryPoint, node.id)
        scope.is_entry_in_scope = True
        scope_copied = scope.create_child_scope_with_parent_info()

        for arg in node.params:
            new_scope = self.visit(arg, scope_copied, new_parent)
            if new_scope is not None:
                scope_copied = new_scope
        
        for child in node.body:
            self.visit(child, scope_copied, new_parent)

        return scope

    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode, scope: Scope, parent):
        assert node.lex.isnumeric()
        return TzScriptIntOrNat()

    @visitor.when(ConstantStringNode)
    def visit(self, node: ConstantStringNode, scope: Scope, parent):
        return TzScriptString()

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope, parent):
        if not scope.is_local_var(node.lex):
            self.errors.append((f'Variable {node.lex} at line {node.line} is not defined'))
            return None
        
        var_info = scope.get_local_variable_info(node.lex)

        return var_info.type
        

    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope, parent):
        if not scope.is_func_defined(node.id, len(node.args)):
            self.errors.append(f'Function {node.id} is not defined', node)

        func_info = scope.get_local_function_info(node.id, len(node.args))
        for i, child in enumerate(node.args):
            arg_type = self.visit(child, scope, parent)
            if arg_type is None:
                return None
            if arg_type != func_info.params_types[i]:
                self.errors.append(
                    (f'Invalid argument type {arg_type.name.value} for function {node.id} at line {node.id_line}, expected {func_info.params_types[i].name}', node))
                return None
        
        return func_info.return_type
          
        
    @visitor.when(ArithmeticNode)
    def visit(self, node: BinaryNode, scope: Scope, parent):
        left_type = self.visit(node.left, scope, parent)
        right_type = self.visit(node.right, scope, parent)

        if left_type is None or right_type is None:
            return None
        
        if not left_type.is_compatible(TzScriptIntOrNat()) or not right_type.is_compatible(TzScriptIntOrNat()):
            self.errors.append((f'Invalid types {left_type.name.value} and {right_type.name.value} for arithmetic operation at line {node.keyword_line}', node.__class__.__name__))
            return None

        if left_type == right_type:
            return left_type

        if left_type == TzScriptInt() and right_type == TzScriptNat():
            return TzScriptInt()

        if left_type == TzScriptNat() and right_type == TzScriptInt():
            return TzScriptInt()

        if left_type == TzScriptIntOrNat:
            return right_type
        
        if right_type == TzScriptIntOrNat:
            return left_type

        if right_type == TzScriptInt and left_type == TzScriptNat:
            return TzScriptInt()

        if right_type == TzScriptNat and left_type == TzScriptInt:
            return TzScriptInt()

    @visitor.when(ComparisonNode)
    def visit(self, node: BinaryNode, scope: Scope, parent):
        left_type = self.visit(node.left, scope, parent)
        right_type = self.visit(node.right, scope, parent)

        if left_type is None or right_type is None:
            return None

        if not left_type.is_compatible(right_type):
            self.errors.append((f'Invalid types {left_type} and {right_type} for comparison operation at line {node.keyword_line}', node.__class__.__name__))
            return None

        return TzScriptBoolean()
        
        
    @visitor.when(IfNode)
    def visit(self, node: IfNode, scope: Scope, parent):
        
        type = self.visit(node.expr, scope, parent)
        if type is None:
            return None
        if not type.is_compatible(TzScriptBoolean()):
            self.errors.append(f'if expression must be boolean at line {node.if_line}')
            return None
            
        scope_copied_for_then = scope.create_child_scope_with_parent_info()
        scope_copied_for_else = scope.create_child_scope_with_parent_info()

        for child in node.then_statements:
            self.visit(child, scope_copied_for_then, parent)

        for child in node.else_statements:
            self.visit(child, scope_copied_for_else, parent)

    @visitor.when(VarCallNode)
    def visit(self, node: VarCallNode, scope: Scope, parent):
        if not scope.is_local_var(node.id):
            self.errors.append(f'Variable {node.id} in line {node.id_line} is not defined')
            return None
        
        var_info = scope.get_local_variable_info(node.id)
        
       
        type = self.visit(node.expr, scope, parent)
        if type is None:
            return None
        if not var_info.type.is_compatible(type):
            self.errors.append(f'Invalid type {type.name.value} for variable {node.id} at line {node.id_line}')
        
        return None

    @visitor.when(ReturnStatementNode)
    def visit(self, node: ReturnStatementNode, scope: Scope, parent):
        func_info = scope.get_local_function_info(parent.id, parent.params)

        type = self.visit(node.expr, scope, parent)
        if type is None:
            return None
        if not func_info.return_type.is_compatible(type):
            self.errors.append(f'Invalid return type {type.name.value} for function {parent.id}')

        return None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, scope: Scope, parent):

        scope.define_variable(node.id, node.type)
        return scope

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope, parent):
        type = self.visit(node.expr, scope, parent)
        if type is None:
            return None
        if not type.is_compatible(TzScriptBoolean()):
            self.errors.append(f'while expression must be boolean, line {node.while_line}')

        scope_copied = scope.create_child_scope_with_parent_info()
        
        for child in node.statements:
            self.visit(child, scope_copied, parent)


