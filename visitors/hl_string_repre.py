from visitors.visitor import Visitor
from intermediate_ast.high_level_ir_ast import *
import visitors.visitor_d as visitor


class HLReprVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ContractNode)
    def visit(self , node: ContractNode ,tabs = 0):
        ans = '\t' * tabs + 'contract { entrypoint{...} storage{...} code{...}} '
        entrypoints = self.visit(node.entrypoints , tabs + 1)
        storage = self.visit(node.storage , tabs + 1)
        code = self.visit(node.code , tabs + 1)
        return f'{ans}\n{entrypoints}\n{storage}\n{code}'

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
    def visit(self , node: CodeNode , tabs = 0):
        ans = '\t' * tabs + 'code { <stat> , <stat> , ... , <stat> }'
        print('los: ', node.statements)
        code = '\n'.join(self.visit(child , tabs + 1) for child in node.statements)
        return f'{ans}\n{code}'
    
    # @visitor.when(VarDeclarationNode)
    # def visit(self , node , tabs = 0):
    #     ans = '\t' * tabs + f'\\__VarDeclarationNode: let {node.id} = <expr> : {node.type}'
    #     expr = self.visit(node.expr , tabs + 1)
    #     return f'{ans}\n{expr}'

    @visitor.when(IfStatementNode)
    def visit(self , node: IfStatementNode , tabs = 0):
        ans = '\t' * tabs + 'if <expr> then { <stat> , <stat> , ... , <stat> } else { <stat> , <stat> , ... , <stat> }'
        # print('expresion if', node.expr)
        expr = '\n'.join(self.visit(child, tabs + 1) for child in node.expr)
        then = '\n'.join(self.visit(child , tabs + 2) for child in node.then_clause)
        then = 'then {' + then + ' }'
        else_clause = '\n'.join(self.visit(child , tabs + 2) for child in node.else_clause)
        else_clause = 'else {' + else_clause + ' }'
        return f'{ans}\n{expr}\n{then}\n{else_clause}'
    
    @visitor.when(WhileDeclarationNode)
    def visit(self , node , tabs = 0):
        ans = '\t' * tabs + 'while <expr> loop { <stat> , <stat> , ... , <stat> }'
        expr = self.visit(node.expr , tabs + 1)
        loop = '\n'.join(self.visit(child , tabs + 1) for child in node.body)
        return f'{ans}\n{expr}\n{loop}'

    @visitor.when(IfEntryNode)
    def visit(self, node: IfEntryNode, tabs = 0):
        ans = '\t' * tabs + f'\\__IfEntryNode: if {node.entry_id} then '
        print('mmm', node.statements)
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        return f'{ans}\n{statements}'

    @visitor.when(PushValueNode)
    def visit(self, node: PushValueNode, tabs = 0):
        ans = '\t' * tabs + f'\\__PushValueNode: push {node.type} {node.value}'
        return f'{ans}'

    @visitor.when(PushVariableNode)
    def visit(self, node: PushVariableNode, tabs = 0):
        ans = '\t' * tabs + f'\\__PushVariableNode: push {node.type} {node.id}'
        return f'{ans}'

    @visitor.when(ReplaceVariableNode)
    def visit(self, node: ReplaceVariableNode, tabs=0):
        ans = '\t' * tabs + f'\\__ReplaceVariableNode: {node.id}'
        return f'{ans}'

    @visitor.when(GetToTopNode)
    def visit(self, node: GetToTopNode, tabs=0):
        ans = '\t' * tabs + f'\\__GetToTopNode: get {node.id}'
        return f'{ans}'

    @visitor.when(OperationNode)
    def visit(self, node: OperationNode, tabs = 0):
        print('operation node: ', node)
        ans = '\t' * tabs + f'\\__ {node.__class__.__name__}'
        return f'{ans}'

        

    

    