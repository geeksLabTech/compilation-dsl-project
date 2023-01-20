
from grammar import Grammar
from parser.tzscript_ast import ProgramNode, EntryDeclarationNode, FuncDeclarationNode, DeclarationStorageNode, AttrDeclarationNode, WhileNode, IfNode, ReturnStatementNode, EqualNode, LessThanEqualNode, PlusNode, CallNode, ConstantNumNode, DivNode, ConstantStringNode, FalseNode, TrueNode, GreaterThanNode, InequalityNode, MinusNode, VariableNode, VarCallNode, VarDeclarationNode, StarNode, GreaterThanEqualNode, LessThanNode

# grammar
TZSCRIPT_GRAMMAR = Grammar()

# non-terminals
program = TZSCRIPT_GRAMMAR.NonTerminal('<program>', startSymbol=True)
stat_list, stat,stat_program_list,stat_program,storage,storage_list = TZSCRIPT_GRAMMAR.NonTerminals('<stat_list> <stat> <stat_program_list> <stat_program> <storage> <storage_list>')
let_var, def_func, if_stat, else_stat, def_entry, while_stat = TZSCRIPT_GRAMMAR.NonTerminals('<let-var>> <def-func> <if-stat> <else-stat> <def-entry> <while-stat> ')
param_list, param, expr_list, op_param_list = TZSCRIPT_GRAMMAR.NonTerminals('<param-list> <param> <expr-list> <op-param-list')
expr, arith, term, factor, atom , equality, comparison, unary, primary, subfactor = TZSCRIPT_GRAMMAR.NonTerminals('<expr> <arith> <term> <factor> <atom> <equality> <comparison> <unary> <primary> <subfactor>')
func_call, arg_list, var_call, return_stat,op_else = TZSCRIPT_GRAMMAR.NonTerminals('<func-call> <arg-list> <var-call> <return-stat> <op-else>')

# terminals
let, func, entry , then = TZSCRIPT_GRAMMAR.Terminals('let func entry then')
semi, colon, comma, dot, opar, cpar, ocur, ccur = TZSCRIPT_GRAMMAR.Terminals('; : , . ( ) { }')
equal, equalequal, plus, minus, star, div, lessthanequal, greaterthanequal, inequality, lessthan, greaterthan = TZSCRIPT_GRAMMAR.Terminals(
    '= == + - * / <= >= != < >')
idx, num, typex, contract, ifx, elsex, truex, falsex, returnx, stringx, dquoutes, whilex, call = TZSCRIPT_GRAMMAR.Terminals(
    'id num type contract if else true false return string_text " while call')

# productions
program %= contract + idx + opar + op_param_list + ocur + stat_program_list + ccur, lambda h, s: ProgramNode(
        s[2], s[4], s[6]), None, None, None, None, None, None, None


stat_program_list %= stat_program_list + stat_program, lambda h, s: s[1] + [s[2]], None, None
stat_program_list %= stat_program, lambda h, s: [s[1]], None

stat_program%= def_func, lambda h, s: s[1], None
stat_program%= def_entry, lambda h, s: s[1], None
stat_program %= storage, lambda h, s: s[1], None

stat_list %= stat_list + stat, lambda h, s: s[1] + [s[2]], None, None
stat_list %= stat, lambda h, s: [s[1]], None

stat %= while_stat, lambda h, s: s[1], None
stat %= if_stat, lambda h, s: s[1], None
# stat %= else_stat, lambda h, s: s[1], None
stat %= return_stat, lambda h, s: s[1], None
stat %= var_call, lambda h, s: s[1], None
stat %= let_var, lambda h, s: s[1], None


storage %= let + idx + colon + typex + semi , lambda h,s :DeclarationStorageNode(s[2], s[4]), None, None, None,None,None

while_stat %= whilex + opar +expr + cpar + ocur + stat_list + ccur, lambda h, s: WhileNode(
        s[1], s[3], s[6]), None, None, None, None, None, None, None
if_stat %= ifx + opar + expr +  cpar + ocur + then + ocur + stat_list + ccur + op_else, lambda h, s: IfNode(
        s[1], s[6], s[3], s[8],s[10]), None, None, None, None, None, None, None,None,None,None
else_stat %= elsex + ocur + stat_list + ccur, lambda h, s: s[3], None, None, None, None
return_stat %= returnx + expr + semi, lambda h, s: ReturnStatementNode(s[1], s[2]), None, None, None

def_func %= func + idx + opar + param_list + cpar + colon + typex + ocur + stat_list + ccur, lambda h, s: FuncDeclarationNode(
        s[2], s[4], s[7], s[9]), None, None, None, None, None, None, None, None, None,None

def_entry %= entry + idx + opar + op_param_list + ocur + stat_list +ccur, lambda h, s: EntryDeclarationNode(
        s[2], s[4], s[6]), None, None, None, None, None, None, None

op_else %= else_stat + ccur,lambda h,s:s[1],None,None
op_else%= ccur, lambda h,s: [], None

op_param_list %= param_list + cpar, lambda h,s: s[1], None,None
op_param_list %= cpar, lambda h,s: [], None

param_list %= param , lambda h, s: [s[1]], None
param_list %= param_list + comma +param, lambda h, s: s[1] + [s[3]], None, None, None

