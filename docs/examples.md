
## Contrato para guardar un valor positivo
```
contract store_value(admin: adress){

    var storage: nat = 0;

    entry replace(new_value: nat){
        called by admin;
        storage = new_value;
    } 

    entry double_previous_value(){
        called by admin;
        storage = storage * 2;
    }
}
```

## Contrato que calcula n-esimo termino de fibonacci
```
contract get_fib_n(){
    let last_fib_calculated = 0;

    entry get_fib_n(n: nat){
        let result = fib(n);
        last_fib_calculated = result;
    }

    func fib(n: nat) -> nat{
        if (n <= 1) {
            return n;
        }
        else {
            return fib(n-1) + fib(n-2);
        }
    }
}
```

## Contrato para emitir certificacion de estudiantes

```
contract student_certification(certifier: adress){

    type student = {
        name: string,
        certificate: bool
    }

    var storage: map[string, student] = {}   
    
    entry certifyStudent(name: string) {
        calledBy certifier;
        const student = findStudent(name);
        if student == None {
            storage.students[name] = {
                name: name,
                certificate: true
            }
        }
        else {
            storage.students[name].certificate = true;
        }
    }

    func findStudent (name: string) -> optional[student] {
        for student in storage.students {
            if student.name == name {
                return student;
            }
        }
        return None;
    }
    
}
```