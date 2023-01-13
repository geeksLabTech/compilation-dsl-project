from lexer.sly_lexer import TzScriptLexer, process_lexer_tokens
from lexer.lex_token import Token
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR, idx, num, typex, contract, ifx, elsex, equal, plus, returnx, minus, star, div, semi, colon, comma, dot, opar, cpar, ocur, ccur, let, func, entry, equalequal, lessthan, greaterthan, lessthanequal, greaterthanequal
from parser.slr_parser import SLR1Parser, build_slr_ast
from visitors.type_check_visitor import TypeCheckVisitor
from visitors.scope_check_visitor import ScopeCheckVisitor
from visitors.semantic_check_visitor import SemanticCheckerVisitor
from visitors.michelson_generator_visitor import MichelsonGenerator
from visitors.string_rep_visitor import FormatVisitor
from visitors.index_visitor import IndexVisitor
from visitors.high_level_ir_generator_visitor import TzScriptToHighLevelIrVisitor
from visitors.hl_string_repre import HLReprVisitor
from visitors.michelson_generator_visitor import MichelsonGenerator
import pytest

def process(script):
    lexer = TzScriptLexer()
    lexer_tokens = list(lexer.tokenize(script))
    tokens = process_lexer_tokens(lexer_tokens)
    terminals = [t.token_type for t in tokens]
    terminals_loc = [t.line_no for t in tokens]
    loc = []
    for i, tok in enumerate(terminals):
        if not str(tok) in ['(', ':', ')', '}', '{', ';', '\"']:
            loc.append((tok, terminals_loc[i]))
    # Parse tokenized Script
    parser = SLR1Parser(TZSCRIPT_GRAMMAR, verbose=False)
    # print(lexer_tokens)
    # tokens = [Token('contract', contract), Token('store_value', idx), Token('(', opar), Token('value', idx), Token(':', colon), Token('int', typex), Token(')', cpar), Token('{', ocur), Token('let', let), Token('storage', idx), Token(':', colon), Token('int', typex), Token('=', equal), Token('0', num), Token(';', semi), Token(
    #     'entry', entry), Token('replace', idx), Token('(', opar), Token('new_value', idx), Token(':', colon), Token('int', typex), Token(')', cpar), Token('{', ocur), Token('storage', idx), Token('=', equal), Token('new_value', idx), Token(';', semi), Token('}', ccur), Token('}', ccur), Token('EOF', TZSCRIPT_GRAMMAR.EOF)]
    # terminals = [token.token_type for token in tokens]
    derivation = parser(terminals, True)
    assert derivation is not None
    productions, operations = derivation
    ast = build_slr_ast(productions, operations, tokens)
    index_visitor = IndexVisitor(loc)
    # for i, val in enumerate(loc):
    #     print((i, val))
    final_dict = index_visitor.visit_program(ast)
    # print(index_visitor.final_dict)
    type_visitor = TypeCheckVisitor()
    type_result = type_visitor.visit_program(ast)
    assert len(type_result) == 0
    semantic_visitor = SemanticCheckerVisitor()
    semantic_result = semantic_visitor.visit(ast)
    assert len(semantic_result) == 0
    high_level_ir = TzScriptToHighLevelIrVisitor()
    ir = high_level_ir.visit(ast)

    visit_generator = MichelsonGenerator()
    visit_generator.visit(ir)
    # michelson_result = michelson_geneator.result
    return visit_generator.code


def test_basic_sum():
    code = """contract sum_2nums(n:int){
    let x: int = 0;

    entry sum(n:int){
        let a: int = 2;
        let b: int = 3;
        x = a + b;
    }

    }"""

    expected_result = """parameter int %sum;
storage int;
code {
UNPAIR;
PUSH int 2;
PUSH int 3;
DIG 1;
DIG 1;
ADD;
DIG 0;
DROP
NIL operation;
PAIR;
}
"""
    assert process(code) == expected_result
