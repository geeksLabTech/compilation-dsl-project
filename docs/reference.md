
## Identificadores
El identificador de un elemento del contrato (parámetro, variable, punto de entrada, ...) es una cadena que comienza con un carácter alfabético (en minúscula o mayúscula) seguido de una cadena de caracteres alfanuméricos (en minúscula o mayúscula) o guiones bajos. El tamaño máximo de un identificador es 254. Es decir, un identificador verifica la siguiente expresión regular:

```([A-Za-z][A-Za-z0-9_]*){1,254}```

## Keywords
Una palabra clave es un identificador reservado que no puede utilizarse como identificador

Las palabras reservadas del lenguage son:
- `contract`
- `entry`
- `func`
- `var`
- `if`
- `else`
- `const`
- `type`
- `for`
- `in`
- `string`
- `nat`
- `int`
- `map`
- `optional`
- `bool`
- `None`
- `true`
- `false`
- `return`
- `calledBy`

## Contract
Un contrato del dsl comienza con la palabra clave contract seguida de un identificador y un bloque de codigo entre llaves 
    
```
contract <identifier> () { <code> }
```

### Parametros
Un contrato puede tener parámetros. El valor de un parámetro no está en el código fuente y se proporciona en el momento del despliegue (originación). Por ejemplo, la dirección del propietario del contrato suele ser un parámetro del contrato. Por defecto, un parámetro del contrato es un elemento del storage. Se define por un identificador y un tipo. La lista de parámetros sigue al identificador del contrato entre paréntesis y separados por coma.
    
```
contract <identifier> (<parameter_identifier>: <parameter_type>, ...) 
{ <code> }
```

### Variables del storage
Una variable del storage es un elemento de cuyo valor se establece en el momento de la declaración. Se declara con la palabra clave var seguida de un identificador, un tipo y el valor inicial.

```
var <identifier>: <type> = <value>
```

El valor de una variable del storage solamente puede ser modificado por instrucciones de asignacion en los puntos de entrada del contrato

### Creacion de tipos
Un type permite agrupar un conjunto de elementos en una estructura. Se declara con la palabra clave type seguida de un identificador y un bloque de código entre llaves. El bloque de código contiene una lista de elementos separados por coma. Cada elemento tiene un identificador y un tipo. Por ejemplo, un type para representar un estudiante puede ser:

```
type student = {
    name: string,
    certificate: bool
}
```

### Puntos de entrada 
Un punto de entrada es un bloque de código que no puede ser llamado desde otros puntos de entrada o funciones. Se declara con la palabra clave entry seguida de un identificador, una lista de parámetros entre paréntesis y un bloque de código entre llaves. Los puntos de entrada pueden acceder y modificar el storage


### Funciones
Una función es un bloque de código que puede ser llamado desde otras funciones o puntos de entrada. Se declara con la palabra clave func seguida de un identificador, una lista de parámetros entre paréntesis y un bloque de código entre llaves. Las funciones solo pueden acceder a los valores que reciben y no pueden modificar el storage.


## Tipos

### address
Cuenta o dirección del contrato en la blockchain de Tezos. Una dirección está formada por un prefijo (tz1 tz2 tz3 y KT1 para los contratos) seguido de un hash codificado en Base58 y terminado por un checksum de 4 bytes.
#### Ejemplos
```
tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx
tz2BFTyPeYRzxd5aiBchbXN3WCZhx7BqbMBq
tz3hFR7NZtjT2QtzgMQnWb4xMuD6yt2YzXUt
KT1Hkg8v4iUykJwpFcLgVwKXHd3LsKdJnVwv
```

### bool
Valor booleano. Puede ser true o false

### int
Valor entero. Puede ser negativo o positivo

### nat
Valor entero positivo

### string
Cadena de caracteres. Se representa entre comillas dobles

### map
Mapa de elementos. Se representa entre llaves y separados por coma. Cada elemento tiene una clave y un valor. La clave es un valor de tipo nat, int o string. El valor puede ser de cualquier tipo. 

### None
Valor especial que representa la ausencia de valor.

### optional
Se usa para representar cuando un valor puede ser de un tipo o None.
```
optional[<type>]
```





