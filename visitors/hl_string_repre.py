from visitors.visitor import Visitor
from intermediate_ast.high_level_ir_ast import *
import visitors.visitor_d as visitor


class HLReprVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ContractNode)
    def visit(self , node ,tabs = 0):
        ans = '\t' * tabs + 'contract { entrypoint{...} storage{...} code{...}} '
        entrepoint = self.visit(node.entrepoint , tabs + 1)
        storage = self.visit(node.storage , tabs + 1)
        code = self.visit(node.code , tabs + 1)
        return f'{ans}\n{entrepoint}\n{storage}\n{code}'

    @visitor.when(EntrypointsNode)
    def visit(self , node , tabs = 0):
        ans = '\t' * tabs + 'entrypoint  { <id,params> , <id,params> , ... , <id,params> }'
        entrypoints = '\n'.join(self.visit(child , tabs + 1) for child in node.entrypoint_list)
        return f'{ans}\n{entrypoints}'

    @visitor.when(EntryPointDeclarationNode)
    def visit(self , node , tabs = 0):
        ans = '\t' * tabs + f'\\__EntryPointDeclarationNode: {node.id} ({node.params})'
        return f'{ans}'
    
    @visitor.when(StoragesNode)
    def visit(self , node , tabs = 0):
        ans = '\t' * tabs + 'storage { <id,type> , <id,type> , ... , <id,type> }'
        storages = '\n'.join(self.visit(child , tabs + 1) for child in node.storage_list)
        return f'{ans}\n{storages}'

    @visitor.when(StorageDeclarationNode)
    def visit(self , node , tabs = 0):
        ans = '\t' * tabs + f'\\__StorageDeclarationNode: {node.id} : {node.type}'
        return f'{ans}'

    @visitor.when(CodeNode)
    def visit(self , node , tabs = 0):
        ans = '\t' * tabs + 'code { <stat> , <stat> , ... , <stat> }'
        code = '\n'.join(self.visit(child , tabs + 1) for child in node.statements)
        return f'{ans}\n{code}'
    
    @visitor.when(VarDeclarationNode)
    def visit(self , node , tabs = 0):
        ans = '\t' * tabs + f'\\__VarDeclarationNode: let {node.id} = <expr> : {node.type}'
        expr = self.visit(node.expr , tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(IfStatementNode)
    def visit(self , node , tabs = 0):
        ans = '\t' * tabs + 'if <expr> then { <stat> , <stat> , ... , <stat> } else { <stat> , <stat> , ... , <stat> }'
        expr = self.visit(node.expr , tabs + 1)
        then = '\n'.join(self.visit(child , tabs + 1) for child in node.then_clause)
        else_clause = '\n'.join(self.visit(child , tabs + 1) for child in node.else_clause)
        return f'{ans}\n{expr}\n{then}\n{else_clause}'
    
    @visitor.when(WhileDeclarationNode)
    def visit(self , node , tabs = 0):
        ans = '\t' * tabs + 'while <expr> loop { <stat> , <stat> , ... , <stat> }'
        expr = self.visit(node.expr , tabs + 1)
        loop = '\n'.join(self.visit(child , tabs + 1) for child in node.body)
        return f'{ans}\n{expr}\n{loop}'


        

    

    