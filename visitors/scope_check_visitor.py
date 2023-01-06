from visitors.visitor import Visitor

class ScopeCheckVisitor(Visitor):
    def __init__(self):
        self.scopes = [{}]  # stack of scopes, with the top of the stack representing the current scope

    def visit_program(self, node):
        # add the parameters to the current scope
        self.scopes[-1].update({param.id: param for param in node.params})
        # visit the statements in the program
        for statement in node.statements:
            statement.accept(self)

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

    def visit_attr_declaraion_node(self, node):
        # add the attribute to the current scope
        self.scopes[-1][node.id] = node

class ScopeError(Exception):
    pass