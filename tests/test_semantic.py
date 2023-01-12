import pytest
from lexer.sly_lexer import TzScriptLexer, process_lexer_tokens 
from lexer.lex_token import Token
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR,idx, num, typex, contract, ifx, elsex,equal, plus, minus, star, div,semi, colon, comma, dot, opar, cpar, ocur, ccur,let, func,entry,lessthanequal,greaterthanequal, iniquelaty, lessthan,greaterthan,equalequal, returnx
from parser.slr_parser import SLR1Parser, build_slr_ast
from visitors.string_rep_visitor import FormatVisitor
from visitors.semantic_check_visitor import SemanticCheckerVisitor





def test():
    badscript = '''contract get_fib_n(n:int){
    let last_fib_calculated : int = 0;

    entry get_fib(n: int){
        let result: int = fib(n);
        last_fib_calculated = result;
        let a : int = b;
    }

    func fib(n: int) : int{
        let x : int = last_fib_calculated;
        if (n <= 1) {
            return n;
        }
        else {
            
            let a: int = n - 1;
            let b: int = n - 2;
            return fib(a) + fib(b);
        }
    }

    func fib(n: int) : int{
        let x : int = last_fib_calculated;
    }
    }'''
    lexer = TzScriptLexer()
    lexer_tokens = list(lexer.tokenize(badscript))
    tokens = process_lexer_tokens(lexer_tokens)

    parser = SLR1Parser(TZSCRIPT_GRAMMAR, verbose=True)

    terminals = [token.token_type for token in tokens]
    derivation = parser(terminals, True)
    productions, operations = derivation
    ast = build_slr_ast(productions, operations, tokens)
    format = FormatVisitor()
    semantic_checker = SemanticCheckerVisitor()
    semantic_checker.visit(ast)

    assert(semantic_checker.errors == ['In the corpus of the program declare entry functions or variables not this constant 0',
 'Invalid variable b',
 'Function fib is defined after entry point',
 'Invalid variable last_fib_calculated',
 'Function name fib is used',
 'Function fib is defined after entry point',
 'Invalid variable last_fib_calculated'])
