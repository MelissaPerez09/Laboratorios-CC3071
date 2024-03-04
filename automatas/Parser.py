"""
Parser.py
Parses the regular expression and checks for errors
"""

"""
Parse the optional operator "?"
:param regex: Regular expression
Reemplaza el operador con una cadena vacía ε
"""
def parse_optional(regex):
    i = 0
    result = ""
    while i < len(regex):
        if i + 1 < len(regex) and regex[i + 1] == "?":
            if regex[i] == ")":
                open_bracket_index = result.rfind("(")
                if open_bracket_index != -1:
                    result = result[:open_bracket_index] + "((" + result[open_bracket_index+1:] + ")|ε)"
            elif regex[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
                if result:
                    result = result[:-1] + result[-1] + "(" + regex[i] + "|ε)"
                else:
                    result += "(" + regex[i] + "|ε)"
            i += 2
        else:
            result += regex[i]
            i += 1
    return result

"""
Parse the repetitive "+"
:param regex: Regular expression
Reemplaza con una concatenación con una repetición
"""
def parse_repetitive(regex):
    i = 0
    result = ""
    while i < len(regex):
        if i + 1 < len(regex) and regex[i + 1] == "+":
            if regex[i] == ")":
                open_index = regex.rfind("(", 0, i)
                repeated = parse_repetitive(regex[open_index + 1:i])
                result = result[:open_index] + "(" + repeated + ")" + "(" + repeated + ")*"
                i += 2
            else:
                result += "(" + regex[i] + regex[i] + "*)"
                i += 2
        else:
            result += regex[i]
            i += 1
    return result

"""
Parse the set of characters
:param char_range: Character range
Devuelve una lista de caracteres del rango
"""
def parse_range(char_range):
    result = []
    i = 0
    while i < len(char_range):
        if i+2 < len(char_range) and char_range[i+1] == '-':
            start, end = char_range[i], char_range[i+2]
            result.extend([chr(c) for c in range(ord(start), ord(end)+1)])
            i += 3
        else:
            result.append(char_range[i])
            i += 1
    return ''.join(result)

"""
Parse the set of characters
:param regex: Regular expression
Reemplaza el conjunto de caracteres con una cadena de caracteres
"""
def parse_set(regex):
    i = 0
    result = ""
    while i < len(regex):
        if regex[i] == "[":
            set_end = regex.find("]", i)
            result += "(" + "|".join(list(parse_range(regex[i+1:set_end]))) + ")"
            i = set_end + 1
        else:
            result += regex[i]
            i += 1
    return result

# Error detection or regex
"""
Check if the regex contains valid symbols
:param regex: Regular expression
Devuelve True si todos los símbolos son válidos
"""
def check_valid_symbols(regex):
    valid_symbols = set("[]-|()ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789*+?ε")
    return all(char in valid_symbols for char in regex)

"""
Check balanced parentheses
:param regex: Regular expression
Devuelve True si los paréntesis están balanceados
"""
def check_balanced_parentheses(regex):
    stack = []
    unbalanced_parentheses = []

    for i, char in enumerate(regex):
        if char == '(':
            stack.append((char, i))
        elif char == ')':
            if not stack:
                unbalanced_parentheses.append((char, i, "missing opening"))
            else:
                stack.pop()

    for item in stack:
        unbalanced_parentheses.append(('(', item[1], "missing closure"))

    return len(stack) == 0, unbalanced_parentheses

"""
Check consecutive operators
:param regex: Regular expression
Devuelve True si no hay operadores consecutivos
"""
def check_consecutive_operators(regex):
    consecutive_operators = ['??', '++', '**']
    for op in consecutive_operators:
        if op in regex:
            return False
    return True

"""
Parse the regular expression
:param regex: Regular expression
Devuelve la expresión regular analizada
"""
def parse_regex(regex):
    valid_symbols = set("[]-|()ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789*+?ε")
    invalid_symbols = [char for char in regex if char not in valid_symbols]

    if invalid_symbols:
        raise ValueError(f">>>Invalid symbol(s) detected: {' '.join(invalid_symbols)}. \nOnly [A-Za-z0-9*+?[],()] are allowed.")

    if not check_consecutive_operators(regex):
        raise ValueError(">>>Consecutive operators are not permitted. Use one at a time.")

    is_balanced, unbalanced_parentheses = check_balanced_parentheses(regex)
    if not is_balanced:
        error_messages = []
        for char, i, error_type in unbalanced_parentheses:
            error_messages.append(f">>>Unbalanced parenthesis '{char}': {error_type}.")
        raise ValueError("\n".join(error_messages))

    # parsing
    return parse_optional(parse_repetitive(parse_set(regex)))

# programmed by @melissaperez_