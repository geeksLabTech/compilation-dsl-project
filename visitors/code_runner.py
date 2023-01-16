from parser.tzscript_ast import *
from visitor import when
import visitors.visitor_d as visitor


class ScopeContext:
    def __init__(self) -> None:
        self.variables = {}
        self.functions = {}


class CodeRunnerVisitor(object):
    def __init__(self) -> None:
        self.scopes = []
        self.current_scope = 0
        self.go_else = False

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.go_else = False
        self.scopes.append(ScopeContext())

        # for p in node.params:
        #     self.scopes[self.current_scope].variables[str(p.idx)] = {'type':p.typex, 'value': None}

        for st in node.statements:
            self.visit(st)

        self.scopes.pop()

    @visitor.when(IfNode)
    def visit(self, node: IfNode):
        self.go_else = False
        if self.visit(node.expr):
            self.current_scope += 1
            self.scopes.append(ScopeContext())

            for st in node.statements:
                self.visit(st)

            self.scopes.pop()
            self.current_scope -= 1
        else:
            self.go_else = True

    @visitor.when(ElseNode)
    def visit(self, node: ElseNode):
        if self.go_else is True:
            self.go_else = False

            self.current_scope += 1
            self.scopes.append(ScopeContext())

            for st in node.statements:
                self.visit(st)

            self.scopes.pop()
            self.current_scope -= 1

    @visitor.when(ReturnStatementNode)
    def visit(self, node: ReturnStatementNode):
        st = self.visit(node.expr)
        return st

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode):
        self.scopes[self.current_scope].variables[node.id] = {
            'type': node.type, 'value': self.visit(node.expr)}

    # TODO look for the var bottom up
    @visitor.when(AssignNode)
    def visit(self, node: AssignNode):
        for i in range(0, self.current_scope):
            if node.id in self.scopes[self.current_scope-i].variables:
                self.scopes[self.current_scope-i].variables[node.id]['value'] = self.visit(
                    node.expr)
                break

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode):
        self.scopes[0].functions[node.id] = {"func": node, "type": node.type}

    @visitor.when(EntryDeclarationNode)
    def visit(self, node: EntryDeclarationNode):
        self.scopes[0].functions[node.id] = {"func": node, "type": None}

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode):
        self.scopes.append(ScopeContext())
        self.current_scope += 1

        cond = self.visit(node.expr)

        while(cond):
            for st in node.statements:
                self.visit(st)

            cond = self.visit(node.expr)

        self.current_scope -= 1
        self.scopes.pop()

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode):
        self.scopes[self.current_scope].variables[node.id] = {
            'type': node.type, 'value': None}

    @visitor.when(AtomicNode)
    @visitor.when(ConstantStringNode)
    def visit(self, node: AtomicNode):
        return node.lex

    @visitor.when(ConstantNumNode)
    def visit(self, node: AtomicNode):
        return int(node.lex)

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        return l+r

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        return l-r

    @visitor.when(DivNode)
    def visit(self, node: DivNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        return l/r

    @visitor.when(StarNode)
    def visit(self, node: StarNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        return l*r

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        return l == r

    @visitor.when(InequalityNode)
    def visit(self, node: InequalityNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        return l != r

    @visitor.when(GreaterThanEqualNode)
    def visit(self, node: GreaterThanEqualNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        return l >= r

    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        return l > r

    @visitor.when(LessThanEqualNode)
    def visit(self, node: LessThanEqualNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        return l <= r

    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        return l < r

    @visitor.when(CallNode)
    def visit(self, node: CallNode):
        self.scopes.append(ScopeContext())
        self.current_scope += 1

        fun: CallNode = node.id

        fun_node: FuncDeclarationNode = self.scopes[0].functions[fun]

        for p in fun_node.params:
            self.visit(p)

        idx = 0
        for p in self.scopes[self.current_scope].variables:
            self.scopes[self.current_scope].variables[p] = node.args[idx]
            idx += 1

        for st in fun_node.body:
            self.visit(st)

        self.scopes.pop()
        self.current_scope -= 1
