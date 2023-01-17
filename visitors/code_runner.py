from parser.tzscript_ast import *
from visitor import when
import visitors.visitor_d as visitor


class ScopeContext:
    def __init__(self) -> None:
        self.variables = {}
        self.functions = {}
        self.entry = {}


class CodeRunnerVisitor(object):
    def __init__(self) -> None:
        self.scopes = []
        self.current_scope = 0
        self.go_else = False
        self.scope_bound = False

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
            # print(self.scopes)
            self.visit(st)

        if len(self.scopes[0].entry) == 1:
            self.scopes[0].variables['n'] = {'type': 'nat', 'value': 5}
            self.visit(
                CallNode(list(self.scopes[0].entry.keys())[0], [ConstantNumNode(5)]))

        self.scopes.pop()

    @visitor.when(IfNode)
    def visit(self, node: IfNode):
        print('if Node')
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
        print("else Node")
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
        print(f">> {st}")
        return st

    def type_cast(self, var, type):
        if type in ['int', 'nat', 'num']:
            return int(var)
        else:
            return var

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode):
        print("declare var")
        self.scopes[self.current_scope].variables[node.id] = {
            'type': node.type, 'value': self.type_cast(self.visit(node.expr), node.type)}
        self.scopes[self.current_scope].variables[node.id]

    # TODO look for the var bottom up
    @visitor.when(AssignNode)
    def visit(self, node: AssignNode):
        print("Assign var")
        for i in range(0, self.current_scope):
            if node.id in self.scopes[self.current_scope-i].variables:
                self.scopes[self.current_scope-i].variables[node.id]['value'] = self.visit(
                    node.expr)
                break

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode):
        print("Func declaration node")
        self.scopes[0].functions[node.id] = {"func": node, "type": node.type}

    @visitor.when(EntryDeclarationNode)
    def visit(self, node: EntryDeclarationNode):
        print("Entry dec Node")
        self.scopes[0].entry[node.id] = {"func": node, "type": None}

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode):
        print("While Node")
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
        print("Attr")
        self.scopes[self.current_scope].variables[node.id] = {
            'type': node.type, 'value': None}
        return self.scopes[self.current_scope].variables[node.id]

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, val=True):
        print("var")
        sc = self.current_scope
        if self.scope_bound:
            sc -= 1
        for i in range(0, self.current_scope+1):
            print(self.scopes[self.current_scope-i].variables)
            if node.lex in self.scopes[self.current_scope-i].variables:
                if not val:
                    return self.scopes[self.current_scope-i].variables[node.lex]
                else:
                    return self.scopes[self.current_scope-i].variables[node.lex]['value']

    @visitor.when(AtomicNode)
    def visit(self, node: AtomicNode):
        print("atomic", node)
        return node.lex

    @visitor.when(ConstantStringNode)
    def visit(self, node: ConstantStringNode):
        print("string")
        return node.lex

    @visitor.when(ConstantNumNode)
    def visit(self, node: AtomicNode):
        print('num')
        return int(node.lex)

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        print("plus")
        l = self.visit(node.left)
        r = self.visit(node.right)
        print(f'{l} + {r}')
        return l+r

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        print(f'{l} - {r}')

        return l-r

    @visitor.when(DivNode)
    def visit(self, node: DivNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        print(f'{l} // {r}')

        return l/r

    @visitor.when(StarNode)
    def visit(self, node: StarNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        print(f'{l} * {r}')

        return l*r

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        print(f'{l} == {r}')

        return l == r

    @visitor.when(InequalityNode)
    def visit(self, node: InequalityNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        print(f'{l} != {r}')

        return l != r

    @visitor.when(GreaterThanEqualNode)
    def visit(self, node: GreaterThanEqualNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        print(f'{l} >= {r}')

        return l >= r

    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        print(f'{l} > {r}')

        return l > r

    @visitor.when(LessThanEqualNode)
    def visit(self, node: LessThanEqualNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        print(f'{l} <= {r}')

        return l <= r

    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        print(f'{l} < {r}')

        return l < r

    @visitor.when(CallNode)
    def visit(self, node: CallNode):
        print(f"Calling {node.id} {node.args}")

        self.scopes.append(ScopeContext())
        self.current_scope += 1

        fun: CallNode = node.id

        try:
            fun_node: FuncDeclarationNode = self.scopes[0].functions[fun]['func']
        except:
            fun_node: FuncDeclarationNode = self.scopes[0].entry[fun]['func']

        for p, i in enumerate(fun_node.params):
            at = self.visit(node.args[p])
            pa_n = self.visit(i)
            print(i.id, pa_n)
            print(at)
            pa_n['value'] = at
            self.scopes[self.current_scope].variables[i.id] = pa_n

        print(self.scopes[-1].variables)
        # idx = 0
        # if len(node.args) > 0:
        #     for p in self.scopes[self.current_scope].variables:
        #         print("pppp", node.args[idx], self.visit(
        #             node.args[idx]))
        #         # self.scope_bound = True
        #         print(self.scopes[self.current_scope].variables[p])
        #         self.scopes[self.current_scope].variables[p]['value'] = self.visit(
        #             node.args[idx])
        #         print(self.scopes[self.current_scope].variables[p])
        #         # self.scope_bound = False
        #         idx += 1

        for st in fun_node.body:
            self.visit(st)

        self.scopes.pop()
        self.current_scope -= 1
