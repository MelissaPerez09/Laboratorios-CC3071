"""
Parser.py

"""

def parse_optional(regex):
    i = 0
    result = "("
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

def parse_regex(regex):
    return parse_optional(parse_repetitive(parse_set(regex)))

