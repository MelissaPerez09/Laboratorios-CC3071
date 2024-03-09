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