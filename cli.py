from typer import Typer, Argument
from visitors.string_rep_visitor import FormatVisitor
from visitors.semantic_check_visitor import SemanticCheckerVisitor
from visitors.high_level_ir_generator_visitor import TzScriptToHighLevelIrVisitor
from utils import run_tzscript_ast_building_pipeline
from visitors.michelson_generator_visitor import MichelsonGenerator
from visitors.hl_string_repre import HLReprVisitor
import typer


app = Typer()


def process(script: str, num_steps=1):
    with typer.progressbar(length=6) as progress:
        # Tokenize Script
        print("\nBuilding TZScript AST", end="")
        ast = run_tzscript_ast_building_pipeline(script)

        print("\nPerforming Semantic Check", end="")
        semantic_checker = SemanticCheckerVisitor()
        semantic_result = semantic_checker.visit(ast)
        if len(semantic_result) > 0:
            print("\nSomething Went Wrong")
            for err in semantic_result:
                print(err)
        else:
            print("... OK")
        progress.update(1)

        print("\nGenerating Intermediate Representation", end="")
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
