from lexer.sly_lexer import TzScriptLexer
from lexer.lex_token import Token
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR, contract, idx, opar, cpar, colon, typex, equal, num, semi, entry, ocur, let, ccur
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
    tokens = lexer.tokenize(hello_world)
    
    expected_tokens = [Token('contract', contract),Token('store_value',idx),Token('(',opar),Token('value',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token('{',ocur),Token('let',let),Token('storage',idx),Token(':',colon),Token('int',typex),Token('=',equal),Token('0',num),Token(';',semi),Token('entry',entry),Token('replace',idx),Token('(',opar),Token('new_value',idx),Token(':',colon),Token('int',typex),Token(')',cpar),Token('{',ocur),Token('storage',idx),Token('=',equal),Token('new_value',idx),Token(';',semi),Token('}',ccur),Token('}',ccur),Token('EOF',TZSCRIPT_GRAMMAR.EOF)]
    expected_lexes = [t.lex for t in expected_tokens if t.token_type != TZSCRIPT_GRAMMAR.EOF]
    expected_terminals = [t.token_type for t in expected_tokens if t.token_type != TZSCRIPT_GRAMMAR.EOF]
    lexes = [t.value for t in tokens]
    terminals = [t.type for t in tokens]
    assert lexes == expected_lexes
    assert terminals == expected_terminals
    
# def func():
#     data = '''
#     contract hello_world () {
#         var msg : string = "Hello";
#         entry input(name: string) {
#             if (len(msg) > 5) {
#                 msg = msg + " " + name;
#             }
#             else {
#                 msg = msg + "," + " " + name;
#             }
#         }
#     }
#     '''
    
#     lexer = TzScriptLexer()    
#     lexer_tokens = []
#     for tok in lexer.tokenize(data):
#         lexer_tokens.append(tok)
#         # print('type=%r, value=%r' % (tok.type, tok.value))

#     return lexer_tokens

# def test_answer():
#     data = '''
#     contract hello_world () {
#         var msg : string = "Hello";
#         entry input(name: string) {
#             if (len(msg) > 5) {
#                 msg = msg + " " + name;
#             }
#             else {
#                 msg = msg + "," + " " + name;
#             }
#         }
#     }
#     '''
    
#     lexer = TzScriptLexer()    
#     lexer_tokens = []
#     for tok in lexer.tokenize(data):
#         lexer_tokens.append(tok)
#         # print('type=%r, value=%r' % (tok.type, tok.value))
    
#     for i, idx in enumerate(func()):
#         assert idx.type == lexer_tokens[i].type 