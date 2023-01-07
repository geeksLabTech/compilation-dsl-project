from typer import Typer, Argument
from lexer.sly_lexer import TzScriptLexer
from lexer.lex_token import Token
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR, idx, num, typex, contract, ifx, elsex, equal, plus, minus, star, div, semi, colon, comma, dot, opar, cpar, ocur, ccur, let, func, entry, equalequal, lessthan, greaterthan, lessthanequal, greaterthanequal
from parser.slr_parser import SLR1Parser, build_slr_ast
from visitors.type_check_visitor import TypeCheckVisitor
from visitors.scope_check_visitor import ScopeCheckVisitor
from visitors.semantic_check_visitor import SemanticCheckVisitor
from visitors.michelson_generator_visitor import MichelsonGeneratorVisitor
from visitors.string_rep_visitor import StringReprVisitor
import typer

map_to_terminals_names = {'CONTRACT': contract.Name, 'ID': idx.Name, 'COLON': colon.Name, 'SEMICOLON': semi.Name, 'COMMA': comma.Name, 'INTEGER': num.Name, 'LPAREN': opar.Name, 'RPAREN': cpar.Name, 'LBRACE': ocur.Name, 'RBRACE': ccur.Name, 'LBRACKET': opar.Name, 'RBRACKET': cpar.Name, 'OR': plus.Name, 'AND': star.Name, 'OPERATOR': equal.Name, 'TERMINAL': typex.Name, 'NONTERMINAL': idx.Name,
                          'ENTRY': entry.Name, 'FUNC': func.Name, 'LET': let.Name, 'IF': ifx.Name, 'ELSE': elsex.Name, 'TYPE': typex.Name, 'STRING': typex.Name, 'NAT': typex.Name, 'INT': typex.Name, 'OPTIONAL': typex.Name, 'BOOL': typex.Name, 'EQUALEQUAL': equalequal.Name, 'LESSTHAN': lessthan.Name, 'GREATERTHAN': greaterthan.Name, 'LESSTHANEQUAL': lessthanequal.Name, 'GREATERTHANEQUAL': greaterthanequal.Name, 'EQUAL': equal.Name}


app = Typer()


