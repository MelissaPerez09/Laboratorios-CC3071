"""
Parser.py

"""

def parse_optional(regex):
    i = 0
    result = ""
    while i < len(regex):
        if i + 1 < len(regex) and regex[i + 1] == "?":
            result += regex[i] + "|ε)"
            i += 2
        else:
            result += regex[i]
            i += 1
    return result

def parse_repetitive(regex):
    i = 0
    result = ""
    while i < len(regex):
        if i + 1 < len(regex) and regex[i + 1] == "+":
            if regex[i] == ")":
                open_index = regex.rfind("(", 0, i)
                repeated = regex[open_index + 1:i]
                result = result[:open_index + 1] + "(" + repeated + ")" + "(" + repeated + ")*)" + result[i + 1:]
            else:
                result += "(" + regex[i] + ")"
            i += 2
        else:
            result += regex[i]
            i += 1
    return result

def parse_range(char_range):
    if len(char_range) == 1:
        return char_range
    else:
        start, end = char_range[0], char_range[-1]
        return [chr(char) for char in range(ord(start), ord(end) + 1)]

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
def check_valid_symbols(regex):
    valid_symbols = set("[]-()ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789*+?")
    return all(char in valid_symbols for char in regex)

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

def parse_regex(regex):
    valid_symbols = set("[]-()ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789*+?")
    invalid_symbols = [char for char in regex if char not in valid_symbols]

    if invalid_symbols:
        raise ValueError(f">>>Invalid symbol(s) detected: {' '.join(invalid_symbols)}. \nOnly [A-Za-z0-9*+?[],()] are allowed.")

    is_balanced, unbalanced_parentheses = check_balanced_parentheses(regex)
    if not is_balanced:
        error_messages = []
        for char, i, error_type in unbalanced_parentheses:
            error_messages.append(f">>>Unbalanced parenthesis '{char}': {error_type}.")
        raise ValueError("\n".join(error_messages))

    # parsing
    return parse_optional(parse_repetitive(parse_set(regex)))