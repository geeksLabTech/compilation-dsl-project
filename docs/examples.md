
## Contrato para guardar un valor positivo

```python
contract store_value(admin: adress){

    var storage: nat = 0;

    entry replace(new_value: nat){
        storage = new_value;
    } 

}
```

## Contrato para sumar 2 numeros
```python
contract sum_2nums(n:int){
    let x: int = 0;

    entry sum(n:int){
        
        let a: int = 2;
        let b: int = 3;
        x = a + b;
    }
        
}
```

## Contrato que calcula n-esimo termino de fibonacci (no disponible su generación)
```python
contract get_fib_n(){
    let last_fib_calculated = 0;

    entry get_fib(n: nat){
        let result = fib(n);
        last_fib_calculated = result;
    }

    func fib(n: nat) : nat{
        if (n <= 1) {
            return n;
        }
        else {
            let a: int = n - 1;
            let b: int = n - 2;
            return fib(a) + fib(b);
        }
    }
}
```
