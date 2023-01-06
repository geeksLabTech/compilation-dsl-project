from lexer.sly_lexer import TzScriptLexer
from lexer.lex_token import Token
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR,idx, num, typex, contract, ifx, elsex,equal, plus, minus, star, div,semi, colon, comma, dot, opar, cpar, ocur, ccur,let, func,entry
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