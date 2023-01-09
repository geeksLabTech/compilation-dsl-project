from parser.tzscript_ast import *
from visitors.scope import Scope
import visitors.visitor_d as visitor
# class SemanticCheckVisitor:
#     def __init__(self):
#         self.symbol_table = {}

#     def visit_program(self, node:ProgramNode):
#         # Traverse the program node and all of its child nodes, performing semantic checks
#         for statement in node.statements:
#             statement.accept(self)
#         return True

#     def visit_var_declaration_node(self, node:VarDeclarationNode):
#         # Check that the variable being declared has a valid name and type
#         if not isinstance(node.id, str):
#             raise SemanticError("Invalid variable name")
#         if node.type not in ['int', 'float', 'bool']:
#             raise SemanticError("Invalid variable type")

#         # Check that the variable is being initialized with an expression of the correct type
#         if not isinstance(node.expr, AtomicNode):
#             raise SemanticError("Invalid initialization expression")
#         if node.expr.type != node.type and (node.type != 'num' and node.expr.type != 'num'):
#             raise SemanticError(f"Type mismatch in initialization expression {node.expr.type} != {node.type}")

#         # Add the variable to the symbol table
#         self.symbol_table[node.id] = node.type

#     def visit_if_node(self, node:IfNode):
#             # Perform a semantic check on the expression in the if statement
#         if not isinstance(node.expr, AtomicNode):
#             raise SemanticError("Invalid expression in if statement")
#         if node.expr.type != 'bool':
#             raise SemanticError("If statement expression must be of type bool")

#         # Traverse the statements in the if block and perform semantic checks on them
#         for statement in node.statements:
#             statement.accept(self)

#     def visit_else_node(self, node:ElseNode):
#         # Traverse the statements in the else block and perform semantic checks on them
#         for statement in node.statements:
#             statement.accept(self)

#     def visit_assign_node(self, node: AssignNode):
#         node.expr.accept(self)

#     def visit_func_declaration_node(self, node:FuncDeclarationNode):
#         # Check if function has already been defined in the current scope
#         if node.id in self.symbol_table:
#             raise SemanticError(f"Error: Function '{node.id}' already defined in current scope")

#         # Add function to symbol table
#         self.symbol_table[node.id] = node
#         # Visit function body and parameters
#         node.body.accept(self)
#         for param in node.params:
#             param.accept(self)

#     def visit_entry_declaration_node(self, node:EntryDeclarationNode):
#             # Check if function has already been defined in the current scope
#         if node.id in self.symbol_table:
#             raise SemanticError(f"Error: Function '{node.id}' already defined in current scope")

#         # Add function to symbol table
#         self.symbol_table[node.id] = node
#         # Visit function body and parameters
#         for param in node.params:
#             param.accept(self)

#         for st in node.body:
#             st.accept(self)

#     def visit_attr_declaration_node(self, node:AttrDeclarationNode):
#         # Check if variable has already been defined in the current scope
#         if node.id in self.symbol_table:
#             raise SemanticError(f"Error: Variable '{node.id}' already defined in current scope")

#         # Add variable to symbol table
#         self.symbol_table[node.id] = node
#         return True

#     def visit_var_call_node(self, node:VarCallNode):
#         # Check if variable has been defined in current scope
#         if node.id not in self.symbol_table:
#             raise SemanticError(f"Error: Variable '{node.id}' not defined in current scope")

#         # Visit expression being assigned to variable
#         node.expr.accept(self)

#     def visit_atomic_node(self, node:AtomicNode):
#         pass

#     def visit_binary_node(self, node:BinaryNode):
#         # Visit left and right operands
#         node.left.accept(self)
#         node.right.accept(self)

#     def visit_call_node(self, node:CallNode):
#         # Check if function has been defined in current scope
#         if node.id not in self.symbol_table:
#             raise SemanticError(f"Error: Function '{node.id}' not defined in current scope")

#         # Visit function arguments
#         for arg in node.args:
#             arg.accept(self)


#     def visit_constant_num_node(self, node):
#         pass

# class SemanticError(Exception):
#     pass
# import itertools as itl


