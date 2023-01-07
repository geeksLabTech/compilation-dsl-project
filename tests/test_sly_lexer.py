from lexer.sly_lexer import TzScriptLexer
from lexer.lex_token import Token
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR,idx, num, typex, contract, ifx, elsex,equal, plus, minus, star, div,semi, colon, comma, dot, opar, cpar, ocur, ccur,let, func,entry,lessthanequal,returnx
import pytest

def test_sly_lexer_hello_world():
    hello_world = '''
    contract store_value(value: int){

    let storage: int = 0;

    entry replace(new_value: int){
       
        storage = new_value;
    } 
    }
    '''
    lexer = TzScriptLexer()
    tokens = list(lexer.tokenize(hello_world))
    expected_tokens = [Token('contract', contract),Token('store_value',idx),Token('(',opar),Token('value',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token('{',ocur),Token('let',let),Token('storage',idx),Token(':',colon),Token('int',typex),Token('=',equal),Token('0',num),Token(';',semi),Token('entry',entry),Token('replace',idx),Token('(',opar),Token('new_value',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token('{',ocur),Token('storage',idx),Token('=',equal),Token('new_value',idx),Token(';',semi),Token('}',ccur),Token('}',ccur),Token('EOF',TZSCRIPT_GRAMMAR.EOF)]
    expected_lexes = [t.lex for t in expected_tokens if t.token_type != TZSCRIPT_GRAMMAR.EOF]
    expected_terminals = [t.token_type for t in expected_tokens if t.token_type != TZSCRIPT_GRAMMAR.EOF]
    lexes = [t.value for t in tokens]
    map_to_terminals_names = {'CONTRACT': contract.Name, 'ID': idx.Name, 'COLON': colon.Name, 'SEMICOLON': semi.Name, 'COMMA': comma.Name, 'INTEGER': num.Name, 'LPAREN': opar.Name, 'RPAREN': cpar.Name, 'LBRACE': ocur.Name, 'RBRACE': ccur.Name, 'LBRACKET': opar.Name, 'RBRACKET': cpar.Name, 'OR': plus.Name, 'AND': star.Name, 'OPERATOR': equal.Name, 'TERMINAL': typex.Name, 'NONTERMINAL': idx.Name, 'ENTRY': entry.Name, 'FUNC': func.Name, 'LET': let.Name, 'IF': ifx.Name, 'ELSE': elsex.Name, 'TYPE': typex.Name, 'STRING': typex.Name, 'NAT': typex.Name, 'INT': typex.Name, 'OPTIONAL': typex.Name, 'BOOL': typex.Name}
    terminals_names = []
    for token in tokens:
        print('hola')
        print(token.type)
        terminals_names.append(map_to_terminals_names[token.type])

    terminals = [TZSCRIPT_GRAMMAR[t] for t in terminals_names]
    assert lexes == expected_lexes
    assert terminals == expected_terminals


def test_sly_lexer_fibonacci():
    fibonacci = '''
    contract get_fib_n(n:int){
        let last_fib_calculated: int = 0;

        entry get_fib(n: int){
            let result: int = fib(n);
            last_fib_calculated = result;
        }

        func fib(n: int) : int{
            if (n <= 1) {
                return n;
            }
            else {
                let a: int = n - 1;
                let b: int = n - 2;
                return fib(a) + fib(b);
            }
        }
    }
    '''
    lexer = TzScriptLexer()
    tokens = list(lexer.tokenize(fibonacci))
    expected_tokens = [Token('contract',contract),Token('get_fib_n',idx),Token('(',opar),Token('n',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token('{',ocur),Token('let',let), Token('last_fib_calculated',idx), Token(':', colon), Token('int', typex), Token('=',equal),Token('0',num),Token(';',semi),Token('entry',entry),Token('get_fib',idx),Token('(',opar),Token('n',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token('{',ocur),Token('let',let),Token('result',idx), Token(':', colon), Token('int', typex),Token('=',equal),Token('fib',idx),Token('(',opar),Token('n',idx),Token(')',cpar),Token(';',semi),Token('last_fib_calculated',idx),Token('=',equal),Token('result',idx),Token(';',semi),Token('}',ccur),Token('func',func),Token('fib',idx),Token('(',opar),Token('n',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token(':',colon),Token('int',typex),Token('{',ocur),Token('if',ifx),Token('(',opar),Token('n',idx),Token('<=',lessthanequal),Token('1',num),Token(')',cpar),Token('{',ocur),Token('return',returnx),Token('n',idx),Token(';',semi),Token('}',ccur),Token('else',elsex),Token('{',ocur),Token('let', let), Token('a', idx), Token(':', colon), Token('int', typex), Token('=', equal), Token('n', idx), Token('-', minus), Token('1', num), Token(';', semi), Token('let', let), Token('b', idx), Token(':', colon), Token('int', typex), Token('=', equal), Token('n', idx), Token('-', minus), Token('2', num), Token(';', semi), Token('return',returnx),Token('fib',idx),Token('(',opar),Token('a',idx),Token(')',cpar),Token('+',plus),Token('fib',idx),Token('(',opar),Token('b',idx),Token(')',cpar),Token(';',semi),Token('}',ccur),Token('}',ccur),Token('}',ccur),Token('EOF',TZSCRIPT_GRAMMAR.EOF)]
    expected_lexes = [t.lex for t in expected_tokens if t.token_type != TZSCRIPT_GRAMMAR.EOF]
    expected_terminals = [t.token_type for t in expected_tokens if t.token_type != TZSCRIPT_GRAMMAR.EOF]
    lexes = [t.value for t in tokens]
    map_to_terminals_names = {'CONTRACT': contract.Name, 'ID': idx.Name, 'COLON': colon.Name, 'SEMICOLON': semi.Name, 'COMMA': comma.Name, 'INTEGER': num.Name, 'LPAREN': opar.Name, 'RPAREN': cpar.Name, 'LBRACE': ocur.Name, 'RBRACE': ccur.Name, 'LBRACKET': opar.Name, 'RBRACKET': cpar.Name, 'OR': plus.Name, 'AND': star.Name, 'OPERATOR': equal.Name, 'TERMINAL': typex.Name, 'NONTERMINAL': idx.Name, 'ENTRY': entry.Name, 'FUNC': func.Name, 'LET': let.Name, 'IF': ifx.Name, 'ELSE': elsex.Name, 'TYPE': typex.Name, 'STRING': typex.Name, 'NAT': typex.Name, 'INT': typex.Name, 'OPTIONAL': typex.Name, 'BOOL': typex.Name, 'RETURN': returnx.Name, 'MINUS': minus.Name, 'LESSTHANEQUAL': lessthanequal.Name, 'PLUS': plus.Name, 'STAR': star.Name, 'EQUAL': equal.Name, 'EOF': TZSCRIPT_GRAMMAR.EOF}
    terminals_names = []
    for token in tokens:
        print('hola')
        print(token.type)
        terminals_names.append(map_to_terminals_names[token.type])

    terminals = [TZSCRIPT_GRAMMAR[t] for t in terminals_names]
    assert lexes == expected_lexes
    assert terminals == expected_terminals