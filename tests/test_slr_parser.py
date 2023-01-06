from lexer.tzscript_lexer import TzScriptLexer
from lexer.lex_token import Token
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR,idx, num, typex, contract, ifx, elsex,equal, plus, minus, star, div,semi, colon, comma, dot, opar, cpar, ocur, ccur,let, func,entry
from parser.slr_parser import SLR1Parser, build_slr_ast

import pytest

def test_productions_and_operations():
    words_separated_by_spaces = ['contract', 'store_value','(',')','{','let', 'storage',':', 'int','=', '0',';', 'entry', 'replace','(','new_value',':', 'int',')','{','storage', '=', 'new_value',';','}','}']
    parser = SLR1Parser(TZSCRIPT_GRAMMAR, verbose=True)
    tokens = [Token('contract',contract),Token('store_value',idx),Token('(',opar),Token('value',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token('{',ocur),Token('let',let),Token('storage',idx),Token(':',colon),Token('int',typex),Token('=',equal),Token('0',num),Token(';',semi),Token('entry',entry),Token('replace',idx),Token('(',opar),Token('new_value',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token('{',ocur),Token('storage',idx),Token('=',equal),Token('new_value',idx),Token(';',semi),Token('}',ccur),Token('}',ccur),Token('EOF',TZSCRIPT_GRAMMAR.EOF)]

    terminals = [token.token_type for token in tokens]
    derivation = parser(terminals, True)
    assert derivation is not None
    productions, operations = derivation
    print(' real productions')
    # print(productions)
    print()
    expected_productions = '[<param> -> id : type, <param-list> -> <param>, <atom> -> num, <factor> -> <atom>, <term> -> <factor>, <expr> -> <term>, <let-var>> -> let id : type = <expr> ;, <stat> -> <let-var>>, <param> -> id : type, <param-list> -> <param>, <atom> -> id, <factor> -> <atom>, <term> -> <factor>, <expr> -> <term>, <var-call> -> id = <expr> ;, <stat> -> <var-call>, <stat_list> -> <stat>, <def-entry> -> entry id ( <param-list> ) { <stat_list> }, <stat> -> <def-entry>, <stat_list> -> <stat>, <stat_list> -> <stat> <stat_list>, <program> -> contract id ( <param-list> ) { <stat_list> }]'
    expected_operations = ['SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'REDUCE', 'REDUCE', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'REDUCE', 'REDUCE', 'REDUCE', 'REDUCE', 'SHIFT','REDUCE','REDUCE','SHIFT','SHIFT','SHIFT','SHIFT','SHIFT','SHIFT','REDUCE','REDUCE','SHIFT','SHIFT','SHIFT','SHIFT','SHIFT','REDUCE','REDUCE','REDUCE','REDUCE','SHIFT','REDUCE','REDUCE','REDUCE','SHIFT','REDUCE','REDUCE','REDUCE','REDUCE','SHIFT','REDUCE']
    assert str(productions) == expected_productions
    assert operations == expected_operations



