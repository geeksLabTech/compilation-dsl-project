# from math import prod
# from lexer.tzscript_lexer import TzScriptLexer
# from lexer.lex_token import Token
# from parser.tzscript_grammar import TZSCRIPT_GRAMMAR,idx, num, typex, contract, ifx, elsex,equal, plus, minus, star, div,semi, colon, comma, dot, opar, cpar, ocur, ccur,let, func,entry, returnx, lessthanequal
# from parser.slr_parser import SLR1Parser, build_slr_ast

# import pytest

# def test_productions_and_operations_hello_world():
#    words_separated_by_spaces = ['contract', 'store_value','(',')','{','let', 'storage',':', 'int','=', '0',';', 'entry', 'replace','(','new_value',':', 'int',')','{','storage', '=', 'new_value',';','}','}']
#    parser = SLR1Parser(TZSCRIPT_GRAMMAR, verbose=True)
#    tokens = [Token('contract',contract),Token('store_value',idx),Token('(',opar),Token('value',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token('{',ocur),Token('let',let),Token('storage',idx),Token(':',colon),Token('int',typex),Token('=',equal),Token('0',num),Token(';',semi),Token('entry',entry),Token('replace',idx),Token('(',opar),Token('new_value',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token('{',ocur),Token('storage',idx),Token('=',equal),Token('new_value',idx),Token(';',semi),Token('}',ccur),Token('}',ccur),Token('EOF',TZSCRIPT_GRAMMAR.EOF)]

#    terminals = [token.token_type for token in tokens]
#    derivation = parser(terminals,True)
#    assert derivation is not None
#    productions, operations = derivation
#    print(' real productions')
#    # print(productions)
#    print()
#    expected_productions = '[<param> -> id : type, <param-list> -> <param>, <atom> -> num, <factor> -> <atom>, <term> -> <factor>, <expr> -> <term>, <let-var>> -> let id : type = <expr> ;, <stat> -> <let-var>>, <stat_list> -> <stat>, <param> -> id : type, <param-list> -> <param>, <atom> -> id, <factor> -> <atom>, <term> -> <factor>, <expr> -> <term>, <var-call> -> id = <expr> ;, <stat> -> <var-call>, <stat_list> -> <stat>, <def-entry> -> entry id ( <param-list> ) { <stat_list> }, <stat> -> <def-entry>, <stat_list> -> <stat_list> <stat>, <program> -> contract id ( <param-list> ) { <stat_list> }]'
   
   
#    expected_operations = ['SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'REDUCE', 'REDUCE', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'REDUCE', 'REDUCE', 'REDUCE', 'REDUCE', 'SHIFT', 'REDUCE', 'REDUCE', 'REDUCE', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'REDUCE', 'REDUCE', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'SHIFT', 'REDUCE', 'REDUCE', 'REDUCE', 'REDUCE', 'SHIFT', 'REDUCE', 'REDUCE', 'REDUCE', 'SHIFT', 'REDUCE', 'REDUCE', 'REDUCE', 'SHIFT', 'REDUCE']
#    assert str(productions) == expected_productions
#    assert operations == expected_operations


