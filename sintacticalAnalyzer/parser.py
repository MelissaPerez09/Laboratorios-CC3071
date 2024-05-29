"""
parser.py
Desarrolla el parser completo de la gramática
"""
import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from sintacticalAnalyzer.main import *

def simulate_slr_parsing(tokens, action_table, goto_table):
    """
    Simula el análisis SLR de una cadena de tokens.
    
    :param tokens: Lista de tokens a analizar.
    :param action_table: Tabla de acciones SLR.
    :param goto_table: Tabla goto SLR.
    """
    
    # Estructuras para el proceso de parsing
    stack = [0]  # stack inicial contiene solo el estado inicial
    pointer = 0  # apunta al token actual en la entrada
    
    # Procesar la entrada
    while pointer < len(tokens):
        current_token = tokens[pointer]
        current_state = stack[-1]
        action = action_table.get((current_state, current_token))
        
        "\n----------------------------\nSLR parsing:\n----------------------------"
        if action is None:
            print(f"Error: no se encuentra acción para el estado {current_state} y el token {current_token}")
            return False
        
        if action[0] == 'shift':
            print(f"\nShift: {current_token}")
            stack.append(current_token)
            stack.append(action[1])  # agregar el estado al que se transita
            pointer += 1
        elif action[0] == 'reduce':
            # La reducción usa una producción, aquí se asume que se conocen las longitudes
            production_head, production_body = action[1], action[2]
            length_to_pop = 2 * len(production_body)  # doble porque incluye estados y símbolos
            stack = stack[:-length_to_pop]  # retirar de la pila
            current_state = stack[-1]
            stack.append(production_head)
            goto_state = goto_table.get((current_state, production_head))
            if goto_state is None:
                print(f"Error: no hay transición goto para {current_state} y {production_head}")
                return False
            stack.append(goto_state)
            print(f"Reduce usando {production_head} -> {' '.join(production_body)}")
        elif action[0] == 'accept':
            print("\nAccept: La cadena es sintácticamente correcta.")
            return True
        else:
            print("Error: acción desconocida.")
            return False

    print("\nError: No se aceptó la cadena.")
    return False

