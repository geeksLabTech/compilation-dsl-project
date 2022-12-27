from lexer.sly_lexer import TzScriptLexer

def func():
    data = '''
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
    
    lexer = TzScriptLexer()    
    lexer_tokens = []
    for tok in lexer.tokenize(data):
        lexer_tokens.append(tok)
        # print('type=%r, value=%r' % (tok.type, tok.value))

    return lexer_tokens

def test_answer():
    data = '''
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
    
    lexer = TzScriptLexer()    
    lexer_tokens = []
    for tok in lexer.tokenize(data):
        lexer_tokens.append(tok)
        # print('type=%r, value=%r' % (tok.type, tok.value))
    
    for i, idx in enumerate(func()):
        assert idx.type == lexer_tokens[i].type 