from sly import Lexer
# from grammar import *
from grammar import Grammar

class TzScriptLexer(Lexer):
    

    # grammar
    TZSCRIPT_GRAMMAR = Grammar()

    # non-terminals
    program = TZSCRIPT_GRAMMAR.NonTerminal('<program>', startSymbol=True)
    stat_list, stat = TZSCRIPT_GRAMMAR.NonTerminals('<stat_list> <stat>')
    let_var, def_func, if_stat, else_stat, def_entry = TZSCRIPT_GRAMMAR.NonTerminals('<let-var>> <def-func> <if-stat> <else-stat> <def-entry>')
    param_list, param, expr_list = TZSCRIPT_GRAMMAR.NonTerminals('<param-list> <param> <expr-list>')
    expr, arith, term, factor, atom = TZSCRIPT_GRAMMAR.NonTerminals('<expr> <arith> <term> <factor> <atom>')
    func_call, arg_list, var_call  = TZSCRIPT_GRAMMAR.NonTerminals('<func-call> <arg-list> <var-call>')

    # terminals
    let, func, entry = TZSCRIPT_GRAMMAR.Terminals('let func entry')
    semi, colon, comma, dot, opar, cpar, ocur, ccur = TZSCRIPT_GRAMMAR.Terminals('; : , . ( ) { }')
    equal, plus, minus, star, div = TZSCRIPT_GRAMMAR.Terminals('= + - * /')
    idx, num, typex, contract, ifx, elsex = TZSCRIPT_GRAMMAR.Terminals('id num type contract if else')

        
    reserved_words = [ 'contract','entry','func','let','if','else','const','type','for','in','string','nat','int','map','optional','bool','None','true','false','return','calledBy']
    # Set of token names. This is always required
    
    tokens = {
        COLON,
        SEMICOLON,
        COMMA,
        INTEGER,
        LPAREN,
        RPAREN,
        LBRACE,
        RBRACE,
        LBRACKET,
        RBRACKET,
        ID,
        OR,
        AND,
        OPERATOR,
        TERMINAL,
        NONTERMINAL,
        EPSILON,
        SENTENCE,
        SENTENCELIST,
        ATTRIBUTEPRODUCTION,
        PRODUCTION,
        GRAMMAR,
        CONTRACT,
        ENTRY,
        FUNC,
        LET,
        IF,
        ELSE,
        CONST,
        TYPE,
        FOR,
        IN,
        STRING,
        NAT,
        INT,
        MAP,
        OPTIONAL,
        BOOL,
        NONE,
        TRUE,
        FALSE,
        RETURN,
        CALLEDBY
        
    }
    
    tokens.add(t for t in R_W)

    # String containing ignored characters (spaces and tabs)
    ignore = ' \t'

    # Regular expression rules for tokens
    COLON = r'\:'
    SEMICOLON = r'\;'
    COMMA = r'\,'
    INTEGER = r'\d+'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    OPERATOR = r'[=<>+-/%*]+'
    OR = r'\|'
    AND = r'\&'
    TERMINAL = r'Terminal'
    NONTERMINAL = r'NonTerminal'
    EPSILON = r'Epsilon'
    SENTENCE = r'Sentence'
    SENTENCELIST = r'SentenceList'
    ATTRIBUTEPRODUCTION = r'AttributeProduction'
    PRODUCTION = r'Production'
    GRAMMAR = r'Grammar'
    
    # reserved Words
    ID["contract"] = contract
    ID['entry'] = entry
    ID['func'] = func
    ID['let'] = let
    ID['if'] = ifx
    ID['else'] = elsex
    ID['const'] = CONST
    ID['type'] = typex
    ID['for'] = FOR
    ID['in'] = IN
    ID['string'] = typex
    ID['nat'] = typex
    ID['int'] = typex
    ID['map'] = typex
    ID['optional'] = typex
    ID['bool'] = typex
    ID['None'] = typex
    ID['true'] = TRUE
    ID['false'] = FALSE
    ID['return'] = RETURN
    ID['calledBy'] = CALLEDBY


    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        if t.value in reserved_words:
            t.type = t.value.upper()
        return t
    # Define a rule so we can track line numbers
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')    

    def t_OPERATOR(self, t):
        r'[=<>+-/*]+'
        return t
    
    def t_COLON(self, t):
        r'\:'
        return t

    def t_SEMICOLON(self, t):
        r'\;'
        return t

    def t_COMMA(self, t):
        r'\,'
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_LPAREN(self, t):
        r'('
        return t

    def t_RPAREN(self, t):
        r')'
        return t

    def t_LBRACE(self, t):
        r'\{'
        return t

    def t_RBRACE(self, t):
        r'\}'
        return t

    def t_LBRACKET(self, t):
        r'\['
        return t

    def t_RBRACKET(self, t):
        r'\]'
        return t

    def t_error(self, t):
        raise ValueError(f'Invalid token: {t.value[0]}')