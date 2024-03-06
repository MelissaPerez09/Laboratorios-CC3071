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
                    value = parts[1].strip().replace("'", "")
                    self.definitions[name] = value
                elif line.startswith('rule tokens'):
                    in_rule = True
                elif in_rule and '{' in line and line != '}':
                    parts = line.strip().split('{')
                    token_pattern = parts[0].strip()
                    if '|' in token_pattern:
                        token_pattern = token_pattern.split('|')[1].strip()
                    token_name = parts[1].split('}')[0].strip().split()[1]
                    self.token_rules.append((token_name, token_pattern))
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
        for token_name, token_pattern in self.token_rules:
            regex = self.replace_definitions(token_pattern)
            regex = regex.replace("'", "").replace('\\', '|\\')
            regexes[token_name] = regex
        return regexes
    
    # For generating full regex of tokens
    def combine_regexes(self, regexes):
        combined_regex_parts = []
        for regex in regexes.values():
            if regex in ['+', '*', '(', ')']:
                regex = "\\" + regex
            combined_regex_parts.append(regex)
        complete_regex = '|'.join(combined_regex_parts)
        return complete_regex
    
"""
# Debbuging class
parser = YALexParser('./yalex/slr-1.yal')
parser.parse()
regexes = parser.generate_all_regex()
full_regex = parser.combine_regexes(regexes)
print(f"{regexes} \n{full_regex}")
"""
