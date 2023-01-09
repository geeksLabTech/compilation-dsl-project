# compilation-dsl-project

TZscript es un DSL para la creación de contratos inteligentes, tiene como objetivo compilar a código Michelson y generando un archivo .tz que es el código nativo que entiende la máquina virtual de Tezos.

Para saber como luce un contrato inteligente en TZscript,asi como las palabras claves de este lenguaje puede consultar la documentación en la carpeta doc del proyecto.

## CLI:
Se brinda una interfaz de consola para construir los ficheros `.tz` de michelson o para obtener una representacion de AST.

- Representación en string del AST
realiza todo el proceso de verificación pero genera como resultado la representación del cóigo en el AST, genera un fichero 'file.tzs.rep'
```bash
python cli.py represent 'file.tzs'
```

- Generación de código Michelson
Genera código michelson a partir del código TzScript, si no se especifica un fichero de salida se generará un fichero 'file.tz' 

```bash
python cli.py build 'file.tzs' 'out_file.tz'
```

- Ayuda
El cli cuenta con un menú de ayuda:

```bash
python cli.py --help
```

