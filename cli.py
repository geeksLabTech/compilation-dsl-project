from typer import Typer, Argument
from lexer.sly_lexer import TzScriptLexer, process_lexer_tokens
from lexer.lex_token import Token
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR, idx, num, typex, contract, ifx, elsex, equal, plus, returnx, minus, star, div, semi, colon, comma, dot, opar, cpar, ocur, ccur, let, func, entry, equalequal, lessthan, greaterthan, lessthanequal, greaterthanequal
from parser.slr_parser import SLR1Parser, build_slr_ast
# from parser.ll_parser import LLParser
from visitors.type_check_visitor import TypeCheckVisitor
from visitors.scope_check_visitor import ScopeCheckVisitor
from visitors.semantic_check_visitor import SemanticCheckerVisitor
from visitors.michelson_generator_visitor import MichelsonGenerator
from visitors.string_rep_visitor import FormatVisitor
from visitors.index_visitor import IndexVisitor
from visitors.high_level_ir_generator_visitor import TzScriptToHighLevelIrVisitor
from visitors.hl_string_repre import HLReprVisitor
from visitors.michelson_generator_visitor import MichelsonGenerator
import typer

app = Typer()


def process(script: str, num_steps=6):
    with typer.progressbar(length=6) as progress:
        # Tokenize Script
        print("\nTokenizing Script", end="")
        lexer = TzScriptLexer()
        lexer_tokens = list(lexer.tokenize(script))
        tokens = process_lexer_tokens(lexer_tokens)
        print("... OK")
        progress.update(1)

        terminals = [t.token_type for t in tokens]
        terminals_loc = [t.line_no for t in tokens]
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
        derivation = parser(terminals, True)
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
        # for i, val in enumerate(loc):
        #     print((i, val))
        final_dict = index_visitor.visit_program(ast)
        # print(index_visitor.final_dict)

        print("\nPerforming Type Check", end="")
        type_visitor = TypeCheckVisitor()
        type_result = type_visitor.visit_program(ast)
        if len(type_result) > 0:

            print("\nSomething Went Wrong")

            for err in type_result:
                try:
                    print(err[0], "at line", final_dict[err[1]])
                except:
                    print(err[0])
        else:
            print("... OK")
        progress.update(1)

        print("\nPerforming Semantic Check", end="")
        semantic_visitor = SemanticCheckerVisitor()
        semantic_result = semantic_visitor.visit(ast)
        if len(semantic_result) > 0:

            print("\nSomething Went Wrong")

            for err in semantic_result:

                try:
                    print(err[0], "at line", final_dict[err[1]])
                except:
                    print(err[0])
        else:
            print("... OK")
        progress.update(1)

        print("Generating Intermediate Representation", end="")
        high_level_ir = TzScriptToHighLevelIrVisitor()
        ir = high_level_ir.visit(ast)
        print("...OK")
        progress.update(1)

        return ast, ir, progress


@app.command()
def build(file: str = Argument("", help="tzscript file to be parsed"),
          out_file: str = Argument(None, help='michelson file to be generated')):
    """ generates the .tz michelson script from the tzscript file specified """

    with open(file, "r", encoding='utf-8') as f:
        script = f.read()

    ast, ir, progress = process(script, 6)

    print("\nGenerating Michelson Code", end="")
    # TODO uncomment this when code generation is working OK
    visit_generator = MichelsonGenerator()
    visit_generator.visit(ir)
    # michelson_result = michelson_geneator.result
    michelson_result = visit_generator.code
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

    ast, ir, progress = process(script, 7)

    print("\nGenerating String representation Code for base AST")
    string_repr = FormatVisitor()
    result = str(string_repr.visit(ast))
    if out_file is None:
        out_file = file[:file.find(".tzs")]+".tzs.rep"
    with open(out_file, "w") as f:

        f.write(result)
    progress.update(1)

    print("\nGenerating String representation Code for intermediate AST")
    hl_repr = HLReprVisitor()
    result = hl_repr.visit(ir)
    if out_file is None:
        out_file = file[:file.find(".tzs")]+".tzs.rep"
    with open(out_file, "a+") as f:
        f.write("\n\n")
        f.write(str(result))
    progress.update(1)
    print(f"\nGenerated {out_file}")


if __name__ == "__main__":
    app()
