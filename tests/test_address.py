from typer import Typer, Argument
from lexer.sly_lexer import TzScriptLexer, process_lexer_tokens
from lexer.lex_token import Token
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR, idx, num, typex, contract, ifx, elsex, equal, plus, returnx, minus, star, div, semi, colon, comma, dot, opar, cpar, ocur, ccur, let, func, entry, equalequal, lessthan, greaterthan, lessthanequal, greaterthanequal
from parser.slr_parser import SLR1Parser, build_slr_ast
from visitors.type_check_visitor import TypeCheckVisitor
import pytest


def process(script):
    # Tokenize Script
    lexer = TzScriptLexer()
    lexer_tokens = list(lexer.tokenize(script))
    tokens = process_lexer_tokens(lexer_tokens)

    terminals = [t.token_type for t in tokens]

    # Parse tokenized Script
    parser = SLR1Parser(TZSCRIPT_GRAMMAR, verbose=False)
    derivation = parser(terminals, True)
    # print(derivation)
    assert not derivation is None
    productions, operations = derivation

    ast = build_slr_ast(productions, operations, tokens)

    type_visitor = TypeCheckVisitor()
    type_result = type_visitor.visit_program(ast)
    return type_result


def test_type_addr_string():
    script = """contract get_fib_n(n:int){
        let ad:address = "aaa";
        let last_fib_calculated: int = 1 ;

        entry get_fib(n: int){
            let result: int = fib(n);
            last_fib_calculated = result;
        }

        func fib(n: int) : int{
            else {
                let a: nat = n - 1;
                let b: int = n - 2;
                return fib(a) + fib(b);
            }
        }
        
    }"""

    type_result = process(script)
    assert type_result[0][0] == 'Incompatible types in variable declaration: expected address, got string'


def test_type_addr_string():
    script = """contract get_fib_n(n:int){
        let ad:address = "tz1QV341nbgxbyzd8SYU7fJtNScaLVPMZkGC";
        let last_fib_calculated: int = 1 ;

        entry get_fib(n: int){
            let result: int = fib(n);
            last_fib_calculated = result;
        }

        func fib(n: int) : int{
            else {
                let a: nat = n - 1;
                let b: int = n - 2;
                return fib(a) + fib(b);
            }
        }
        
    }"""

    type_result = process(script)
    assert len(type_result) == 0


def test_type_addr_string():
    script = """contract get_fib_n(n:int){
        let ad:address = "tz1QV341nbgxbyzdsSYU7fJtNScaLVPMZkGC";
        let last_fib_calculated: int = 1 ;

        entry get_fib(n: int){
            let result: int = fib(n);
            last_fib_calculated = result;
        }

        func fib(n: int) : int{
            else {
                let a: nat = n - 1;
                let b: int = n - 2;
                return fib(a) + fib(b);
            }
        }
        
    }"""

    type_result = process(script)
    assert len(type_result) == 1
    assert type_result[0][0] == "Invalid Tezos Address"
