from typer import Typer, Argument
from lexer.sly_lexer import TzScriptLexer, process_lexer_tokens
from lexer.lex_token import Token
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR, idx, num, typex, contract, ifx, elsex, equal, plus, returnx, minus, star, div, semi, colon, comma, dot, opar, cpar, ocur, ccur, let, func, entry, equalequal, lessthan, greaterthan, lessthanequal, greaterthanequal
from parser.slr_parser import SLR1Parser, build_slr_ast
from visitors.type_check_visitor import TypeCheckVisitor
from visitors.scope_check_visitor import ScopeCheckVisitor
from visitors.semantic_check_visitor import SemanticCheckerVisitor
from visitors.michelson_generator_visitor import MichelsonGeneratorVisitor
from visitors.string_rep_visitor import FormatVisitor
from visitors.index_visitor import IndexVisitor
import typer

fibonacci = '''contract get_fib_n(n:int){
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
        
    }'''

app = Typer()


def process(script: str):
    with typer.progressbar(length=7) as progress:
        # Tokenize Script
        print("\nTokenizing Script", end="")
        lexer = TzScriptLexer()
        lexer_tokens = list(lexer.tokenize(script))
        tokens = process_lexer_tokens(lexer_tokens)
        print("... OK")
        progress.update(1)

        terminals = [t.token_type for t in tokens]
        terminals_loc = [(t.line_no, t.col_no) for t in tokens]
        loc = []

        for i, tok in enumerate(terminals):
            if not str(tok) in ['(', ':', ')', '}', '{', ';', '\"']:
                loc.append((tok, terminals_loc[i]))

        # Parse tokenized Script
        print("\nParsing Script", end="")
        parser = SLR1Parser(TZSCRIPT_GRAMMAR, verbose=False)
        # print(lexer_tokens)
        # tokens = [Token('contract', contract), Token('store_value', idx), Token('(', opar), Token('value', idx), Token(':', colon), Token('int', typex), Token(')', cpar), Token('{', ocur), Token('let', let), Token('storage', idx), Token(':', colon), Token('int', typex), Token('=', equal), Token('0', num), Token(';', semi), Token(
        #     'entry', entry), Token('replace', idx), Token('(', opar), Token('new_value', idx), Token(':', colon), Token('int', typex), Token(')', cpar), Token('{', ocur), Token('storage', idx), Token('=', equal), Token('new_value', idx), Token(';', semi), Token('}', ccur), Token('}', ccur), Token('EOF', TZSCRIPT_GRAMMAR.EOF)]

        # terminals = [token.token_type for token in tokens]
        derivation = parser(terminals, terminals_loc, True)
        if derivation is None:
            print(
                "Something unexpected happened during parsing")
            return
        productions, operations = derivation
        print("... OK")
        progress.update(1)

        print("\nBuilding AST", end="")
        ast = build_slr_ast(productions, operations, tokens)
        print("... OK")
        progress.update(1)

        index_visitor = IndexVisitor(loc)
        for i, val in enumerate(loc):
            print((i, val))
        final_dict = index_visitor.visit_program(ast)
        print(index_visitor.final_dict)

        print("\nPerforming Type Check", end="")
        type_visitor = TypeCheckVisitor()
        type_result = type_visitor.visit_program(ast)
        if len(type_result) > 0:

            print("\nSomething Went Wrong")

            for err in type_result:
                print(err)
        else:
            print("... OK")
        progress.update(1)

        # print("\nPerforming Scope Check", end="")
        # scope_visitor = ScopeCheckVisitor()
        # scope_result = scope_visitor.visit_program(ast)
        # if not scope_result:
        #     print("Something Went Wrong")
        #     return

        # print("... OK")
        progress.update(1)

        print("\nPerforming Semantic Check", end="")
        semantic_visitor = SemanticCheckerVisitor()
        semantic_result = semantic_visitor.visit(ast)
        if len(semantic_result) > 0:

            print("\nSomething Went Wrong")

            for err in semantic_result:
                print(err)
        else:
            print("... OK")
        progress.update(1)

        return ast, progress


@app.command()
def build(file: str = Argument("", help="tzscript file to be parsed"),
          out_file: str = Argument(None, help='michelson file to be generated')):
    """ generates the .tz michelson script from the tzscript file specified """

    with open(file, "r", encoding='utf-8') as f:
        script = f.read()

    ast, progress = process(script)

    print("\nGenerating Michelson Code", end="")
    # TODO uncomment this when code generation is working OK
    # michelson_generator = MichelsonGeneratorVisitor()
    # michelson_generator.visit_program(ast)
    # michelson_result = michelson_geneator.result
    michelson_result = "NOT IMPLEMENTED YET"
    if out_file is None:
        out_file = file[:file.find(".tzs")]+".tz"
    with open(out_file, "w") as f:
        f.write(michelson_result)
    print(f"\nGenerated {out_file}")
    progress.update(1)


@app.command()
def represent(file: str = Argument("", help="tzscript file to be parsed"),
              out_file: str = Argument(None, help='michelson file to be generated')):
    """ generates the .tzs.repr the string representation of the code in the input """

    # with typer.progressbar(length=total) as progress:
    with open(file, "r") as f:
        script = f.read()

    ast, progress = process(script)

    print("\nGenerating String representation Code")
    string_repr = FormatVisitor()
    result = string_repr.visit(ast)
    if out_file is None:
        out_file = file[:file.find(".tzs")]+".tzs.rep"
    with open(out_file, "w") as f:
        f.write(result)
    progress.update(1)
    print(f"\nGenerated {out_file}")


@app.command()
def build_run(file: str = Argument("", help="tzscript file to be parsed"),
              out_file: str = Argument(None, help='michelson file to be generated and runned')):
    """ generates the .tz michelson script from the tzscript file specified and executes it"""
    build(file, out_file)
    print("Executing file...")
    # Run out_file
    # TODO make the run script


@app.command()
def run(file: str = Argument(None, help='michelson file to be runned')):
    print("Executing file...")
    # Run out_file
    # TODO make the run script


if __name__ == "__main__":
    app()
