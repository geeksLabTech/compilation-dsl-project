from sly import Lexer

class TzScriptLexer(Lexer):

    tokens = {ID,NUMBER,IF,ELSE,WHILE,PLUS,MINUS,TIMES,DIVIDE,EQ,ASSIGN,LE,LT,GE,GT,NE, VAR,CONTRACT,STRING}
    
    # Tokens
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    # Special Cases
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['var'] = VAR
    ID['contract'] = CONTRACT
    ID['string'] = STRING

    ignore = ' \t'
    
    # Symbols
    literals = { ':', ';' , "\"", "\'", '{', '}' , '(', ')', ',' , '='}
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
