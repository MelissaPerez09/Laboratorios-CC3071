"""
gammar.py
Define la estructura de la gramática utilizada por el analizador sintáctico
"""

def parse_yapar_file(file_path):
    # Estructuras para almacenar la información extraída
    grammar = {}
    tokens = set()
    
    # Leer el archivo
    with open(file_path, 'r') as file:
        content = file.readlines()
    
    # Analizar cada línea
    current_section = None
    current_head = None
    for line in content:
        line = line.strip()
        if line.startswith('/*') and line.endswith('*/'):
            # Ignorar comentarios
            continue
        elif line.startswith('%token'):
            # Sección de tokens
            parts = line.split()
            tokens.update(parts[1:])  # Agregar todos los tokens encontrados
        elif line.startswith('%%'):
            # Inicio de las reglas gramaticales
            current_section = 'rules'
        elif current_section == 'rules' and line:
            if line.endswith(';'):
                line = line[:-1]  # Remover punto y coma final
            if ':' in line:
                # Nueva regla gramatical
                head, production = line.split(':')
                head = head.strip()
                current_head = head
                grammar[current_head] = []
                line = production  # Continuar procesando el resto de la línea como producción
            # Añadir producciones a la cabeza actual
            if current_head:
                productions = [prod.strip() for prod in line.split('|')]
                for prod in productions:
                    if prod:
                        production = tuple(prod.split())
                        grammar[current_head].append(production)
        elif line.startswith('IGNORE'):
            # Sección de ignorar tokens (por ejemplo, espacios en blanco)
            _, ignore_token = line.split()
            if ignore_token in tokens:
                tokens.remove(ignore_token)  # Remover el token de ignorar de los tokens activos
    
    return grammar, tokens

# Testing
grammar, tokens = parse_yapar_file('./yapar/slr-8.yalp')
print("Grammar:", grammar)
print("Tokens:", tokens)
