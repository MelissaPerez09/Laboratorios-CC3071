"""
parser.py
Desarrolla el parser completo de la gramática
"""
import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

"""
Realiza el parsing de la tabla de análisis sintáctico SLR
"""
def simulate_slr_parsing(token_generator, action_table, goto_table):
    stack = [0]
    error_detected = False

    print("\n----------------------------\nAnálisis sintáctico SLR\n----------------------------")

    # Iterar sobre los tokens generados por el analizador léxico
    for current_token, error in token_generator:
        # Si hay un error léxico, se imprime y se ignora el token
        if error:
            print(f"\n(!) ERROR LÉXICO \nEn línea {error[0]}, posición {error[1]} caracter: '{error[2]}'")
            error_detected = True
            continue
        
        # Iterar sobre los elementos de la pila
        while True:
            current_state = stack[-1]
            action = action_table.get((current_state, current_token), None)

            # Prints para conocer el estado actual del análisis
            print(f"\nProcesando token: '{current_token}' en el estado {current_state}")
            print(f"Pila actual: {stack}")

            if action is None:
                print(f"\n(!) ERROR SINTÁCTICO \nNo se encuentra acción para el estado {current_state} y el token '{current_token}'")
                error_detected = True
                break

            action_type, *args = action

            # Accion: Accept
            if action_type == 'accept':
                print("Acción: Accept")
                # Si no se ha detectado un error léxico, se acepta la entrada
                if not error_detected:
                    print("\n (✓) La entrada es aceptada.")
                # Si se detectó un error léxico, se rechaza la entrada
                else:
                    print("\n (!) La entrada no es aceptada.")
                return not error_detected
            
            # Accion: Shift
            elif action_type == 'shift':
                new_state = args[0]
                stack.extend([current_token, new_state])
                print(f"Acción: Shift, nuevo estado: {new_state}")
                break
            
            # Accion: Reduce
            elif action_type == 'reduce':
                production_head, production_body = args
                stack = stack[:-2 * len(production_body)]
                goto_state = goto_table.get((stack[-1], production_head))
                stack.extend([production_head, goto_state])
                print(f"Acción: Reduce, mediante {production_head} -> {' '.join(production_body)}")
    
    # Si no encuentra error sintáctico, se acepta la entrada
    if not error_detected:
        print("\n (✓) La entrada es aceptada.")
    # Si encuentra error sintáctico, se rechaza la entrada
    else:
        print("\n (!) La entrada no es aceptada.")
    return not error_detected

# programmed by @melissaperez_