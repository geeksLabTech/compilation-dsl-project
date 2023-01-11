from visitors.visitor import Visitor


class ScopeCheckVisitor(Visitor):
    def __init__(self):
        # stack of scopes, with the top of the stack representing the current scope
        self.scopes = [{}]

    def visit_program(self, node):
        # add the parameters to the current scope
        self.scopes[-1].update({param.id: param for param in node.params})
        # visit the statements in the program
        for statement in node.statements:
            statement.accept(self)
        return True

    def visit_if_node(self, node):
        # visit the expression in the if statement
        node.expr.accept(self)
        # create a new scope for the if statement
        self.scopes.append({})
        # visit the statements in the if block
        for statement in node.statements:
            statement.accept(self)
        # remove the scope for the if block
        self.scopes.pop()

    def visit_else_node(self, node):
        # create a new scope for the else block
        self.scopes.append({})
        # visit the statements in the else block
        for statement in node.statements:
            statement.accept(self)
        # remove the scope for the else block
        self.scopes.pop()

    def visit_var_declaration_node(self, node):
        # visit the expression being assigned to the variable
        node.expr.accept(self)
        # add the variable to the current scope
        self.scopes[-1][node.id] = node

    def visit_assign_node(self, node):
        # visit the expression being assigned to the variable
        node.expr.accept(self)
        # check if the variable has been declared in the current scope or any parent scopes
        for scope in reversed(self.scopes):
            if node.id in scope:
                break
        else:
            # if the variable has not been declared, raise an error
            raise ScopeError(f"Variable '{node.id}' has not been declared")

    def visit_func_declaration_node(self, node):
        # add the function to the current scope
        self.scopes[-1][node.id] = node
        # create a new scope for the function
        self.scopes.append({})
        # add the parameters to the function scope
        self.scopes[-1].update({param.id: param for param in node.params})
        # visit the statements in the function body
        for statement in node.body:
            statement.accept(self)
        # remove the scope for the function
        self.scopes.pop()

    def visit_call_node(self, node):
        pass

    def visit_arith_node(self, node, oper):
        node.left.accept(self)
        node.right.accept(self)

    def visit_return_node(self, node):
        node.expr.accept(self)
    
    def visit_variable_node(self, node):
        if not node.id in self.scopes[-1]:
            self.errors.append()

    def visit_attr_declaration_node(self, node):
        # add the attribute to the current scope
        self.scopes[-1][node.id] = node

    def visit_var_call_node(self, node):
        # Look up the symbol in the list of scopes to see if it has been defined
        found = False
        for scope in self.scopes:
            if node.id in scope:
                found = True
                break
        if not found:
            raise ScopeError("Undefined symbol '{}'".format(node.id))

    def visit_entry_declaration_node(self, node):
        # Add a new scope to the list, containing the symbols defined in the function parameters and body
        scope_symbols = {}
        for param in node.params:
            scope_symbols[param.id] = param.type
        self.scopes.append(scope_symbols)

        # Traverse the body of the function and perform a scope check on each node
        for statement in node.body:
            statement.accept(self)

    def visit_constant_num_node(self, node):
        pass


class ScopeError(Exception):
    pass
