from sly import Lexer
# from grammar import *
from grammar import Grammar

class TzScriptLexer(Lexer):
           
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
    ID["contract"] = CONTRACT
    ID['entry'] = ENTRY
    ID['func'] = FUNC
    ID['let'] = LET
    ID['if'] = IF
    ID['else'] = ELSE
    ID['const'] = CONST
    ID['type'] = TYPE
    ID['for'] = FOR
    ID['in'] = IN
    ID['string'] = TYPE
    ID['nat'] = TYPE
    ID['int'] = TYPE
    ID['map'] = TYPE
    ID['optional'] = TYPE
    ID['bool'] = TYPE
    ID['None'] = TYPE
    ID['true'] = TRUE
    ID['false'] = FALSE
    ID['return'] = RETURN
    ID['calledBy'] = CALLEDBY

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