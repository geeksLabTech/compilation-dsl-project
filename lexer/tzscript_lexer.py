from grammar import Terminal
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR
from lexer.lexer import Lexer
# Import all terminals from tzscript_grammar.py
from parser.tzscript_grammar import idx, num, typex, contract, equal, plus, minus, star, div, opar, cpar, ocur, ccur, semi, colon, comma, dot, func, let, contract

class TzScriptLexer:
    def __init__(self) -> None:
        self.table = self._build_table()
        print('tabla akiiiiiiiii:',self.table)
        self.lexer = Lexer(self.table, TZSCRIPT_GRAMMAR.EOF)

    def _build_table(self):
        # list of tuplpes of token_type and associated regular expression
        table: list[tuple[Terminal, str]] = []
        # table.append((typex, 'int|bool|string'))
        # table.append((num, '[0-9]+'))
        # table.append((idx, '[a-zA-Z_][a-zA-Z0-9_]*'))
        # table.append((contract, 'contract'))
        # table.append((equal, '='))
        # table.append((plus, '+'))
        # table.append((minus, '-'))
        # table.append((star, '*'))
        # table.append((div, '/'))
        # table.append((opar, '('))
        # table.append((cpar, ')'))
        # table.append((ocur, '{'))
        # table.append((ccur, '}'))
        # table.append((semi, ';'))
        # table.append((colon, ':'))
        # table.append((comma, ','))
        # table.append((dot, '.'))
        # table.append((func, 'func'))
        table.append((let, 'let'))
        return table

    def tokenize(self, text: str):
        return self.lexer(text)

