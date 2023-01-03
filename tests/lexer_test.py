
from lexer.tzscript_lexer import TzScriptLexer
from lexer.lex_token import Token
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR

import pytest


def test_hello_world_example():
    contract = '''
    contract hello_world () {
        var msg : string = "Hello";
        entry input(name: string) {
            if (len(msg) > 5) {
                msg = msg + " " + name;
            }
            else {
                msg = msg + "," + " " + name;
            }
        }
    }
    '''
    # build list of tuples of (Terminal, string)
    words_separated_by_spaces = ['contract', 'hello_world', '(', ')', '{', 'var', 'msg', ':', 'string', '=', '"Hello"', ';', 'entry', 'input', '(', 'name', ':', 'string', ')', '{', 'if', '(', 'len', '(', 'msg', ')', '>', '5', ')', '{', 'msg', '=', 'msg', '+', '" "', '+', 'name', ';', '}', 'else', '{', 'msg', '=', 'msg', '+', '", "', '+', '" "', '+', 'name', ';', '}', '}', '}']
    table = [(TZSCRIPT_GRAMMAR[tok], tok) for tok in words_separated_by_spaces]
    expected_tokens = [ Token(x[1], x[0]) for x in table]
    tz_lexer = TzScriptLexer()
    lexer_tokens = tz_lexer.tokenize(contract)
    
    assert lexer_tokens == expected_tokens