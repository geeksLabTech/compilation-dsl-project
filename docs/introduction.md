## Introduccion
'Insertar nombre' es un dsl para la creacion de contratos inteligentes en la blockchain de tezos inspirado fundamentalmente en ['archetype-lang']((https://archetype-lang.org/))

## Documentacion
El núcleo de esta documentación es la Referencia del lenguaje organizada en cuatro partes (Declaraciones, Tipos, Instrucciones y Expresiones), sobre las que se encuentran artículos temáticos que explican los conceptos básicos del lenguaje y los detalles de su implementación.

## Hello World
```
contract hello_world () {

    var msg : string = "Hello";

    entry input(name: string) {
        if (len(msg) > 5) {
            msg = msg + " " + name;
        }
        else {
            msg = msg + "," + " " + name;
        }
    }
}

```

## CLI
El CLI de 'Insertar nombre' permite compilar un script del dsl a un script Michelson, tambien permite testear y desplegar los scripts compilados apoyandose en ['pytezos'](https://pytezos.org/). Para compilar un script del dsl, ejecute el siguiente comando:
```cli compile <path>```


Para desplegar un script de Michaelson, ejecute el siguiente comando:

```cli deploy <path>```

