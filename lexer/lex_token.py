
from grammar import Terminal
from parser.tzscript_types import TzScriptType


class Token:
    """
    Basic token class.

    Parameters
    ----------
    lex : str
        Token's lexeme.
    token_type : Enum
        Token's type.
    """

    def __init__(self, lex: str, token_type: Terminal, tzscript_type=None, line_no: int = 0, col_no: int = 0):
        # def __init__(self, lex: str, token_type: Terminal, tzscript_type: TzScriptType|None = None, line_no: int = 0, col_no: int = 0):
        self.lex = lex
        self.token_type = token_type
        self.line_no = line_no
        self.col_no = col_no
        self.tzscript_type = tzscript_type

    def __str__(self):
        return f'{self.token_type}: {self.lex}'

    def __repr__(self):
        return str(self)

    @property
    def is_valid(self):
        return True


class UnknownToken(Token):
    def __init__(self, lex):
        Token.__init__(self, lex, None, None)

    def transform_to(self, token_type):
        return Token(self.lex, token_type, None)

    @property
    def is_valid(self):
        return False
