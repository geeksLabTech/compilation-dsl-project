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

    @visitor.when(IfEntryNode)
    def visit(self, node: IfEntryNode, tabs = 0):
        ans = '\t' * tabs + f'\\__IfEntryNode: if {node.entry_id} then '
        print('If entry:', node.statements)
        # for child in node.statements:
        #     f = self.visit(child, tabs+1)
        #     print(f'f: {f}')
        #     print(f'child: {child}')
        #     try:
        #         print(child.id)
        #         print(child.type)
        #         print('paso')
        #     except:
        #         print('aaaaaaaa')
        #     print(f'child type: {type(child)} {isinstance(child, PushVariableNode)}')
        
        # print()
        # x=[self.visit(child, tabs + 1) for child in node.statements]
        # print('x', x)
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        return f'{ans}\n{statements}'

    @visitor.when(PushValueNode)
    def visit(self, node: PushValueNode, tabs = 0):
        ans = '\t' * tabs + f'\\__PushValueNode: push {node.type} {node.value}'
        return f'{ans}'

    @visitor.when(PushVariableNode)
    def visit(self, node: PushVariableNode, tabs = 0):
        
        ans = '\t' * tabs + f'\\__PushVariableNode: push {node.type} {node.id}'
        print('ans de variable', node.type, node.id)
        return f'{ans}'

    @visitor.when(GetToTopNode)
    def visit(self, node: GetToTopNode, tabs=0):
        ans = '\t' * tabs + f'\\__GetToTopNode: get {node.id}'
        return f'{ans}'

    @visitor.when(OperationNode)
    def visit(self, node: OperationNode, tabs = 0):
        print('operacion')
        ans = '\t' * tabs + f'\\__ {node.__class__.__name__}'
        print('ans deplus', ans)
        return f'{ans}'

        

    

    