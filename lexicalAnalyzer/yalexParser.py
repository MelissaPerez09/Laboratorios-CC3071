"""
yalexParser.py
Parses the YALex file
"""

class YALexParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.token_rules = []
        self.definitions = {}

    def parse(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            in_rule = False
            for line in lines:
                line = line.split('(*')[0].strip()
                if line.startswith('let'):
                    parts = line.split('=')
                    name = parts[0].strip().split()[1]
                    value = parts[1].strip()
                    self.definitions[name] = value
                elif line.startswith('rule tokens'):
                    in_rule = True
                elif in_rule and '{' in line and line != '}':
                    parts = line.strip().split('{')
                    token_pattern = parts[0].strip()
                    if '|' in token_pattern:
                        token_pattern = token_pattern.split('|')[1].strip()
                    token_action = parts[1].split('}')[0].strip()
                    self.token_rules.append((token_action, token_pattern))
                elif line == '':
                    in_rule = False

    def replace_definitions(self, pattern):
        prev_pattern = None
        while prev_pattern != pattern:
            prev_pattern = pattern
            for def_name, def_value in self.definitions.items():
                pattern = pattern.replace(def_name, def_value)
        return pattern

    def generate_all_regex(self):
        regexes = {}
        for token_action, token_pattern in self.token_rules:
            regex = self.replace_definitions(token_pattern)
            regex = self.escape_special_chars(regex)
            regexes[token_action] = regex
        return regexes

    def escape_special_chars(self, regex):
        special_chars_outside_classes = {'+', '*', '|', '?', '{', '}', '.', '^', '$', '-', '/', '\\'}
        operator_chars = {'(', ')'}

        escaped_regex = ""
        inside_char_class = False
        inside_square_brackets = False
        inside_single_quotes = False
        i = 0

        while i < len(regex):
            char = regex[i]

            if char in ['[', '(', '*', '+', ')', '-', '/']:
                inside_char_class = True
                inside_square_brackets = True
            elif char in [']', ')']:
                inside_char_class = False
                inside_square_brackets = False
            elif char == "'":
                inside_single_quotes = not inside_single_quotes

            if char in special_chars_outside_classes and (i == 0 or regex[i - 1] != '\\') and not inside_char_class:
                if i == 0 or i == len(regex) - 1 or regex[i - 1].isalnum() or regex[i + 1].isalnum():
                    escaped_regex += '\\' + char
                else:
                    escaped_regex += char
            elif char in operator_chars and (i == 0 or (regex[i - 1] not in {'\\', '&', '(', '!', ':', ',', ')', '-'})) and not inside_char_class and not inside_square_brackets:
                escaped_regex += '\\' + char
            elif inside_single_quotes and char in {'+', '*', '(', ')', '-', '/', '|', '?', '{', '}', '.', '^', '$', '-', '/', ';', ':', '>', '<', '=', '!', '&', ',', '=:'}:
                escaped_regex += '\\' + char
            else:
                escaped_regex += char.replace("'", "").replace(" ", "\\_")

            i += 1

        return escaped_regex
    
    # For generating full regex of tokens
    def combine_regexes(self, regexes):
        combined_regex_parts = []
        for regex in regexes.values():
            if regex in ['+', '*', '(', ')']:
                regex = "\\" + regex
            combined_regex_parts.append(regex)
        complete_regex = '|'.join(combined_regex_parts)
        return complete_regex
    
#"""
# Debbuging class
parser = YALexParser('./yalex/slr-1.yal')
parser.parse()
regexes = parser.generate_all_regex()
full_regex = parser.combine_regexes(regexes)
print(f"{regexes} \n\n{full_regex}")
#"""
