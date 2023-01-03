
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

stat_list %= stat + semi, lambda h,s: [s[1]]
stat_list %= stat + semi + stat_list, lambda h,s: [s[1]] + s[3]

stat %= let_var, lambda h,s: s[1]
stat %= def_func, lambda h,s: s[1]
stat %= if_stat, lambda h,s: s[1]
stat %= else_stat, lambda h,s: s[1]

if_stat %= ifx + opar + expr + cpar + ocur + stat_list + ccur, lambda h,s: IfNode(s[3], s[6])
else_stat %= elsex + ocur + stat_list + ccur, lambda h,s: ElseNode(s[3])

def_func %= func + idx + opar + param_list + cpar + typex + ocur + expr_list + ccur, lambda h,s: FuncDeclarationNode(s[2], s[4], s[6], s[8])

param_list %= param, lambda h,s: [ s[1] ]
param_list %= param + comma + param_list, lambda h,s: [ s[1] ] + s[3]

param %= idx + colon + typex, lambda h,s: AttrDeclarationNode(s[1], s[3])

expr_list %= expr, lambda h,s: [s[1]]
expr_list %= expr + comma + expr_list, lambda h,s: [s[1]] + s[3]

expr %= expr + plus + term, lambda h,s: PlusNode(s[1], s[3])
expr %= expr + minus + term, lambda h,s: MinusNode(s[1], s[3])
expr %= term, lambda h,s: s[1]
# <arith>        ???
term %= term + star + factor, lambda h,s: StarNode(s[1], s[3])
term %= term + div + factor, lambda h,s: DivNode(s[1], s[3])
term %= factor, lambda h,s: s[1] # MMM

factor %= atom, lambda h,s: s[1]
factor %= opar + expr + cpar, lambda h,s: s[2]

atom %= num, lambda h,s: ConstantNumNode(s[1])
atom %= idx, lambda h,s: VariableNode(s[1])
atom %= func_call, lambda h,s: s[1]

func_call %= idx + opar + arg_list + cpar, lambda h,s: CallNode(s[1], s[3])

let_var %= let + idx + typex + equal + expr, lambda h,s: VarDeclarationNode(s[2], s[3], s[5])

arg_list %= idx, lambda h,s: [s[1]]
arg_list %= idx + comma + arg_list, lambda h,s: [s[1]] + s[3]


if __name__ == '__main__': print(TZSCRIPT_GRAMMAR)