class SemanticCheckerVisitor(object):
    def __init__(self):
        self.errors = []

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        if scope is None:
            scope = Scope()
        else:
            scope = Scope(parent=scope)

        self.iterations = 1

        for child in node.statements:
            new_scope = self.visit(child, scope)
            if new_scope is not None:
                scope = new_scope

        self.iterations += 1

        for child in node.statements:
            new_scope = self.visit(child, scope)
            if new_scope is not None:
                scope = new_scope

        return self.errors

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope: Scope):
        if self.iterations == 1:
            if scope.is_local_var(node.id):
                self.errors.append(f'Variable {node.id} is used')

        scope.define_variable(node.id)
        self.visit(node.expr, scope)
        return scope

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope):

        if scope.is_func_defined(node.id, len(node.params)):
            if self.iterations == 1:
                self.errors.append(f'Function name {node.id} is used')

        scope.define_function(node.id, len(node.params))
        new_scope = scope.create_child_scope()
        for arg in node.params:
            # print(arg.id, 'arg id')
            scope_update = self.visit(arg, new_scope)
            if scope_update is not None:
                new_scope = scope_update
        # print(new_scope.local_vars,'var')
        for body in node.body:
            scope_update = self.visit(body, new_scope)
            if scope_update is not None:
                new_scope = scope_update

        return scope

    @visitor.when(EntryDeclarationNode)
    def visit(self, node: EntryDeclarationNode, scope: Scope):
        if scope.is_func_defined(node.id, node.params):
            self.errors.append(f'Function name {node.id} is used')

        scope.define_function(node.id, len(node.params))
        scope_copied = Scope()

        for f in scope.local_funcs:
            scope_copied.local_funcs.append(f)
        for v in scope.local_vars:
            scope_copied.local_vars.append(v)

        for arg in node.params:
            # print(arg.id, 'arg id')
            new_scope = self.visit(arg, scope_copied)
            if new_scope is not None:
                scope_copied = new_scope
        # new_scope = scope.create_child_scope()
        for child in node.body:
            self.visit(child, scope_copied)

        return scope

    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode, scope: Scope):
        if not node.lex.isnumeric():
            self.errors.append(f'Value is not Numeric')

        return None

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope):
        if not scope.is_local_var(node.lex):
            self.errors.append(f'Invalid variable {node.lex}')

    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):
        if not scope.is_func_defined(node.id, len(node.args)):
            # print(f'no definida {node.id}')
            # print('local_funcs', scope.local_funcs)
            # if scope.parent:
            # print('enr')
            # print([(f.name, f.params) for f in scope.parent.local_funcs])
            # print('parent funcs', scope.parent.local_funcs)
            if self.iterations == 2:
                self.errors.append(f'Function {node.id} is not defined')

        # print(node.id) #TODO: change to get_local_function_info
        # if len(node.args) != len(scope.get_local_function_info(node.id, node.args)):
        #     self.errors.append(f'Invalid number of arguments of function {node.id}')

        for child in node.args:
            new_scope = self.visit(child, scope)

            if new_scope is not None:
                scope = new_scope

    @visitor.when(BinaryNode)
    def visit(self, node: BinaryNode, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(IfNode)
    def visit(self, node: IfNode, scope: Scope):
        # new_scope = scope.create_child_scope()
        for child in node.statements:
            self.visit(child, scope)

    @visitor.when(ElseNode)
    def visit(self, node: ElseNode, scope: Scope):
        # new_scope = scope.create_child_scope()
        for child in node.statements:
            self.visit(child, scope)

    @visitor.when(VarCallNode)
    def visit(self, node: VarCallNode, scope: Scope):
        # print('estoy en', node.id, scope.local_vars)
        self.visit(node.expr, scope)
        if not scope.is_local_var(node.id):
            self.errors.append(f'Variable {node.id} is not defined')

    @visitor.when(ReturnStatementNode)
    def visit(self, node: ReturnStatementNode, scope: Scope):
        self.visit(node.expr, scope)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, scope: Scope):
        scope.define_variable(node.id)
        return scope
