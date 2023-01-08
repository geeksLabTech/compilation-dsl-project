
## Contrato para guardar un valor positivo
```
contract store_value(admin: adress){

    var storage: nat = 0;

    entry replace(new_value: nat){
        storage = new_value;
    } 

    entry double_previous_value(){
        storage = storage * 2;
    }
}
```

## Contrato que calcula n-esimo termino de fibonacci
```
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
