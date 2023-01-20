
from parser.tzscript_ast import *
import visitors.visitor as visitor


class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, tabs=0):
        ans = '\t' * tabs + \
            f'\\__ProgramNode: contract node.idx (param,...,param) [<stat>; ... <stat>;]'
        params = '\n'.join(self.visit(param, tabs + 1)
                           for param in node.params)
        statements = '\n'.join(self.visit(child, tabs + 2)
                               for child in node.statements)

        return f'{ans}\n{params}\n{statements}'

    @visitor.when(DeclarationStorageNode)
    def visit(self,node: DeclarationStorageNode,tabs = 0):
        ans = '\t' * tabs + f'\\__DeclarationStorageNode: {node.id} : {node.type.name.value}'
        return f'{ans}'
        
    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, tabs=0):
        ans = '\t' * tabs + \
            f'\\__VarDeclarationNode: let {node.id} = <expr> : {node.type.name.value}'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(IfNode)
    def visit(self, node: IfNode, tabs=0):
        ans = '\t' * tabs + f'\\__IfNode: if <expr> then [<stat>; ... <stat>;] else [<stat>; ... <stat>;]'
        expr = self.visit(node.expr, tabs + 1)
        then_statements = '\n'.join(self.visit(child, tabs + 1) for child in node.then_statements)
        else_statements = '\n'.join(self.visit(child,tabs + 1) for child in node.else_statements)
        return f'{ans}\n{expr}\n then\n{then_statements}\n else\n{else_statements}'


    @visitor.when(ReturnStatementNode)
    def visit(self, node: ReturnStatementNode, tabs=0):
        ans = '\t' * tabs + f'\\__ReturnStatementNode: return <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, tabs=0):
        ans = '\t' * tabs + \
            f'\\__FuncDeclarationNode: func {node.id} (param,...,param) [<stat>; ... <stat>;]'
        param = '\n'.join(self.visit(child,tabs+1) for child in node.params)
        body = '\n'.join(self.visit(child, tabs + 1) for child in node.body)
        return f'{ans}\n{param}\n{body}'

    @visitor.when(EntryDeclarationNode)
    def visit(self, node: EntryDeclarationNode, tabs=0):
        ans = '\t' * tabs + \
            f'\\__EntryDeclarationNode: Entry {node.id} (param,...,param)[<stat>; ... <stat>;]'
        params = '\n'.join(self.visit(param, tabs + 1)
                           for param in node.params)

        body = '\n'.join(self.visit(child, tabs + 2) for child in node.body)

        return f'{ans}\n{params}\n{body}'

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, tabs=0):
        return '\t' * tabs + f'\\__AttrDeclarationNode: {node.id} : {node.type.name.value}'

    @visitor.when(AtomicNode)
    def visit(self, node: AtomicNode, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

    @visitor.when(BinaryNode)
    def visit(self, node: BinaryNode, tabs=0):
        ans = '\t' * tabs + f'\\__ {node.__class__.__name__}'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(CallNode)
    def visit(self, node: CallNode, tabs=0):
        ans = '\t' * tabs + f'\\__CallNode: {node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'

    @visitor.when(VarCallNode)
    def visit(self, node: VarCallNode, tabs=0):
        ans = '\t' * tabs + f'\\__VarCallNode: {node.id} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, tabs=0):
        ans = '\t' * tabs + \
            f'\\__WhileNode: while <expr> then [<stat>; ... <stat>;]'
        expr = self.visit(node.expr, tabs + 1)
        statements = '\n'.join(self.visit(child, tabs + 1)
                               for child in node.statements)
        return f'{ans}\n{expr}\n{statements}'

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, tabs=0):
        return '\t' * tabs + f'\\__VariableNode: {node.lex}'
