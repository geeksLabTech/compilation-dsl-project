from enum import Enum
from importlib.metadata import EntryPoint
import visitor
from intermediate_ast import high_level_ir_ast as hl_ir
from parser.tzscript_ast import *
from visitors.scope import Scope


class LevelRepresentatives(Enum):
    '''
    Enum to represent the level of a node in the TzScript ast
    '''
    Program = 0
    EntryPoint = 1
    Function = 2


class Parent:
    def __init__(self, level: LevelRepresentatives, id: str) -> None:
        self.level = level
        self.id = id


class TzScriptToHighLevelIrVisitor:
    '''
    Class to traverse TzScript ast and generate a high level intermediate representation ast for getting close to
    the Michelson language without move away to much from the TzScript language, another intermediate representation
    will be needed. 
    The structure for this intermediate representation is the following:
    contract {
        entrypoints {
            id (params);
            ...
        }
        storage {
            id: type;
            ...
        }
        code {
            if (entrypoint_id) {
                statement
                ...

            }
    }

    The calls to functions in entrypoints are replaced by the corresponding code of each function
    In the case of recursive calls, a RecursiveCallNode is created
    '''

    def __init__(self) -> None:
        self.entrypoints_declarations: list[hl_ir.EntryPointDeclarationNode] = []
        self.storage: list[hl_ir.StorageDeclarationNode] = []
        self.code: list[hl_ir.Node] = []
        self.statements_per_entrypoint_id: dict[str, list[hl_ir.Node]] = {}
        # self.utility_functions: dict[str, hl_ir.UtilityFunctionDefinition] = {}

        # The key is the id assigned for the corresponding entry or function
        self.id_for_new_registed_variables: dict[str, int] = {}
        self.else_node = []

    @visitor.on('node')
    def visit(self, node: Node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, parent=None) -> hl_ir.ContractNode:

        parent = Parent(LevelRepresentatives.Program, 'Program')

        statements = []

        for s in node.statements:
            print('mirame')
            
            statements.extend(self.visit(s, parent))

        

        # entrepoints = hl_ir.Entrpoints(self.entrypoints_declarations)

        # Replace CallNode in functions
        # for id in self.utility_functions:
        #     self.replace_calls_in_function(self.utility_functions[id])

        # Replace CallNode in entrypoints
        # for id in self.statements_per_entrypoint_id:
        #     new_statement_list = []
        #     for statement in self.statements_per_entrypoint_id[id]:
        #         if isinstance(statement, CallNode):
        #             replaced_args: list[hl_ir.VarDeclarationNode] = []
        #             for i in range(len(statement.args)):
        #                 func_attrs = self.utility_functions[statement.id].params
        #                 name = self.create_name_for_new_variable(parent)

        #                 replaced_args.append(hl_ir.VarDeclarationNode(name, func_attrs[i].type, statement.args[i].lex))

        #             # TODO replace all occurrences of old variable name with new variable name in self.utility_functions[statement.id]
        #             new_statement_list.extend(replaced_args)
        #             new_statement_list.extend(self.utility_functions[statement.id].body)
        #         else:
        #             new_statement_list.append(statement)
        #     self.statements_per_entrypoint_id[id] = new_statement_list

        return hl_ir.ContractNode(hl_ir.EntrypointsNode(self.entrypoints_declarations), hl_ir.StoragesNode(self.storage), hl_ir.CodeNode(statements))

    @visitor.when(EntryDeclarationNode)
    def visit(self, node: EntryDeclarationNode, parent: Parent):
        # entrypoint = hl_ir.EntryPointDeclarationNode(
        #     node.id, [hl_ir.AttrDeclarationNode(param.id, param.type) for param in node.params])
        # self.entrypoints_declarations.append(entrypoint)
        # self.statements_per_entrypoint_id[node.id] = []
        self.entrypoints_declarations.append(hl_ir.EntryPointDeclarationNode(node.id, node.params))
        new_parent = Parent(LevelRepresentatives.EntryPoint, node.id)

        statements = []
        for s in node.body:
            print('statements in entry: ', s)
            statements.extend(self.visit(s, new_parent))

        statements = self.merge_if_else_nodes(statements)
        return [hl_ir.IfEntryNode(node.id, statements)]

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, parent: Parent):
        # TODO: handle node.expr
       
        if parent.level == LevelRepresentatives.Program:
            self.storage.append(hl_ir.StorageDeclarationNode(node.id, node.type))
            return []
        elif parent.level == LevelRepresentatives.EntryPoint:
            expr = self.visit(node.expr, parent)
            # self.statements_per_entrypoint_id[parent.id].append(hl_ir.VarDeclarationNode(node.id, node.type, node.expr))
            return expr + [hl_ir.PushVariableNode(node.id, node.type)]

        # elif parent.level == LevelRepresentatives.Function:
        #     self.visit(node.expr,parent)
        #     self.utility_functions[parent.id].body.append(hl_ir.PushVariableNode(node.id, node.type))

    # @visitor.when(FuncDeclarationNode)
    # def visit(self, node: FuncDeclarationNode, parent: Parent):
    #     parent = Parent(LevelRepresentatives.Function, node.id)
    #     params = [hl_ir.AttrDeclarationNode(param.id, param.type) for param in node.params]
    #     self.utility_functions[node.id] = hl_ir.UtilityFunctionDefinition(node.id, params, [])

    #     for s in node.body:
    #         self.visit(s, parent)

    # @visitor.when(CallNode)
    # def visit(self, node: CallNode, parent: Parent):
    #     if node.id == parent.id:
    #         assert parent.level == LevelRepresentatives.Function
    #         # Note: the generated variables for replacing function params help to represent when the recursive function start.
    #         # The start of a function will always start with a generated variable for every param.
    #         self.utility_functions[parent.id].body.append(hl_ir.RecursiveCallNode(node.args))
    #     elif parent.level == LevelRepresentatives.EntryPoint:
    #         self.statements_per_entrypoint_id[parent.id].append(node)

    #     else:
    #         self.utility_functions[parent.id].body.append(node)

    @visitor.when(BinaryNode)
    def visit(self, node: BinaryNode, parent: Parent):
        print('here')
        nodes = []
        nodes.extend(self.visit(node.left, parent))
        nodes.extend(self.visit(node.right, parent))
        if isinstance(node, EqualNode):
            if parent.level == LevelRepresentatives.EntryPoint:
                nodes.append(hl_ir.EqualNode())
            # else:
            #     self.utility_functions[parent.id].body.append(hl_ir.EqualNode())
        elif isinstance(node, InequalityNode):
            if parent.level == LevelRepresentatives.EntryPoint:
                nodes.append(hl_ir.InequalityNode())
            # else:
            #     self.utility_functions[parent.id].body.append(hl_ir.IniquelatyNode())
        elif isinstance(node, LessThanNode):
            if parent.level == LevelRepresentatives.EntryPoint:
                nodes.append(hl_ir.LessThanNode())
            # else:
            #     self.utility_functions[parent.id].body.append(hl_ir.LessThanNode())
        elif isinstance(node, LessThanEqualNode):
            if parent.level == LevelRepresentatives.EntryPoint:
                nodes.append(hl_ir.LessThanEqualNode())
            # else:
            #     self.utility_functions[parent.id].body.append(hl_ir.LessThanEqualNode())
        elif isinstance(node, GreaterThanNode):
            if parent.level == LevelRepresentatives.EntryPoint:
                nodes.append(hl_ir.GreaterThanNode())
            # else:
            #     self.utility_functions[parent.id].body.append(hl_ir.GreaterThanNode())
        elif isinstance(node, GreaterThanEqualNode):
            if parent.level == LevelRepresentatives.EntryPoint:
                nodes.append(hl_ir.GreaterThanEqualNode())
            # else:
            #     self.utility_functions[parent.id].body.append(hl_ir.GreaterThanEqualNode())
        elif isinstance(node, PlusNode):
            if parent.level == LevelRepresentatives.EntryPoint:
                nodes.append(hl_ir.PlusNode())
            # else:
            #     self.utility_functions[parent.id].body.append(hl_ir.PlusNode())
        elif isinstance(node, MinusNode):
            if parent.level == LevelRepresentatives.EntryPoint:
                nodes.append(hl_ir.MinusNode())
            # else:
            #     self.utility_functions[parent.id].body.append(hl_ir.MinusNode())
        elif isinstance(node, StarNode):
            if parent.level == LevelRepresentatives.EntryPoint:
                nodes.append(hl_ir.StarNode())
            # else:
            #     self.utility_functions[parent.id].body.append(hl_ir.StarNode())
        elif isinstance(node, DivNode):
            if parent.level == LevelRepresentatives.EntryPoint:
                nodes.append(hl_ir.DivNode())
            # else:
            #     self.utility_functions[parent.id].body.append(hl_ir.DivNode())
        print('nodos donde suma')
        return nodes
    # @visitor.when(ReturnStatementNode)
    # def visit(self, node: ReturnStatementNode, parent: Parent):
    #     self.visit(node.expr, parent)

    @visitor.when(IfNode)
    def visit(self, node: IfNode, parent: Parent):
        statements = []

        expr = self.visit(node.expr, parent)
        
        for s in node.statements:
            statements.extend(self.visit(s, parent))
        statements = self.merge_if_else_nodes(statements)
        return [IfNode(expr, statements)]

    @visitor.when(ElseNode)
    def visit(self, node: ElseNode, parent: Parent):
        statements = []
        for child in node.statements:
            statements.extend(self.visit(child, parent))

        statements = self.merge_if_else_nodes(statements)
        return [ElseNode(statements)]

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, parent: Parent):
        statements = []
        print('statement in while')
        expr = self.visit(node.expr, parent)
        
        for s in node.statements:
            
            statements.extend(self.visit(s, parent))

        statements = self.merge_if_else_nodes(statements)
        return [hl_ir.WhileDeclarationNode(expr, statements)]
    
    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode, parent: Parent):
        return [hl_ir.PushValueNode(node.lex, node.type)]

    @visitor.when(ConstantStringNode)
    def visit(self, node: ConstantNumNode, parent: Parent):
        return [hl_ir.PushValueNode(node.lex, node.type)]

    @visitor.when(VarCallNode)
    def visit(self, node: VarCallNode, parent: Parent):
        expr = self.visit(node.expr, parent)
        return expr + [hl_ir.PushVariableNode(node.id, '')]

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, parent: Parent):
        return [hl_ir.GetToTopNode(node.lex)]

    # def replace_calls_in_function(self, function: hl_ir.UtilityFunctionDefinition):
    #     statements = []
    #     for i, statement in enumerate(function.body):
    #         if isinstance(statement, CallNode):
    #             resolved_function_body = self.replace_calls_in_function(self.utility_functions[statement.id])
    #             replaced_args: list[hl_ir.VarDeclarationNode] = []
    #             parent = Parent(LevelRepresentatives.Function, statement.id)
    #             for i in range(len(statement.args)):
    #                 func_attrs = self.utility_functions[statement.id].params
    #                 name = self.create_name_for_new_variable(parent)

    #                 replaced_args.append(hl_ir.VarDeclarationNode(name, func_attrs[i].type, statement.args[i].lex))

    #             # TODO replace all occurrences of old variable name with new variable name in self.utility_functions[statement.id]
    #             resolved_function_body = replaced_args + resolved_function_body
    #             statements.extend(resolved_function_body)
    #         else:
    #             statements.append(statement)

    #     self.utility_functions[function.id].body = statements
    #     return statements

    def create_name_for_new_variable(self, parent: Parent):
        if parent.level == LevelRepresentatives.Function:
            id = f'function_{parent.id}'
        else:
            id = f'entry_{parent.id}'

        if not id in self.id_for_new_registed_variables:
            self.id_for_new_registed_variables[id] = 0
        else:
            self.id_for_new_registed_variables[id] += 1

        return f'_generated_var_{id}_{self.id_for_new_registed_variables[id]}'

    def merge_if_else_nodes(self, statements):
        new_statements = []
        for i, statement in enumerate(statements):
            if isinstance(statement, IfNode) and i+1 < len(statements):
                if isinstance(statements[i+1], ElseNode):
                    new_statements.append(hl_ir.IfStatementNode(statement.expr, statement.statements, statements[i+1].statements))
                else:
                    new_statements.append(hl_ir.IfStatementNode(statement.expr, statement.statements, []))
            else:
                new_statements.append(statement)

        return new_statements

    # def replace_variable_name(self, node, old_name, new_name):
    #     for x in node.body:
