"""
parser.py
Desarrolla el parser completo de la gramática
"""
import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from sintacticalAnalyzer.main import *

def simulate_slr_parsing(tokens, action_table, goto_table):
    tokens.append('$')  # Aseguramos que '$' es parte de los tokens
    stack = [0]  # El stack inicial contiene solo el estado inicial.
    pointer = 0  # Apunta al primer token en la entrada.

    print("Inicio del proceso de parsing")
    print("Tokens: ", tokens)
    print("Estado inicial de la pila: ", stack)

    while True:
        current_state = stack[-1]
        current_token = tokens[pointer] if pointer <= len(tokens) - 1 else None
        action = action_table.get((current_state, current_token), None)

        print(f"\nProcesando token: '{current_token}' en el estado: {current_state}")
        print(f"Acción encontrada: {action}")

        if action is None:
            print(f"Error: No se encuentra acción para el estado {current_state} y el token '{current_token}'")
            print(f"Estado final de la pila: {stack}")
            return False

        action_type, *args = action

        if action_type == 'accept':
            print("Acción: Accept. La cadena es sintácticamente correcta.")
            return True
        elif action_type == 'shift':
            new_state = args[0]
            stack.extend([current_token, new_state])
            pointer += 1
        elif action_type == 'reduce':
            production_head, production_body = args
            stack = stack[:-2 * len(production_body)]  # Removing symbols from stack
            goto_state = goto_table.get((stack[-1], production_head))  # Use the state after reduction
            stack.extend([production_head, goto_state])

        print(f"Estado actual de la pila: {stack}")

    print("\nError: La cadena no fue aceptada al final del análisis.")
    print(f"Estado final de la pila: {stack}")
    return False