from utils import run_tzscript_ast_building_pipeline

import pytest

from visitors.semantic_check_visitor import SemanticCheckerVisitor

def test_type_in_while_if_expr():
    script = '''
    contract get_fib_n(n:int){
        let last_fib_calculated: int;

        entry get_fib(n: int){
            let result: int = 2;
            while (result+2) {
                result = result + 1;
            }
            if (2) {
                then{result = result + 1;}
            }
            if (2-4*5) {
                then{result = result + 1;}
            }
            while (4*5 <= 2/3 ) {
                result = result + 1;
            }
            if (2-4*5 >= 2-3) {
                then{result = result + 1;}
            }
        }
    }
    '''

    ast = run_tzscript_ast_building_pipeline(script)
    errors = SemanticCheckerVisitor().visit(ast)
    expected_errors = ['while expression must be boolean, line 7',
 'if expression must be boolean at line 10',
 'if expression must be boolean at line 13']
    assert errors == expected_errors


def test_function_return_types():

    script = '''
    contract test_return_types(){
        let temp: int;

        entry double(a: int){
            let b: int = sum(a,a);
            let text: string = "hola";
            let c: int = get_hello(text);
            let d: int = sum(a,b) + 2 + get_hello(text);
            let e: nat = sum(a,b) + 2 * 9;
            let f: nat = sum_nat(a,b) - 1;
            
        }

        func sum(a:int, b:int): int{
            return 3 * 4 - 8;
        }

        func substract(a:int, b:int): int{
            let x: string = "test";
            return x;
        }

        func get_hello(a:string): string{
            return a;
        }

        func sum_nat(a:nat, b:nat): nat{
            return a + b;
        }

    }
    '''

    ast = run_tzscript_ast_building_pipeline(script)
    errors = SemanticCheckerVisitor().visit(ast)
    expected_errors = ['Variable type int of c is not compatible with string at line 8',
 ('Invalid types int and string for arithmetic operation at line 9',
  'PlusNode'),
  'Variable type nat of e is not compatible with int at line 10',
 'Invalid argument type int for function sum_nat at line 11, expected nat',
 'Invalid return type string for function substract']
    assert errors == expected_errors


def test_expression_types():
    script = '''
    contract test_expr_types(){
        let temp: nat;

        entry double(a: int, b:nat, c:string, d:bool){
            temp = 5 - 8;
            let e: nat = b - a;
            let f: nat = a - b;
            c = True;
            let g: int = a + b * d;
            d = False;
            let x: int = 2*5-4<10/5;
            let y: bool = a-b >= 2;

        }
    }
    '''
    ast = run_tzscript_ast_building_pipeline(script)
    errors = SemanticCheckerVisitor().visit(ast)
    expected_errors = ['Invalid type int for variable temp at line 6',
 'Variable type nat of e is not compatible with int at line 7',
 'Variable type nat of f is not compatible with int at line 8',
 'Invalid type bool for variable c at line 9',
 ('Invalid types nat and bool for arithmetic operation at line 10',
  'StarNode'),
 'Variable type int of x is not compatible with bool at line 12']
    assert errors == expected_errors


def test_address_type():
    script = '''
    contract test_address_type(){
        let temp: address;

        entry test_entry(a: int, b:nat, c:string, d:bool, e:address){
            temp = c;
            let f: address = e;
            let x: string = c + e;
            let y: address = "tz1icNwg34VPyWJevGRBz56r19MiqYeJQaxU";
            let z: address = "hola mundo";
            let z: address = y + z;
            let s: string = "hello";
            let v: address = test_func(s);
        }

        func test_func(a: address): address{
            return a;
        }
    }
    '''
    ast = run_tzscript_ast_building_pipeline(script)
    errors = SemanticCheckerVisitor().visit(ast)
    expected_errors = ['Invalid type string for variable temp at line 6',
 ('Invalid types string and address for arithmetic operation at line 8',
  'PlusNode'),
 'Variable type address of z is not compatible with string at line 10',
 'Variable z is used, error in line 11',
 ('Invalid types address and address for arithmetic operation at line 11',
  'PlusNode'),
 'Invalid argument type string for function test_func at line 13, expected address']
    assert errors == expected_errors