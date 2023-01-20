from parser.tzscript_ast import *
from visitors.visitor import when
from visitors import visitor


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
        self.break_exec = False

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.go_else = False
        self.scopes.append(ScopeContext())

        # for p in node.params:
        #     self.scopes[self.current_scope].variables[str(p.idx)] = {'type':p.typex, 'value': None}
        if len(list(self.scopes[0].entry.keys())) > 1:
            raise SyntaxError('More than one Entrypoint defined.')

        for st in node.statements:
            # print(self.scopes)
            self.visit(st)
            if self.break_exec:
                break
        if list(self.scopes[0].entry.keys())[-1] != 'main':
            raise TypeError("Entrypoint 'main' missing.")
        # self.scopes[0].variables['n'] = {'type': 'nat', 'value': 5}
        self.visit(CallNode(list(self.scopes[0].entry.keys())[-1], []))

        self.scopes.pop()

    @visitor.when(IfNode)
    def visit(self, node: IfNode):
        # print('if Node')
        self.go_else = False
        r = ''
        if self.visit(node.expr):
            self.current_scope += 1
            self.scopes.append(ScopeContext())

            for st in node.then_statements:
                t = self.visit(st)

                if t is not None:
                    r = t

                if self.break_exec:
                    break

        else:
            self.current_scope += 1
            self.scopes.append(ScopeContext())
            for st in node.else_statements:
                t = self.visit(st)

                if t is not None:
                    r = t

                if self.break_exec:
                    break

        self.scopes.pop()
        self.current_scope -= 1

        return r

    @visitor.when(ReturnStatementNode)
    def visit(self, node: ReturnStatementNode):
        st = self.visit(node.expr)
        print(f">> {st}")
        self.break_exec = True
        return st

    def type_cast(self, var, type):
        # print("Casting", var, type.name._value_)
        if type.name._value_ in ['int', 'nat', 'num']:
            # print("True")
            try:
                return int(var)
            except:
                return var
        else:
            return var

    @visitor.when(DeclarationStorageNode)
    def visit(self, node: DeclarationStorageNode):
        # print("declare var in storage")
        self.scopes[self.current_scope].variables[node.id] = {
            'type': node.type, 'value': None}
        self.scopes[self.current_scope].variables[node.id]

    @visitor.when(VarCallNode)
    def visit(self, node: VarCallNode):
        # print(f"Modifiying {node.id}")
        sc = self.current_scope
        if self.scope_bound:
            sc -= 1
        for i in range(0, self.current_scope+1):
            # print(self.scopes[self.current_scope-i].variables)
            if node.id in self.scopes[self.current_scope-i].variables:
                self.scopes[self.current_scope -
                            i].variables[node.id]['value'] = self.visit(node.expr)

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode):
        # print("declare var")
        # print(node.expr)
        val = self.visit(node.expr)
        self.scopes[self.current_scope].variables[node.id] = {
            'type': node.type, 'value': self.type_cast(val, node.type)}
        self.scopes[self.current_scope].variables[node.id]

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode):
        # print("Func declaration node")
        self.scopes[0].functions[node.id] = {"func": node, "type": node.type}

    @visitor.when(EntryDeclarationNode)
    def visit(self, node: EntryDeclarationNode):
        # print("Entry dec Node")
        self.scopes[0].entry[node.id] = {"func": node, "type": None}

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode):
        # print("While Node")
        self.scopes.append(ScopeContext())
        self.current_scope += 1

        cond = self.visit(node.expr)
        r = ''
        while(cond):
            for st in node.statements:
                r = self.visit(st)
                
                if self.break_exec:
                    break
            if self.break_exec:
                    break

            cond = self.visit(node.expr)

        self.current_scope -= 1
        self.scopes.pop()

        return r

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode):
        # print("Attr")
        self.scopes[self.current_scope].variables[node.id] = {
            'type': node.type, 'value': None}
        return self.scopes[self.current_scope].variables[node.id]

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode):
        # print("var")
        sc = self.current_scope
        if self.scope_bound:
            sc -= 1
        for i in range(0, self.current_scope+1):
            # print(self.scopes[self.current_scope-i].variables)
            if node.lex in self.scopes[self.current_scope-i].variables:
                return self.scopes[self.current_scope-i].variables[node.lex]['value']

    @visitor.when(AtomicNode)
    def visit(self, node: AtomicNode):
        # print("atomic", node)
        return node.lex

    @visitor.when(ConstantStringNode)
    def visit(self, node: ConstantStringNode):
        # print("string")
        return node.lex

    @visitor.when(ConstantNumNode)
    def visit(self, node: AtomicNode):
        # print('num', node.lex)
        return int(node.lex)

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        # print("plus")
        l = self.visit(node.left)
        r = self.visit(node.right)
        # print(f'{l} + {r}')
        return int(l+r)

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        # print(f'{l} - {r}')

        return int(l-r)

    @visitor.when(DivNode)
    def visit(self, node: DivNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        # print(f'{l} // {r}')

        return int(l/r)

    @visitor.when(StarNode)
    def visit(self, node: StarNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        # print(f'{l} * {r}')

        return int(l*r)

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        # print(f'{l} == {r}')

        return l == r

    @visitor.when(InequalityNode)
    def visit(self, node: InequalityNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        # print(f'{l} != {r}')

        return l != r

    @visitor.when(GreaterThanEqualNode)
    def visit(self, node: GreaterThanEqualNode):
        l = self.visit(node.left)
        r = self.visit(node.right)

        # print(f'{l} >= {r}')

        return l >= r

    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        # print(f'{l} > {r}')

        return l > r

    @visitor.when(LessThanEqualNode)
    def visit(self, node: LessThanEqualNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        # print(f'{l} <= {r}')

        return l <= r

    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode):
        l = self.visit(node.left)
        r = self.visit(node.right)
        # print(f'{l} < {r}')

        return l < r

    @visitor.when(CallNode)
    def visit(self, node: CallNode):
        n_a = node.args
        n_a = [self.visit(arg) for arg in n_a]
        print(f"Calling {node.id} {n_a}")
        r = None
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
            # print(i.id, pa_n)
            # print(at)
            pa_n['value'] = at
            self.scopes[self.current_scope].variables[i.id] = pa_n

        # print("scope", self.scopes[-1].variables)

        for st in fun_node.body:
            t = self.visit(st)
            if t is not None:
                r = t
            if self.break_exec:
                break
            
        self.break_exec = False
        self.scopes.pop()
        self.current_scope -= 1

        return r
