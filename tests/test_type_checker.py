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
    productions, operations = derivation

    ast = build_slr_ast(productions, operations, tokens)

    type_visitor = TypeCheckVisitor()
    type_result = type_visitor.visit_program(ast)
    return type_result


def test_type_string():
    script = """contract get_fib_n(n:int){
            let last_fib_calculated: int = 0;
            let last: string = 1;

            entry get_fib(n: int){
                let result: int = fib(n);
                last_fib_calculated = result;
            }

            func fib(n: int) : int{
                if (n <= 1) {
                    return n;
                }
                else {
                    let a: int = n - "a";
                    let b: int = n - 2;
                    return fib(a) + fib(b);

                }

            }
        }"""

    type_result = process(script)
    assert len(type_result) == 2
    assert type_result[0][0] == 'Incompatible types in variable declaration: expected string, got num'
    assert type_result[1][0] == "Cannot permform '-' operation between int and string"


def test_type_int():
    script = """contract get_fib_n(n:int){
            let last_fib_calculated: int = "3";
            
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
        }"""

    type_result = process(script)
    assert len(type_result) == 1
    assert type_result[0][0] == 'Incompatible types in variable declaration: expected int, got string'


def test_type_nat():
    script = """contract get_fib_n(n:int){
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
                    let a: nat = 0 - 1;
                    let b: int = n - 2;
                    return fib(a) + fib(b);

                }

            }
        }"""

    type_result = process(script)

    assert len(type_result) == 1
    assert type_result[0][0] == "Value -1 cannot be assigned to 'nat' type variable"


def test_return_func():
    script = """contract get_fib_n(n:int){
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
                return "fib(a) + fib(b)";
            }
        }
        
    }"""

    type_result = process(script)
    assert len(type_result) == 1
    assert type_result[0][0] == "Invalid return type for function call fib expected int, got string"
