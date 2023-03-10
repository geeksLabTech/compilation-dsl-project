

from base_ast import Node, AtomicNode, UnaryNode, BinaryNode



class DeclarationNode(Node):
    pass

class ExpressionNode(Node):
    pass

class OperationNode(Node):
    pass
    
class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex):
        self.id = idx
        self.type = typex
        
class PushVariableNode(Node):
    def __init__(self, idx, typex):
        self.id = idx
        self.type = typex

class PushValueNode(Node):
    def __init__(self, value, type) -> None:
        self.value = value
        self.type = type

class ReplaceVariableNode(Node):
    def __init__(self, id) -> None:
        self.id = id

class StorageDeclarationNode(DeclarationNode):
    def __init__(self, id, typex):
        self.id = id
        self.type = typex

class StoragesNode(DeclarationNode):
    def __init__(self, storage_list : list[StorageDeclarationNode]):
        self.storage_list = storage_list

class EntryPointDeclarationNode(DeclarationNode):
    def __init__(self, idx, params: list[AttrDeclarationNode]):
        self.id = idx
        self.params = params

class EntrypointsNode(DeclarationNode):
    def __init__(self, entrypoint_list : list[EntryPointDeclarationNode]):
        self.entrypoint_list = entrypoint_list

class UtilityFunctionDefinition(Node):
    def __init__(self, idx, params, body) -> None:
        self.id = idx
        self.params = params
        self.body = body

class CodeNode(Node):
    def __init__(self, statements):
        self.statements = statements

class ContractNode(Node):
    def __init__(self, entrypoints: EntrypointsNode, storage: StoragesNode, code: CodeNode):
        self.entrypoints = entrypoints
        self.storage = storage
        self.code = code

class IfEntryNode(Node):
    def __init__(self, entry_id, statements) -> None:
        self.entry_id = entry_id
        self.statements = statements

class RecursiveFunctionNode(Node):
    def __init__(self, params, body):
        self.params = params
        self.body = body

class RecursiveCallNode(Node):
    def __init__(self, params):
        self.params = params


class IfStatementNode(Node):
    def __init__(self, expr, then_clause, else_clause) -> None:
        self.expr = expr
        self.then_clause = then_clause
        self.else_clause = else_clause

class ReturnNode(ExpressionNode):
    def __init__(self, expr) -> None:
        self.expr = expr

class VarDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr):
        self.id = idx
        self.type = typex
        self.expr = expr

class GetToTopNode(Node):
    def __init__(self, id) -> None:
        self.id = id

class TrueNode(ExpressionNode):
    pass

class FalseNode(ExpressionNode):
    pass

class ConstantNumNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.type = 'num'


class VarCallNode(DeclarationNode):
    def __init__(self, idx, expr) -> None:
        self.id = idx
        self.expr = expr

class WhileDeclarationNode(DeclarationNode):
    def __init__(self, expr, body) -> None:
        self.expr = expr
        self.body = body

class VariableNode(AtomicNode):
    pass

class PlusNode(OperationNode):
    def __init__(self):
        pass

class MinusNode(OperationNode):
    def __init__(self):
        pass
       

class StarNode(OperationNode):
    def __init__(self):
        pass

class DivNode(OperationNode):
    def __init__(self):
        pass

class EqualNode(OperationNode):
    def __init__(self):
        pass

class InequalityNode(OperationNode):
    def __init__(self):
        pass

class LessThanNode(OperationNode):
   def __init__(self):
        pass

class LessThanEqualNode(OperationNode):
    def __init__(self):
        pass

class GreaterThanNode(OperationNode):
    def __init__(self):
        pass

class GreaterThanEqualNode(OperationNode):
    def __init__(self):
        pass
