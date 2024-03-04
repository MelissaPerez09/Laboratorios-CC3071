"""
yalexParser.py
Parses the YALex file
"""

class YALexParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.token_rules = []

    def parse(self):
        definitions = {}
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.split('(*')[0].strip()
                if line.startswith('let'):
                    parts = line.split('=')
                    name = parts[0].strip().split()[1]
                    value = parts[1].strip()
                    ascii_value = self.replace_characters_with_ascii(value)
                    definitions[name] = (value, ascii_value)
                elif not line or line.startswith('rule tokens ='):
                    continue
                elif line.endswith('}'):
                    action = line.split('{')[1].split('}')[0].strip()
                    token_name = action.split()[1]
                    self.token_rules.append((action, token_name))
        self.definitions = definitions

    def replace_characters_with_ascii(self, value):
        replaced_value = ""
        in_quotes = False
        for char in value:
            if char == "'" and not in_quotes:
                in_quotes = True
                replaced_value += char
            elif char == "'" and in_quotes:
                in_quotes = False
                replaced_value += char
            elif in_quotes:
                replaced_value += f" ({ord(char)})"
            else:
                replaced_value += char
        return replaced_value

    def get_token_rules(self):
        return self.token_rules

    def get_definitions(self):
        return self.definitions

    def generate_id_regex(self):
        token_rules = self.get_token_rules()
        definitions = self.get_definitions()

        id_definition = definitions.get('id', None)
        number_definition = definitions.get('number', None)
        
        if id_definition:
            id_regex = id_definition[0]
        else:
            id_regex = ""
        
        if number_definition:
            number_regex = number_definition[0]
        else:
            number_regex = ""

        for name, (original, _) in definitions.items():
            id_regex = id_regex.replace(name, original)
            number_regex = number_regex.replace(name, original)

        for action, token_name in token_rules:
            id_regex = id_regex.replace(token_name, action)
            number_regex = number_regex.replace(token_name, action)

        id_regex = id_regex.replace("'", "").replace('"', "")
        number_regex = number_regex.replace("'", "").replace('"', "")

        return id_regex, number_regex

parser = YALexParser('./yalex/slr-4.yal')
parser.parse()
print(parser.generate_id_regex())
print(parser.get_token_rules())