param %= idx + colon + typex, lambda h, s: AttrDeclarationNode(s[1], s[3]), None, None, None


'''
expression     → equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" ;
'''
expr %= equality, lambda h, s: s[1], None


equality %= comparison, lambda h, s: s[1], None
equality %= equality + inequality + comparison, lambda h, s: InequalityNode(s[2], s[1], s[3]), None, None, None
equality %= equality + equalequal + comparison, lambda h, s: EqualNode(s[2], s[1], s[3]), None, None, None

comparison %= term, lambda h, s: s[1], None
comparison %= comparison + greaterthanequal + term, lambda h, s: GreaterThanEqualNode(s[2], s[1], s[3]), None, None, None
comparison %= comparison + lessthanequal + term, lambda h, s: LessThanEqualNode(s[2], s[1], s[3]), None, None, None
comparison %= comparison + greaterthan + term, lambda h, s: GreaterThanNode(s[2], s[1], s[3]), None, None, None
comparison %= comparison + lessthan + term, lambda h, s: LessThanNode(s[2], s[1], s[3]), None, None, None

# term %= func_call, lambda h, s: s[1], None
term %= factor, lambda h, s: s[1], None
term %= term + plus + factor, lambda h, s: PlusNode(s[2], s[1], s[3]), None, None, None
term %= term + minus + factor, lambda h, s: MinusNode(s[2], s[1], s[3]), None, None, None


factor %= subfactor, lambda h, s: s[1], None
factor %= factor + star + subfactor, lambda h, s: StarNode(s[2], s[1], s[3]), None, None, None
factor %= factor + div + subfactor, lambda h, s: DivNode(s[2], s[1], s[3]), None, None, None

subfactor %= primary, lambda h, s: s[1], None
subfactor %= opar + expr + cpar, lambda h, s: s[2], None, None, None

# unary %= minus + unary, lambda h, s: MinusNode(s[1], s[2]), None, None, None
# unary %= primary, lambda h, s: s[1], None
# unary %= primary + func_call, lambda h, s: CallNode(s[1],s[2]), None, None

primary %= num, lambda h, s: ConstantNumNode(s[1]), None
primary %= idx, lambda h, s: VariableNode(s[1]), None
primary %= func_call, lambda h, s: s[1], None
primary %= stringx, lambda h, s: ConstantStringNode(s[1]), None
primary %= truex, lambda h, s: TrueNode(s[1]), None
primary %= falsex, lambda h, s: FalseNode(s[1]), None

# primary %= opar + expr + cpar, lambda h, s: s[2], None, None, None

# oper %= expr + equalequal + term, lambda h, s: EqualNode(s[2], s[1], s[3]), None, None, None
# oper %= expr + lessthanequal + term, lambda h, s: LessThanEqualNode(s[2], s[1], s[3]), None, None, None
# oper %= expr + greaterthanequal + term, lambda h, s: GreaterThanEqualNode(s[2], s[1], s[3]), None, None, None
# oper %= expr + iniquelaty + term, lambda h, s: InequalityNode(s[2], s[1], s[3]), None, None, None
# oper %= expr + lessthan + term, lambda h, s: LessThanNode(s[2], s[1], s[3]), None, None, None
# oper %= expr + greaterthan + term, lambda h, s: GreaterThanNode(s[2], s[1], s[3]), None, None, None
# oper %= expr,lambda h,s:s[1]

# expr_list %= expr, lambda h, s: [s[1]], None
# expr_list %= expr + comma + expr_list, lambda h, s: [s[1]] + s[3], None, None, None

# expr %= expr + plus + term, lambda h, s: PlusNode(s[2], s[1], s[3]), None, None, None
# expr %= expr + minus + term, lambda h, s: MinusNode(s[2], s[1], s[3]), None, None, None
# expr %= term,lambda h, s: s[1], None

# factor %= atom, lambda h, s: s[1], None
# factor %= func_call, lambda h, s: s[1], None
# factor %= opar + expr + cpar, lambda h, s: s[2], None, None, None

# term %= term + star + factor, lambda h, s: StarNode(s[2], s[1], s[3]), None, None, None
# term %= term + div + factor, lambda h, s: DivNode(s[2], s[1], s[3]), None, None, None
# term %= factor, lambda h, s: s[1], None  # MMM

# atom %= num, lambda h, s: ConstantNumNode(s[1]), None
# atom %= idx, lambda h, s: VariableNode(s[1]), None
# atom %= dquoutes + stringx + dquoutes, lambda h, s: ConstantStringNode(s[2]), None, None, None
# atom %= truex, lambda h, s: TrueNode(s[1]), None
# atom %= falsex, lambda h, s: FalseNode(s[1]), None

func_call %= idx + opar + arg_list + cpar, lambda h, s: CallNode(s[1], s[3]), None, None, None, None

var_call %= idx + equal + expr + semi, lambda h, s: VarCallNode(s[1], s[3]), None, None, None, None

let_var %= let + idx + colon + typex + equal + expr + semi , lambda h, s: VarDeclarationNode(s[2], s[4], s[6]), None, None, None, None, None, None, None

arg_list %= idx, lambda h, s: [VariableNode(s[1])], None
arg_list %= idx + comma + arg_list, lambda h, s: [VariableNode(s[1])] + s[3], None, None, None
# <arith>        ???


if __name__ == '__main__':
    pass
