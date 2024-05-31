# Laboratorios - CC3071
Repositorio que contiene todos los laboratorios del curso de Diseño de lenguajes de programación.

## Laboratorio AB
Implementación de algoritmos básicos de autómatas finitos y expresiones regulares. Se trata de la base de un generador de analizadores léxicos. 
Se implementan los algoritmos:
- _Shunting yard:_ para pasar de una expresión en notación infija a posfija.
- _McNaughton–Yamada–Thompson:_ para convertir la expresión en notación posfija a un autómata finito no determinista (AFN).
- _Construcción de subconjuntos:_ para convertir el autómata finito no determinista (AFN) a uno determinista (AFD).
- _Minimización de un AFD:_ para minimizar los estados de un autómata finito determinista (AFD).
- _Construcción directa de un AFD:_ para convertir de una expresión posfija a un autómata finito determinista (AFD) en su forma minimizada.

El código funciona ingresando una expresión en notación infija y una cadena. Luego realiza un análisis de la expresión y la convierte a la notación deseada para poder evaluar la precedencia de operadores y convertirla a notación posfija. Si encuentra un error en la expresión ingresada, lo muestra claramente. Pasando ese análisis, realiza el proceso de generar los autómatas finitos y por cada uno evalúa si la cadena ingresada pertenece al lenguaje.

## Laboratorio C
Inicio del desarrollo de un generador de analizadores léxicos basados en YALex.

El código funciona en una interfaz gráfica que permite abrir un archivo con la extesión _.yal_, recibe una especificación de componentes léxicos para generar un autómata que reconoce los componentes léxicos especificados.

La interfaz gráfica cuenta con un botón para abrir el archivo, un editor donde se puede modificar el archivo que se abrió, un botón 'analizar' para ejecutar las funciones del código y una terminal donde imprime lo que sucede en el análisis.

## Laboratorio D
Finalización del desarrollo de un generador léxico basado en YALex y su ejecución con textos de prueba para identificar tokens con las reglas descritas.

Al igual que el laboratorio C funciona con una interfaz gráfica. En este caso, en el apartado de _'LA Generator'_ se encuentra el generador del código fuente del analizador léxico que recibe como entrada un archivo escrito en YALex para devolver un diccionario con los tokens donde la llave es la acción y el valor es la expresión regular. Este genera el código fuente que implementa todo el analizador para que pueda ejecutarse de forma independiente a otras clases o módulos. 

Para ejecutar el código fuente es necesario dirigirse al apartado _'Analyzer'_ donde recibe un archivo de texto con los caracteres a evaluar, devuelve los tokens y  ejecuta las acciones en la terminal.

## Laboratorio E
Desarrollo de un generador de analizadores sintáticos basados en YAPar.

Utiliza la extracción de tokens de un archivo YALex para validar que se encuentren definidos en la gramática y viceversa. Si alguno de los tokens que utiliza la gramática YAPar no se encuentra en YALex muestra un error e idenitifica los tokens faltantes.

Luego de la validación continúa con la generación del autómata LR(0) donde identifica los elementos que pertenecen al corazón, los que no y el estado de aceptación.

Por último, realiza el cálculo de las funciones primero y siguiente mostrando el resultado como un conjunto.

Para la ejecución del código, debe correrse el archivo _'app.py'_ y abrir los dos archivos (YALex y YAPar) para presionar el botón _generate_ y que realice el proceso antes mencionado.

## Laboratorio F
Finalización del analizador sintáctico y unión con el analizador léxico.

Su funcionamiento consta de obtener tres archivos de entrada, uno con la definición de tokens (YALex), uno con la definición de la gramática (YAPar) y uno con la cadena a evaluar.

El analizador léxico evalúa los tokens existentes en la cadena para que puedan ser enviados uno a uno al analizador sintáctico. El analizador sintáctico realiza la tabla de análisis SLR utilizando los estados de la gramática y las funciones primero y siguiente. Luego, recibe los tokens que le pasa el analizador léxico para que generen el _parsing_ de la tabla para identificar las acciones que corresponden a cada estado.

Al finalizar todo el proceso y las impresiones de las acciones, el analizador permite aceptar la entrada o no. Esto depende si encuentra errores léxicos, sintácticos o la cadena no es aceptada por la gramática.