@app.command()
def build(file: str = Argument("", help="tzscript file to be parsed"),
          out_file: str = Argument(None, help='michelson file to be generated')):
    """ generates the .tz michelson script from the tzscript file specified """
    total = 7
    with typer.progressbar(length=total) as progress:
        with open(file, "r") as f:
            script = f.read()
        # print(script)
        # Tokenize Script
        print("\nTokenizing Script", end="")
        lexer = TzScriptLexer()
        tokens = list(lexer.tokenize(script))

        terminals = []

        for token in tokens:
            terminals.append(map_to_terminals_names[token.type])
        print("... OK")
        progress.update(1)

        # Parse tokenized Script
        print("\nParsing Script", end="")
        parser = SLR1Parser(TZSCRIPT_GRAMMAR, verbose=False)
        # print(tokens)
        # tokens = [Token('contract', contract), Token('store_value', idx), Token('(', opar), Token('value', idx), Token(':', colon), Token('int', typex), Token(')', cpar), Token('{', ocur), Token('let', let), Token('storage', idx), Token(':', colon), Token('int', typex), Token('=', equal), Token('0', num), Token(';', semi), Token(
        #     'entry', entry), Token('replace', idx), Token('(', opar), Token('new_value', idx), Token(':', colon), Token('int', typex), Token(')', cpar), Token('{', ocur), Token('storage', idx), Token('=', equal), Token('new_value', idx), Token(';', semi), Token('}', ccur), Token('}', ccur), Token('EOF', TZSCRIPT_GRAMMAR.EOF)]

        # terminals = [token.token_type for token in tokens]
        derivation = parser(terminals, True)
        if derivation is None:
            print(
                "Please re-run the command something unexpected (and unrelated to the parsing) happened")
            return
        productions, operations = derivation
        print("... OK")
        progress.update(1)

        print("\nBuilding AST", end="")
        ast = build_slr_ast(productions, operations, tokens)
        print("... OK")
        progress.update(1)

        print("\nPerforming Type Check", end="")
        type_visitor = TypeCheckVisitor()
        type_result = type_visitor.visit_program(ast)
        if not type_result:
            print("Something Went Wrong")
            return

        print("... OK")
        progress.update(1)

        print("\nPerforming Scope Check", end="")
        scope_visitor = ScopeCheckVisitor()
        scope_result = scope_visitor.visit_program(ast)
        if not scope_result:
            print("Something Went Wrong")
            return

        print("... OK")
        progress.update(1)

        print("\nPerforming Semantic Check", end="")
        semantic_visitor = SemanticCheckVisitor()
        semantic_result = semantic_visitor.visit_program(ast)
        if not semantic_result:
            print("\nSomething Went Wrong")
            return
        print("... OK")
        progress.update(1)

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
    total = 7
    with typer.progressbar(length=total) as progress:
        with open(file, "r") as f:
            script = f.read()
        # print(script)
        # Tokenize Script
        print("\nTokenizing Script", end="")
        lexer = TzScriptLexer()
        tokens = list(lexer.tokenize(script))

        terminals = []

        for token in tokens:
            terminals.append(map_to_terminals_names[token.type])
        print("... OK")
        progress.update(1)

        # Parse tokenized Script
        print("\nParsing Script", end="")
        parser = SLR1Parser(TZSCRIPT_GRAMMAR, verbose=False)
        print(tokens)
        # tokens = [Token('contract', contract), Token('store_value', idx), Token('(', opar), Token('value', idx), Token(':', colon), Token('int', typex), Token(')', cpar), Token('{', ocur), Token('let', let), Token('storage', idx), Token(':', colon), Token('int', typex), Token('=', equal), Token('0', num), Token(';', semi), Token(
        #     'entry', entry), Token('replace', idx), Token('(', opar), Token('new_value', idx), Token(':', colon), Token('int', typex), Token(')', cpar), Token('{', ocur), Token('storage', idx), Token('=', equal), Token('new_value', idx), Token(';', semi), Token('}', ccur), Token('}', ccur), Token('EOF', TZSCRIPT_GRAMMAR.EOF)]

        # terminals = [token.token_type for token in tokens]
        derivation = parser(terminals, True)
        if derivation is None:
            print(
                "Please re-run the command something unexpected (and unrelated to the parsing) happened")
            return
        productions, operations = derivation
        print("... OK")
        progress.update(1)

        print("\nBuilding AST", end="")
        ast = build_slr_ast(productions, operations, tokens)
        print("... OK")
        progress.update(1)

        print("\nPerforming Type Check", end="")
        type_visitor = TypeCheckVisitor()
        type_result = type_visitor.visit_program(ast)
        if not type_result:
            print("Something Went Wrong")
            return

        print("... OK")
        progress.update(1)

        print("\nPerforming Scope Check", end="")
        scope_visitor = ScopeCheckVisitor()
        scope_result = scope_visitor.visit_program(ast)
        if not scope_result:
            print("Something Went Wrong")
            return

        print("... OK")
        progress.update(1)

        print("\nPerforming Semantic Check", end="")
        semantic_visitor = SemanticCheckVisitor()
        semantic_result = semantic_visitor.visit_program(ast)
        if not semantic_result:
            print("Something Went Wrong")
            return
        print("... OK")
        progress.update(1)

        print("\nGenerating String representation Code", end="")
        string_repr = StringReprVisitor()
        string_repr.visit_program(ast)
        if out_file is None:
            out_file = file[:file.find(".tzs")]+".tzs.rep"
        with open(out_file, "w") as f:
            f.write(string_repr.result)
        print(f"Generated {out_file}")
        progress.update(1)


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
