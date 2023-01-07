## Introduccion
'Insertar nombre' es un dsl para la creacion de contratos inteligentes en la blockchain de tezos inspirado fundamentalmente en ['archetype-lang']((https://archetype-lang.org/))

## Documentacion
El núcleo de esta documentación es la Referencia del lenguaje organizada en cuatro partes (Declaraciones, Tipos, Instrucciones y Expresiones), sobre las que se encuentran artículos temáticos que explican los conceptos básicos del lenguaje y los detalles de su implementación.

## Hello World
```
contract store_value(value: int){

    let storage: int = 0;

    entry replace(new_value: int){
       
        storage = new_value;
    } 
}

```

## CLI
El CLI de TzScript permite compilar un script del dsl a un script Michelson. Para compilar un script del dsl, ejecute el siguiente comando:
```cli compile <path>```


