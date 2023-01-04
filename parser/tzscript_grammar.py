
from grammar import Grammar
from parser.tzscript_ast import *

# grammar
TZSCRIPT_GRAMMAR = Grammar()

# non-terminals
program = TZSCRIPT_GRAMMAR.NonTerminal('<program>', startSymbol=True)
stat_list, stat = TZSCRIPT_GRAMMAR.NonTerminals('<stat_list> <stat>')
let_var, def_func, if_stat, else_stat = TZSCRIPT_GRAMMAR.NonTerminals('<<let-var>> <def-func> <if-stat> <else-stat>')
param_list, param, expr_list = TZSCRIPT_GRAMMAR.NonTerminals('<param-list> <param> <expr-list>')
expr, arith, term, factor, atom = TZSCRIPT_GRAMMAR.NonTerminals('<expr> <arith> <term> <factor> <atom>')
func_call, arg_list  = TZSCRIPT_GRAMMAR.NonTerminals('<func-call> <arg-list>')

# terminals
let, func, = TZSCRIPT_GRAMMAR.Terminals('let func')
semi, colon, comma, dot, opar, cpar, ocur, ccur = TZSCRIPT_GRAMMAR.Terminals('; : , . ( ) { }')
equal, plus, minus, star, div = TZSCRIPT_GRAMMAR.Terminals('= + - * /')
idx, num, typex, contract, ifx, elsex = TZSCRIPT_GRAMMAR.Terminals('id num type contract if else')

# productions
program %= contract + idx + opar + param_list + cpar + ocur + stat_list + ccur, lambda h,s: ProgramNode(s[2], s[4], s[7])

stat_list %= stat + semi, lambda h,s: [s[1]],None,None
stat_list %= stat + semi + stat_list, lambda h,s: [s[1]] + s[3],None,None,None

stat %= let_var, lambda h,s: s[1],None
stat %= def_func, lambda h,s: s[1],None
stat %= if_stat, lambda h,s: s[1],None
stat %= else_stat, lambda h,s: s[1],None

if_stat %= ifx + opar + expr + cpar + ocur + stat_list + ccur, lambda h,s: IfNode(s[3], s[6]),None,None,None,None,None,None,None
else_stat %= elsex + ocur + stat_list + ccur, lambda h,s: ElseNode(s[3]),None,None,None,None

def_func %= func + idx + opar + param_list + cpar + typex + ocur + expr_list + ccur, lambda h,s: FuncDeclarationNode(s[2], s[4], s[6], s[8]),None,None,None,None,None,None,None,None,None

param_list %= param, lambda h,s: [ s[1] ],None
param_list %= param + comma + param_list, lambda h,s: [ s[1] ] + s[3],None,None,None

param %= idx + colon + typex, lambda h,s: AttrDeclarationNode(s[1], s[3]),None,None,None

expr_list %= expr, lambda h,s: [s[1]],None
expr_list %= expr + comma + expr_list, lambda h,s: [s[1]] + s[3],None,None,None

expr %= expr + plus + term, lambda h,s: PlusNode(s[1], s[3]),None,None,None
expr %= expr + minus + term, lambda h,s: MinusNode(s[1], s[3]),None,None,None
expr %= term, lambda h,s: s[1],None
# <arith>        ???
term %= term + star + factor, lambda h,s: StarNode(s[1], s[3]),None,None,None
term %= term + div + factor, lambda h,s: DivNode(s[1], s[3]),None,None,None
term %= factor, lambda h,s: s[1],None # MMM

factor %= atom, lambda h,s: s[1],None
factor %= opar + expr + cpar, lambda h,s: s[2],None,None,None

atom %= num, lambda h,s: ConstantNumNode(s[1]),None
atom %= idx, lambda h,s: VariableNode(s[1]),None
atom %= func_call, lambda h,s: s[1],None

func_call %= idx + opar + arg_list + cpar, lambda h,s: CallNode(s[1], s[3]),None,None,None,None

let_var %= let + idx + typex + equal + expr, lambda h,s: VarDeclarationNode(s[2], s[3], s[5]),None,None,None,None,None

arg_list %= idx, lambda h,s: [s[1]],None
arg_list %= idx + comma + arg_list, lambda h,s: [s[1]] + s[3],None,None,None


if __name__ == '__main__': print(TZSCRIPT_GRAMMAR)

