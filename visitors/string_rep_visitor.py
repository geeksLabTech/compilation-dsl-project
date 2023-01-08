from visitors.visitor import Visitor
from parser.tzscript_ast import *
import visitors.visitor_d as visitor

# class StringReprVisitor(Visitor):
#     def __init__(self, tabs):
#         self.result = ""  # string representation of the AST
#         self.tabs = 0
#         

#     def visit_program(self, node: ProgramNode):
#         self.result += f"program {node.idx}({', '.join(param.id for param in node.params)}):\n"
#         self.Lia = '\t' * self.tabs + f'\\__ProgramNode [<stat>; ... <stat>;]'
#         for statement in node.statements:
#             statement.accept(self)

#     def visit_if_node(self, node):
#         self.result += "    if "
#         node.expr.accept(self)
#         self.result += ":\n"
#         for statement in node.statements:
#             statement.accept(self)

#     def visit_else_node(self, node):
#         self.result += "    else:\n"
#         for statement in node.statements:
#             statement.accept(self)

#     def visit_var_declaration_node(self, node):
#         self.result += f"    {node.type} {node.id} = "
#         node.expr.accept(self)
#         self.result += "\n"
    
#     def visit_entry_declaration_node(self, node):
#         # self.result += f"Entry Declaration Node: \n"
#         self.result += f"{node.id}("
#         for n in node.params:
#             n.accept(self) 
#         self.result += '):\n'
#         for st in node.body:
#             self.result += '\t'
#             st.accept(self)
#         self.result += '\n'

#     def visit_assign_node(self, node):
#         self.result += f"    {node.id} = "
#         node.expr.accept(self)
#         self.result += "\n"

#     def visit_func_declaration_node(self, node):
#         self.result += f"    def {node.id}({', '.join(param.id for param in node.params)})"
#         if node.type:
#             self.result += f" -> {node.type}"
#         self.result += ":\n"
#         for statement in node.body:
#             statement.accept(self)

#     def visit_attr_declaration_node(self, node):
#         self.result += f" {node.type} {node.id}"

#     def visit_atomic_node(self, node):
#         self.result += f" {node.lex}\n"
        
        
#     def visit_constant_num_node(self, node):
#         self.result += f" {node.lex}\n"
        
#     def visit_var_call_node(self, node):
#         self.result += f"{node.id} = "
#         node.expr.accept(self)

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        # print(type(node), 'tipo')
        # print(node.params)
        sparams = ''
        for param in node.params:
            string_paramt = param.id+' '+':' +' ' + param.type
            sparams = sparams.join(string_paramt)
        ans = '\t' * tabs + f'\\__ProgramNode: contract node.idx({sparams}) [<stat>; ... <stat>;]'
        params = '\n'.join(self.visit(param, tabs + 1 ) for param in node.params)
        statements = '\n'.join(self.visit(child, tabs + 2) for child in node.statements)
        return f'{ans}\n{params}\n{statements}'
    
    # @visitor.when(PrintNode)
    # def visit(self, node, tabs=0):
    #     ans = '\t' * tabs + f'\\__PrintNode <expr>'
    #     expr = self.visit(node.expr, tabs + 1)
    #     return f'{ans}\n{expr}'
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VarDeclarationNode: let {node.id} = <expr> : {node.type}'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(IfNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__IfNode: if <expr> then [<stat>; ... <stat>;]'
        expr = self.visit(node.expr, tabs + 1)
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        return f'{ans}\n{expr}\n{statements}'
    
    @visitor.when(ElseNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ElseNode: else [<stat>; ... <stat>;]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        return f'{ans}\n{statements}'

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tabs=0):
        # params = ', '.join(node.params)
        sparams = ''
        for param in node.params:
            string_paramt = param.id+' '+':' +' ' + param.type
            sparams = sparams.join(string_paramt)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: def {node.id}({sparams}) : {node.type}'
        body = self.visit(node.body, tabs + 2)
        return f'{ans}\n{sparam}\n{body}'

    @visitor.when(EntryDeclarationNode)
    def visit(self, node, tabs=0):
        sparams = ''
        for param in node.params:
            string_paramt = param.id+' '+':' +' ' + param.type
            sparams = sparams.join(string_paramt)
        # params = ', '.join(str(node.params))
        ans = '\t' * tabs + f'\\__EntryDeclarationNode: Entry {node.id}({sparams})'
        params = '\n'.join(self.visit(param, tabs + 1 ) for param in node.params)
        # print(node.body, 'body')

        body = '\n'.join(self.visit(child, tabs + 2) for child in node.body)
        # print(self.visit(node.body, tabs + 2), 'body')

        return f'{ans}\n{params}\n{body}'
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__AttrDeclarationNode: {node.id} : {node.type}'

    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
    
    # @visitor.when(ExpressionNode)
    # def visit(self, node, tabs=0):
    #     return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
    
    @visitor.when(CallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__CallNode: {node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'

    @visitor.when(VarCallNode)
    def visit(self, node, tabs=0):
        # print('llega')
        ans = '\t' * tabs + f'\\__VarCallNode: {node.id} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'