# def test_productions_and_operations_fibonacci():

   
#    expected_productions = '[<param> -> id : type, <param-list> -> <param>, <atom> -> num, <factor> -> <atom>, <term> -> <factor>, <expr> -> <term>, <let-var>> -> let id : type = <expr> ;, <stat> -> <let-var>>, <stat_list> -> <stat>, <param> -> id : type, <param-list> -> <param>, <arg-list> -> id, <func-call> -> id ( <arg-list> ), <factor> -> <func-call>, <term> -> <factor>, <expr> -> <term>, <let-var>> -> let id : type = <expr> ;, <stat> -> <let-var>>, <stat_list> -> <stat>, <atom> -> id, <factor> -> <atom>, <term> -> <factor>, <expr> -> <term>, <var-call> -> id = <expr> ;, <stat> -> <var-call>, <stat_list> -> <stat_list> <stat>, <def-entry> -> entry id ( <param-list> ) { <stat_list> }, <stat> -> <def-entry>, <stat_list> -> <stat_list> <stat>, <param> -> id : type, <param-list> -> <param>, <atom> -> id, <factor> -> <atom>, <term> -> <factor>, <expr> -> <term>, <atom> -> num, <factor> -> <atom>, <term> -> <factor>, <expr> -> <expr> <= <term>, <atom> -> id, <factor> -> <atom>, <term> -> <factor>, <expr> -> <term>, <return-stat> -> return <expr> ;, <stat> -> <return-stat>, <stat_list> -> <stat>, <if-stat> -> if ( <expr> ) { <stat_list> }, <stat> -> <if-stat>, <stat_list> -> <stat>, <atom> -> id, <factor> -> <atom>, <term> -> <factor>, <expr> -> <term>, <atom> -> num, <factor> -> <atom>, <term> -> <factor>, <expr> -> <expr> - <term>, <let-var>> -> let id : type = <expr> ;, <stat> -> <let-var>>, <stat_list> -> <stat>, <atom> -> id, <factor> -> <atom>, <term> -> <factor>, <expr> -> <term>, <atom> -> num, <factor> -> <atom>, <term> -> <factor>, <expr> -> <expr> - <term>, <let-var>> -> let id : type = <expr> ;, <stat> -> <let-var>>, <stat_list> -> <stat_list> <stat>, <arg-list> -> id, <func-call> -> id ( <arg-list> ), <factor> -> <func-call>, <term> -> <factor>, <expr> -> <term>, <arg-list> -> id, <func-call> -> id ( <arg-list> ), <factor> -> <func-call>, <term> -> <factor>, <expr> -> <expr> + <term>, <return-stat> -> return <expr> ;, <stat> -> <return-stat>, <stat_list> -> <stat_list> <stat>, <else-stat> -> else { <stat_list> }, <stat> -> <else-stat>, <stat_list> -> <stat_list> <stat>, <def-func> -> func id ( <param-list> ) : type { <stat_list> }, <stat> -> <def-func>, <stat_list> -> <stat_list> <stat>, <program> -> contract id ( <param-list> ) { <stat_list> }]'
#    expected_operations = ['SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'SHIFT',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE',
#  'REDUCE',
#  'REDUCE',
#  'SHIFT',
#  'REDUCE']
   
#    parser = SLR1Parser(TZSCRIPT_GRAMMAR, verbose=True)
#    tokens = [Token('contract',contract),Token('get_fib_n',idx),Token('(',opar),Token('n',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token('{',ocur),Token('let',let), Token('last_fib_calculated',idx), Token(':', colon), Token('int', typex), Token('=',equal),Token('0',num),Token(';',semi),Token('entry',entry),Token('get_fib',idx),Token('(',opar),Token('n',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token('{',ocur),Token('let',let),Token('result',idx), Token(':', colon), Token('int', typex),Token('=',equal),Token('fib',idx),Token('(',opar),Token('n',idx),Token(')',cpar),Token(';',semi),Token('last_fib_calculated',idx),Token('=',equal),Token('result',idx),Token(';',semi),Token('}',ccur),Token('func',func),Token('fib',idx),Token('(',opar),Token('n',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token(':',colon),Token('int',typex),Token('{',ocur),Token('if',ifx),Token('(',opar),Token('n',idx),Token('<=',lessthanequal),Token('1',num),Token(')',cpar),Token('{',ocur),Token('return',returnx),Token('n',idx),Token(';',semi),Token('}',ccur),Token('else',elsex),Token('{',ocur),Token('let', let), Token('a', idx), Token(':', colon), Token('int', typex), Token('=', equal), Token('n', idx), Token('-', minus), Token('1', num), Token(';', semi), Token('let', let), Token('b', idx), Token(':', colon), Token('int', typex), Token('=', equal), Token('n', idx), Token('-', minus), Token('2', num), Token(';', semi), Token('return',returnx),Token('fib',idx),Token('(',opar),Token('a',idx),Token(')',cpar),Token('+',plus),Token('fib',idx),Token('(',opar),Token('b',idx),Token(')',cpar),Token(';',semi),Token('}',ccur),Token('}',ccur),Token('}',ccur),Token('EOF',TZSCRIPT_GRAMMAR.EOF)]
#    terminals = [token.token_type for token in tokens]
#    derivation = parser(terminals, True)
#    assert derivation is not None
#    productions, operations = derivation
#    print('productions', productions)
#    assert str(productions) == expected_productions
#    assert operations == expected_operations