"""
parser.py
Desarrolla el parser completo de la gramática
"""
import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

"""
Realiza el parsing de la tabla de análisis sintáctico SLR
"""
def simulate_slr_parsing(tokens, action_table, goto_table):
    tokens.append('$')
    stack = [0]
    pointer = 0

    print("\n----------------------------\nAnálisis sintáctico SLR\n----------------------------")

    while True:
        current_state = stack[-1]
        current_token = tokens[pointer] if pointer <= len(tokens) - 1 else None
        action = action_table.get((current_state, current_token), None)

        # Prints para conocer el estado actual del análisis
        print(f"\nProcesando token: '{current_token}' en el estado {current_state}")
        print(f"Pila actual: {stack}")

        action_type, *args = action

        # Acción para aceptar la cadena
        if action_type == 'accept':
            print("Acción: Accept")
            return True
        
        # Acción para desplazar 
        elif action_type == 'shift':
            new_state = args[0]
            stack.extend([current_token, new_state])
            pointer += 1
            print(f"Acción: Shift, nuevo estado: {new_state}")
        
        # Acción para reducir
        elif action_type == 'reduce':
            production_head, production_body = args
            stack = stack[:-2 * len(production_body)]
            goto_state = goto_table.get((stack[-1], production_head))
            stack.extend([production_head, goto_state])
            print(f"Acción: Reduce, mediante {production_head} -> {' '.join(production_body)}")
        
        # Acción para error
        elif action_type == 'error':
            print(f"Error: {args[0]}")
            return False

# programmed by @melissaperez_