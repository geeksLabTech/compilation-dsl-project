
from lexer.sly_lexer import TzScriptLexer, process_lexer_tokens 
from parser.tzscript_grammar import TZSCRIPT_GRAMMAR
from parser.slr_parser import SLR1Parser, build_slr_ast
from parser.lr_parser import LR1Parser

# from typing import Self
from grammar import EOF, Epsilon, Grammar, Production, Sentence, Symbol
import hashlib
import base58
PARSER = LR1Parser(TZSCRIPT_GRAMMAR, verbose=True)

def run_tscript_sly_lexer_pipeline(script: str):
    lexer = TzScriptLexer()
    lexer_tokens = list(lexer.tokenize(script))
    tokens = process_lexer_tokens(lexer_tokens)
    return tokens

def run_tzscript_slr_parser_pipeline(script: str):
    tokens = run_tscript_sly_lexer_pipeline(script)

    parser = SLR1Parser(TZSCRIPT_GRAMMAR, verbose=True)

    terminals = [token.token_type for token in tokens]
    derivation = parser(terminals, True)
    assert derivation is not None 
    productions, operations = derivation
    return productions, operations, tokens

def run_tzscript_lr_parser_pipeline(script: str):
    tokens = run_tscript_sly_lexer_pipeline(script)
    terminals = [token.token_type for token in tokens]
    derivation = PARSER(terminals, True)
    assert derivation is not None 
    productions, operations = derivation
    return productions, operations, tokens


def run_tzscript_ast_building_pipeline(script: str):
    productions, operations, tokens = run_tzscript_lr_parser_pipeline(script)
    ast = build_slr_ast(productions, operations, tokens)
    assert ast is not None
    return ast


def inspect(item, grammar_name='G', mapper=None):
    try:
        return mapper[item]
    except (TypeError, KeyError):
        if isinstance(item, dict):
            items = ',\n   '.join(
                f'{inspect(key, grammar_name, mapper)}: {inspect(value, grammar_name, mapper)}' for key, value in item.items())
            return f'{{\n   {items} \n}}'
        elif isinstance(item, ContainerSet):
            args = f'{ ", ".join(inspect(x, grammar_name, mapper) for x in item.set) } ,' if item.set else ''
            return f'ContainerSet({args} contains_epsilon={item.contains_epsilon})'
        elif isinstance(item, EOF):
            return f'{grammar_name}.EOF'
        elif isinstance(item, Epsilon):
            return f'{grammar_name}.Epsilon'
        elif isinstance(item, Symbol):
            return f"G['{item.Name}']"
        elif isinstance(item, Sentence):
            items = ', '.join(inspect(s, grammar_name, mapper)
                              for s in item._symbols)
            return f'Sentence({items})'
        elif isinstance(item, Production):
            left = inspect(item.Left, grammar_name, mapper)
            right = inspect(item.Right, grammar_name, mapper)
            return f'Production({left}, {right})'
        elif isinstance(item, tuple) or isinstance(item, list):
            ctor = ('(', ')') if isinstance(item, tuple) else ('[', ']')
            return f'{ctor[0]} {("%s, " * len(item)) % tuple(inspect(x, grammar_name, mapper) for x in item)}{ctor[1]}'
        else:
            raise ValueError(f'Invalid: {item}')


def pprint(item, header=""):
    if header:
        print(header)

    if isinstance(item, dict):
        for key, value in item.items():
            print(f'{key}  --->  {value}')
    elif isinstance(item, list):
        print('[')
        for x in item:
            print(f'   {repr(x)}')
        print(']')
    else:
        print(item)


def base58check_decode(encoded):
    # Decode the encoded string using base58 decoding
    decoded = base58.b58decode(encoded)

    # Extract the version byte, payload, and checksum
    version = decoded[0]
    payload = decoded[1:-4]
    st = decoded[:-4]
    checksum = decoded[-4:]

    # Calculate double SHA-256 hash of the version payload
    first_hash = hashlib.sha256(st).digest()
    second_hash = hashlib.sha256(first_hash).digest()

    # Take the first 4 bytes of the second hash as the calculated checksum
    calculated_checksum = second_hash[:4]

    # Verify that the calculated checksum matches the original checksum
    if calculated_checksum != checksum:
        raise ValueError("Invalid checksum")

    return version, payload


def is_valid_tezos_address(address):
    # Check if address is a valid Base58 encoded string
    try:
        version, payload = base58check_decode(address)
    except ValueError:
        return False

    # Check if version byte corresponds to Tezos address format
    if version not in [6, 7, 8]:
        return False

    return True
