from utils import run_tzscript_ast_building_pipeline

import pytest

from visitors.semantic_check_visitor import SemanticCheckerVisitor

def test_global_entry_and_func_definition():
    script = '''
    contract get_fib_n(n:int){
        let last_fib_calculated: int;

        func test_func(n: int) : int{
            return n;
        }

        entry get_fib(n: int){
            let result: int = 2;
        }

        func test_func(b: int): int{
            return b;
        }

        entry get_fib(c: int){
            let result: int = 2;
        }
    }
    '''
    ast = run_tzscript_ast_building_pipeline(script)
    errors = SemanticCheckerVisitor().visit(ast)
    expected_errors = ['Function test_func is already defined, error in line 13',
 'Entry point get_fib is already defined, error in line 17']
    assert errors == expected_errors


def test_global_scope():
    script = '''contract get_fib_n(n:int){

    let first: int;
    
    func fib(n: int) : int{
        let x : int = last_fib_calculated;
        if (n <= 1) {
            then{return n;}
            else {
                
                let a: int = n - 1;
                let b: int = n - 2;
                return fib(a) + fib(b);
            }
        }
    }

    let last_fib_calculated : int ;

    entry get_fib(n: int){
        let result: int = fib(n);
        last_fib_calculated = result;
        let a : int = b;
        let c : int = first;
    }
    }'''

    ast = run_tzscript_ast_building_pipeline(script)
    errors = SemanticCheckerVisitor().visit(ast)
    expected_errors = ['Variable last_fib_calculated at line 6 is not defined', 'Variable b at line 23 is not defined']
    assert errors == expected_errors

def test_scope_with_if_and_while():
    script = '''contract get_fib_n(n:int){

    let first: int;
    let last_fib_calculated : int ;
    
    func if_test(n: int) : int{
        let x : int = last_fib_calculated;
        if (n <= 1) {
            then{let v: int = 1;}
            
        }
        let a: int = v;
    }

    entry get_fib(n: int){
        let result: int = if_test(n);
        last_fib_calculated = result;
        let a : int = b;
        let c : int = first;
    }

    func while_test(x: int): int{
        let count: int = 0;
        while (2+3<4){
            count = count + 1;
            let temp: int = count;
        }
        let a: int = temp;
    }

    func else_test(y: int) : int{
        if (2+3<4){
            then{let a: int = 1;}
            else{let b: int = 2;}
        }
        let c: int = b;
    }
    func if_else_test(z:int): int{
        if (2+3<4){
            then{let a: int = 1;}
            else{let b: int = a;}
        }
    }
    }'''

    ast = run_tzscript_ast_building_pipeline(script)
    errors = SemanticCheckerVisitor().visit(ast)
    expected_errors = ['Variable last_fib_calculated at line 7 is not defined',
 'Variable v at line 12 is not defined',
 'Variable b at line 18 is not defined',
 'Variable temp at line 28 is not defined',
 'Variable b at line 36 is not defined',
 'Variable a at line 41 is not defined']
    assert errors == expected_errors

def test_entries_and_func_local_scopes():
    script = '''
    contract test_local(n:int){
        let a: int;

        func test_func(x: int): int{
            let b: int = 0;
            let v: int = 6;
        }

        entry test_entry(x: int){
            let b: int = 0;
            let c: int = a;
            let d: int = v;
        }

        entry test_entry2(x: int){
            let b: int = 0;
            let z: int = c;
        }

        func test_func2(x: int): int{
            let b: int = v;
            let z: int = c;
        }
    }
    '''
    ast = run_tzscript_ast_building_pipeline(script)
    errors = SemanticCheckerVisitor().visit(ast)
    expected_errors = ['Variable v at line 13 is not defined',
 'Variable c at line 18 is not defined',
 'Variable v at line 22 is not defined',
 'Variable c at line 23 is not defined']
    assert errors == expected_errors

def test_scope_on_parameters():
    script = '''
    contract test_params(n:int, n: int){
        let a: int;

        func test_func(x: int, x: int): int{
            let b: int = 0;
        }

        entry test_entry(x: int, x: string){
            let b: int = 0;
        }
    }
    '''
    ast = run_tzscript_ast_building_pipeline(script)
    errors = SemanticCheckerVisitor().visit(ast)
    expected_errors = ['Attribute x for test_func is already defined, error at line 5',
 'Attribute x for test_entry is already defined, error at line 9']
    assert errors == expected_errors

def test_calls_to_functions():
    script = '''
    contract test_calls(n:int){
        let a: int;

        entry test_entry(x: int){
            let b: int = 0;
            let c: int = sum(a, b);
            let z: int = sum(a, b, c);
        }
        entry test_entry2(x: int){
            let b: int = 0;
            let c: int = test_entry(x);
        }

        func sum(x: int, y: int): int{
            let l: int = 0;
            let m: int = test_func(x, y, l);
            return x + y;
        }

        func test_func(x: int, y: int, z: int): int{
            let b: int = x + y + z;
            return b;
        }
    }
    '''
    ast = run_tzscript_ast_building_pipeline(script)
    errors = SemanticCheckerVisitor().visit(ast)
    expected_errors = ['Invalid number of arguments for function sum at line 8',
 'Function test_entry is not defined at line 12']
    assert errors == expected_errors

