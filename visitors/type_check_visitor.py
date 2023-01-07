from parser.tzscript_ast import *
from visitors.visitor import Visitor

class TypeCheckVisitor(Visitor):
    def __init__(self):
        self.symbol_table = {}  # symbol table to store variable and function types
    
    def visit_program(self, node: ProgramNode):
        # check types for program node
        for statement in node.statements:
            statement.accept(self)
    
    def visit_if_node(self, node: IfNode):
        # check types for if node
        # check that the expression is of a boolean type
        if not self.is_boolean_type(node.expr.type):
            raise TypeError("If statement expression must be of type boolean")
        for statement in node.statements:
            statement.accept(self)
    
    def visit_else_node(self, node: ElseNode):
        # check types for else node
        for statement in node.statements:
            statement.accept(self)
    
    def visit_var_declaration_node(self, node: VarDeclarationNode):
        # check types for variable declaration node
        # check that the type of the expression is compatible with the declared type
        if not self.is_compatible_type(node.expr.type, node.type):
            raise TypeError(f"Incompatible types in variable declaration: expected {node.type}, got {node.expr.type}")
        self.symbol_table[node.id] = node.type
    
    def visit_assign_node(self, node: AssignNode):
        # check types for assignment node
        # check that the variable being assigned to is in the symbol table
        if node.id not in self.symbol_table:
            raise NameError(f"Variable {node.id} not defined")
        # check that the type of the expression is compatible with the variable's type
        if not self.is_compatible_type(node.expr.type, self.symbol_table[node.id]):
            raise TypeError(f"Incompatible types in assignment: expected {self.symbol_table[node.id]}, got {node.expr.type}")
    
    def visit_func_declaration_node(self, node: FuncDeclarationNode):
        # check types for function declaration node
        # add function to symbol table
        self.symbol_table[node.id] = node.type
        # check types for function body
        for statement in node.body:
            statement.accept(self)
        
    def visit_var_call_node(self, node: VarCallNode):
        pass
    
    def visit_constant_num_node(self, node: ConstantNumNode):
        pass
    
    def visit_entry_declaration_node(self, node: EntryDeclarationNode):
        for p in node.params:
            p.accept(self)
        for st in node.body:
            st.accept(self)
    
    def visit_attr_declaraion_node(self, node: AttrDeclarationNode):
        # check types for attribute declaration node
        self.symbol_table[node.id] = node.type
    
    def visit_atomic_node(self, node: AtomicNode):
        # check types for atomic node
        pass
    
    def visit_binary_node(self, node: BinaryNode):
        # check types for binary node
        # check that operand types are compatible with the operation
        if not self.is_compatible_type(node.left.type, node.right.type):
            raise TypeError(f"Incompatible types in binary operation: {node.left.type} and {node.right.type}")
    
    def is_boolean_type(self, expr):
        if type(expr) is bool:
            return True
    
    def is_compatible_type(self, expr_type, node_type):
        
        if expr_type == node_type:
            return True
        if node_type == 'num' and (expr_type == 'nat' or expr_type == 'int'):
            return True
        if expr_type == 'num' and (node_type == 'nat' or node_type == 'int'):
            return True
        # TODO get compatibility list
        return False