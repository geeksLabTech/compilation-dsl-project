from parser.tzscript_ast import *


class SemanticCheckVisitor:
    def __init__(self):
        self.symbol_table = {}

    def visit_program(self, node:ProgramNode):
        # Traverse the program node and all of its child nodes, performing semantic checks
        for statement in node.statements:
            statement.accept(self)
        return True

    def visit_var_declaration_node(self, node:VarDeclarationNode):
        # Check that the variable being declared has a valid name and type
        if not isinstance(node.id, str):
            raise SemanticError("Invalid variable name")
        if node.type not in ['int', 'float', 'bool']:
            raise SemanticError("Invalid variable type")

        # Check that the variable is being initialized with an expression of the correct type
        if not isinstance(node.expr, AtomicNode):
            raise SemanticError("Invalid initialization expression")
        if node.expr.type != node.type and (node.type != 'num' and node.expr.type != 'num'):
            raise SemanticError(f"Type mismatch in initialization expression {node.expr.type} != {node.type}")

        # Add the variable to the symbol table
        self.symbol_table[node.id] = node.type

    def visit_if_node(self, node:IfNode):
            # Perform a semantic check on the expression in the if statement
        if not isinstance(node.expr, AtomicNode):
            raise SemanticError("Invalid expression in if statement")
        if node.expr.type != 'bool':
            raise SemanticError("If statement expression must be of type bool")

        # Traverse the statements in the if block and perform semantic checks on them
        for statement in node.statements:
            statement.accept(self)

    def visit_else_node(self, node:ElseNode):
        # Traverse the statements in the else block and perform semantic checks on them
        for statement in node.statements:
            statement.accept(self)

    def visit_assign_node(self, node: AssignNode):
        node.expr.accept(self)

    def visit_func_declaration_node(self, node:FuncDeclarationNode):
        # Check if function has already been defined in the current scope
        if node.id in self.symbol_table:
            raise SemanticError(f"Error: Function '{node.id}' already defined in current scope")

        # Add function to symbol table
        self.symbol_table[node.id] = node
        # Visit function body and parameters
        node.body.accept(self)
        for param in node.params:
            param.accept(self)
    
    def visit_entry_declaration_node(self, node:EntryDeclarationNode):
            # Check if function has already been defined in the current scope
        if node.id in self.symbol_table:
            raise SemanticError(f"Error: Function '{node.id}' already defined in current scope")

        # Add function to symbol table
        self.symbol_table[node.id] = node
        # Visit function body and parameters
        for param in node.params:
            param.accept(self)

        for st in node.body:
            st.accept(self)
            
    def visit_attr_declaration_node(self, node:AttrDeclarationNode):
        # Check if variable has already been defined in the current scope
        if node.id in self.symbol_table:
            raise SemanticError(f"Error: Variable '{node.id}' already defined in current scope")

        # Add variable to symbol table
        self.symbol_table[node.id] = node
        return True

    def visit_var_call_node(self, node:VarCallNode):
        # Check if variable has been defined in current scope
        if node.id not in self.symbol_table:
            raise SemanticError(f"Error: Variable '{node.id}' not defined in current scope")

        # Visit expression being assigned to variable
        node.expr.accept(self)

    def visit_atomic_node(self, node:AtomicNode):
        pass

    def visit_binary_node(self, node:BinaryNode):
        # Visit left and right operands
        node.left.accept(self)
        node.right.accept(self)

    def visit_call_node(self, node:CallNode):
        # Check if function has been defined in current scope
        if node.id not in self.symbol_table:
            raise SemanticError(f"Error: Function '{node.id}' not defined in current scope")
            
        # Visit function arguments
        for arg in node.args:
            arg.accept(self)
        

    def visit_constant_num_node(self, node):
        pass
    
class SemanticError(Exception):
    pass