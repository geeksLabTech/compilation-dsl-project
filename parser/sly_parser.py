from sly import Parser
from lexer.sly_lexer import TzScriptLexer

class TzScriptParser(Parser):
    
    tokens = TzScriptLexer.tokens
    
    precedence = (
        ('left', "+", '-'),
        ('left', "*", '/'),
        ('right', "UMINUS")
    )
    
    def __init__(self):
        self.env = {}
        
    @_("")
    def statement(self, p):
        pass
    
    @_("var_assign")
    def statement(slef, p):
        return p.var_assign
    
    @_("NAME '=' expr")
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)
    
    @_("NAME '=' STRING")
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)
    
    @_('expr')
    def statement(self, p):
        return (p.expr)
    
    @_("expr '+' expr")
    def expr(self, p):
        return ('add', p.expr0, p.expr1)
    
    @_("expr '-' expr")
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)
    
    @_("expr '*' expr")
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)
    
    @_("expr '/' expr")
    def expr(self, p):
        return ('div', p.expr0, p.expr1)
    
    @_("'-' expr  expr")
    def expr(self, p):
        return ('add', p.expr0, p.expr1)
    
    @_("ENTRY ID LPAREN params RPAREN {")
    def entry(self,p):
        return ("ENTRY", p.NAME, p.params)
    
    # Define a rule to parse the list of parameters
    @_("NAME")
    @_("parameters COMMA NAME")
    def parameters(self, p):
        if len(p) == 1:
            # If there is only one parameter, return a singleton list
            return [p.NAME]
        else:
            # If there are multiple parameters, append the new parameter to the list
            p.parameters.append(p.NAME)
            return p.parameters