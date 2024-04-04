"""
lexer.py
Lexical analyzer and source code generator
"""

import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from lexicalAnalyzer.yalexParser import YALexParser

def generate_source_code(yalex_path, output_path):
    parser = YALexParser(yalex_path)
    parser.parse()
    tokens = parser.generate_all_regex()

    with open(output_path, 'w') as f:
        f.write("#LexicalAnalyzer.py\n")
        f.write("from graphviz import Digraph\n")
        f.write("import os\n")
        
        f.write(f"\ntokens = {tokens}\n\n")
        
        f.write("#Parser regex of tokens\n")
        f.write("def parse_special_characters(regex):\n")
        f.write("   i = 0\n")
        f.write("   result = ''\n")
        f.write("   while i < len(regex):\n")
        f.write("       if i + 1 < len(regex) and regex[i] == '\\\\' and regex[i+1] in 'wnts':\n")
        f.write("           result += regex[i:i+2]\n")
        f.write("           i += 2\n")
        f.write("       else:\n")
        f.write("           result += regex[i]\n")
        f.write("           i += 1\n")
        f.write("   return result\n")
        f.write("def parse_optional(regex):\n")
        f.write("   i = 0\n")
        f.write("   result = ''\n")
        f.write("   while i < len(regex):\n")
        f.write("       if i + 1 < len(regex) and regex[i + 1] == '?':\n")
        f.write("           if regex[i] == ')':\n")
        f.write("               open_bracket_index = result.rfind('(')\n")
        f.write("               if open_bracket_index != -1:\n")
        f.write("                   result = result[:open_bracket_index] + '((' + result[open_bracket_index+1:] + ')|ε)'\n")
        f.write("           elif regex[i] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':\n")
        f.write("               if result:\n")
        f.write("                   result = result[:-1] + result[-1] + '(' + regex[i] + '|ε)'\n")
        f.write("               else:\n")
        f.write("                   result += '(' + regex[i] + '|ε)'\n")
        f.write("           i += 2\n")
        f.write("       else:\n")
        f.write("           result += regex[i]\n")
        f.write("           i += 1\n")
        f.write("   return result\n")
        f.write("def parse_repetitive(regex):\n")
        f.write("   i = 0\n")
        f.write("   result = ''\n")
        f.write("   while i < len(regex):\n")
        f.write("       if regex[i] == '\\\\':\n")
        f.write("           result += regex[i] + regex[i + 1]\n")
        f.write("           i += 2\n")
        f.write("       elif i + 1 < len(regex) and regex[i + 1] == '+':\n")
        f.write("           if regex[i] == ')':\n")
        f.write("               open_index = regex.rfind('(', 0, i)\n")
        f.write("               repeated = parse_repetitive(regex[open_index + 1:i])\n")
        f.write("               result = result[:open_index] + '(' + repeated + ')' + '(' + repeated + ')*'\n")
        f.write("               i += 2\n")
        f.write("           else:\n")
        f.write("               result += '(' + regex[i] + regex[i] + '*)'\n")
        f.write("               i += 2\n")
        f.write("       elif i + 1 < len(regex) and regex[i + 1] == '+':\n")
        f.write("           result += regex[i] + regex[i]\n")
        f.write("           i += 2\n")
        f.write("       else:\n")
        f.write("           result += regex[i]\n")
        f.write("           i += 1\n")
        f.write("   return result\n")
        f.write("def parse_range(char_range):\n")
        f.write("   result = []\n")
        f.write("   i = 0\n")
        f.write("   while i < len(char_range):\n")
        f.write("       if char_range[i:i+2] in ['\\\\w', '\\\\t', '\\\\n', '\\\\s']:\n")
        f.write("           result.append(char_range[i:i+2])\n")
        f.write("           i += 2\n")
        f.write("       elif i+2 < len(char_range) and char_range[i+1] == '-':\n")
        f.write("           start, end = char_range[i], char_range[i+2]\n")
        f.write("           result.extend([chr(c) for c in range(ord(start), ord(end)+1)])\n")
        f.write("           i += 3\n")
        f.write("       else:\n")
        f.write("           result.append(char_range[i])\n")
        f.write("           i += 1\n")
        f.write("   return result\n")
        f.write("def parse_set(regex):\n")
        f.write("   i = 0\n")
        f.write("   result=''\n")
        f.write("   while i < len(regex):\n")
        f.write("       if regex[i] == '[':\n")
        f.write("           j = i\n")
        f.write("           while regex[j] != ']':\n")
        f.write("               j += 1\n")
        f.write("           set_chars = regex[i+1:j]\n")
        f.write("           if set_chars[0] == '^':\n")
        f.write("               negated = True\n")
        f.write("               set_chars = set_chars[1:]\n")
        f.write("           else:\n")
        f.write("               negated = False\n")
        f.write("           parsed_chars = parse_range(set_chars)\n")
        f.write("           if negated:\n")
        f.write("               all_chars = set(chr(c) for c in range(32, 127))\n")
        f.write("               parsed_chars = all_chars - set(parsed_chars)\n")
        f.write("           result += '(' + '|'.join(parsed_chars) + ')'\n")
        f.write("           i = j + 1\n")
        f.write("       else:\n")
        f.write("           result += regex[i]\n")
        f.write("           i += 1\n")
        f.write("   return result\n")
        f.write("def parse_regex(regex):\n")
        f.write("   regex = parse_special_characters(regex)\n")
        f.write("   return parse_optional(parse_repetitive(parse_set(regex)))\n\n")
        
        f.write("#Shunting Yard\n")
        f.write("class ShuntingYard:\n")
        f.write("   def __init__(self, input_string):\n")
        f.write("       self.tokens = self.tokenize(input_string)\n")
        f.write("       self.epsilon = 'ε'\n")
        f.write("   def tokenize(self, input_string):\n")
        f.write("       cleaned = input_string.replace(' ', '')\n")
        f.write("       tokens = []\n")
        f.write("       i = 0\n")
        f.write("       while i < len(cleaned):\n")
        f.write("           if cleaned[i] == '\\\\':\n")
        f.write("               if i + 1 < len(cleaned):\n")
        f.write("                   tokens.append(cleaned[i] + cleaned[i + 1])\n")
        f.write("                   i += 2\n")
        f.write("               else:\n")
        f.write("                   raise ValueError('Invalid escaped character at the end of input string')\n")
        f.write("           elif cleaned[i] in {' ', '\\t', '\\n'}:\n")
        f.write("               tokens.append(f'\\\\{cleaned[i]}')\n")
        f.write("               i += 1\n")
        f.write("           else:\n")
        f.write("               tokens.append(cleaned[i])\n")
        f.write("               i += 1\n")
        f.write("       i = 0\n")
        f.write("       while i < len(tokens) - 1:\n")
        f.write("           if (tokens[i].isalnum() or tokens[i] == ')' or tokens[i] == '*') and (tokens[i + 1].isalnum() or tokens[i + 1] == '('):\n")
        f.write("               tokens.insert(i + 1, '.')\n")
        f.write("           i += 1\n")
        f.write("       return tokens\n")
        f.write("   def getPrecedence(self, operator):\n")
        f.write("       precedence = {'|': 1, '*': 3, '.': 2}\n")
        f.write("       return precedence.get(operator, 0)\n")
        f.write("   def handleSpecialChars(self, token):\n")
        f.write("       if token in ['_', '\\\\', '\\t', '\\n', '\s']:\n")
        f.write("           return True\n")
        f.write("       return False\n")
        f.write("   def shuntingYard(self):\n")
        f.write("       expression = list(self.tokens)\n")
        f.write("       i = 0\n")
        f.write("       while i < len(expression) - 1:\n")
        f.write("           if (expression[i].isalnum() or self.handleSpecialChars(expression[i]) or expression[i] == ')') and (expression[i+1].isalnum() or self.handleSpecialChars(expression[i+1]) or expression[i+1] == '('):\n")
        f.write("               expression.insert(i+1, '.')\n")
        f.write("           i += 1\n")
        f.write("       expression = ''.join(expression)\n")
        f.write("       output = []\n")
        f.write("       stack = []\n")
        f.write("       for token in expression:\n")
        f.write("           if token.isalnum() or self.handleSpecialChars(token):\n")
        f.write("               output.append(token if token != self.epsilon else 'ε')\n")
        f.write("           elif token == '(':\n")
        f.write("               stack.append(token)\n")
        f.write("           elif token == ')':\n")
        f.write("               while stack and stack[-1] != '(':\n")
        f.write("                   output.append(stack.pop())\n")
        f.write("               if stack:\n")
        f.write("                   stack.pop()\n")
        f.write("           else:\n")
        f.write("               while stack and stack[-1] != '(' and self.getPrecedence(stack[-1]) >= self.getPrecedence(token):\n")
        f.write("                   output.append(stack.pop())\n")
        f.write("               stack.append(token)\n")
        f.write("       while stack:\n")
        f.write("           output.append(stack.pop())\n")
        f.write("       return ''.join(output)\n\n")
        
        f.write("#Direct method\n")
        f.write("class DirectAFD:\n")
        f.write("   def __init__(self, value, position=None):\n")
        f.write("       self.value = value\n")
        f.write("       self.position = position\n")
        f.write("       self.left = None\n")
        f.write("       self.right = None\n")
        f.write("def increaseR(regex):\n")
        f.write("   return regex + '#.'\n")
        f.write("def construct_syntax_tree(postfix):\n")
        f.write("   stack = []\n")
        f.write("   tokens = []\n")
        f.write("   i = 0\n")
        f.write("   while i < len(postfix):\n")
        f.write("       if postfix[i] == '\\\\':\n")
        f.write("           tokens.append(postfix[i:i+2])\n")
        f.write("           i += 2\n")
        f.write("       else:\n")
        f.write("           tokens.append(postfix[i])\n")
        f.write("           i += 1\n")
        f.write("   for token in tokens:\n")
        f.write("       if token not in {'|', '*', '.'}:\n")
        f.write("           stack.append(DirectAFD(token))\n")
        f.write("   position = 0\n")
        f.write("   for token in postfix:\n")
        f.write("       if token.isalnum():\n")
        f.write("           node = DirectAFD(token, position)\n")
        f.write("           stack.append(node)\n")
        f.write("           position += 1\n")
        f.write("       elif token in ['.', '|', '#']:\n")
        f.write("           if token == '#':\n")
        f.write("               node = DirectAFD(token, position)\n")
        f.write("               stack.append(node)\n")
        f.write("               position += 1\n")
        f.write("           else:\n")
        f.write("               right = stack.pop()\n")
        f.write("               left = stack.pop()\n")
        f.write("               node = DirectAFD(token)\n")
        f.write("               node.left = left\n")
        f.write("               node.right = right\n")
        f.write("               stack.append(node)\n")
        f.write("       elif token == '*':\n")
        f.write("           operand = stack.pop()\n")
        f.write("           node = DirectAFD(token)\n")
        f.write("           node.left = operand\n")
        f.write("           stack.append(node)\n")
        f.write("   return stack.pop()\n")
        f.write("def label_leaves(node, label=0):\n")
        f.write("   if node:\n")
        f.write("       if node.left is None and node.right is None:\n")
        f.write("           node.position = label\n")
        f.write("           return label + 1\n")
        f.write("       label = label_leaves(node.left, label)\n")
        f.write("       label = label_leaves(node.right, label)\n")
        f.write("   return label\n")
        f.write("def calculate_nullable(node):\n")
        f.write("   if node is None:\n")
        f.write("       return False\n")
        f.write("   if node.value == '#':\n")
        f.write("       return True\n")
        f.write("   if node.value == '|':\n")
        f.write("       return calculate_nullable(node.left) or calculate_nullable(node.right)\n")
        f.write("   if node.value == '.':\n")
        f.write("       return calculate_nullable(node.left) and calculate_nullable(node.right)\n")
        f.write("   if node.value == '*':\n")
        f.write("       return True\n")
        f.write("   return False\n")
        f.write("def calculate_first_position(node):\n")
        f.write("   if node is None:\n")
        f.write("       return set()\n")
        f.write("   if node.value.isalnum() or node.value == '#':\n")
        f.write("       return {node.position}\n")
        f.write("   if node.value == '|':\n")
        f.write("       return calculate_first_position(node.left) | calculate_first_position(node.right)\n")
        f.write("   if node.value == '.':\n")
        f.write("       if calculate_nullable(node.left):\n")
        f.write("           return calculate_first_position(node.left) | calculate_first_position(node.right)\n")
        f.write("       else:\n")
        f.write("           return calculate_first_position(node.left)\n")
        f.write("   if node.value == '*':\n")
        f.write("       return calculate_first_position(node.left)\n")
        f.write("   return set()\n")
        f.write("def calculate_last_position(node):\n")
        f.write("   if node is None:\n")
        f.write("       return set()\n")
        f.write("   if node.value.isalnum() or node.value == '#':\n")
        f.write("       return {node.position}\n")
        f.write("   if node.value == '|':\n")
        f.write("       return calculate_last_position(node.left) | calculate_last_position(node.right)\n")
        f.write("   if node.value == '.':\n")
        f.write("       if calculate_nullable(node.right):\n")
        f.write("           return calculate_last_position(node.left) | calculate_last_position(node.right)\n")
        f.write("       else:\n")
        f.write("           return calculate_last_position(node.right)\n")
        f.write("   if node.value == '*':\n")
        f.write("       return calculate_last_position(node.left)\n")
        f.write("   return set()\n")
        f.write("def calculate_follow_pos(node, follow_pos=None):\n")
        f.write("   if follow_pos is None:\n")
        f.write("       follow_pos = {i: set() for i in range(label_leaves(node))}  # Initialize follow_pos with positions\n")
        f.write("   if node.value == '.':\n")
        f.write("       for pos in calculate_last_position(node.left):\n")
        f.write("           follow_pos[pos].update(calculate_first_position(node.right))\n")
        f.write("   elif node.value == '*':\n")
        f.write("       for pos in calculate_last_position(node):\n")
        f.write("           follow_pos[pos].update(calculate_first_position(node))\n")
        f.write("   if node.left:\n")
        f.write("       calculate_follow_pos(node.left, follow_pos)\n")
        f.write("   if node.right:\n")
        f.write("       calculate_follow_pos(node.right, follow_pos)\n")
        f.write("   return follow_pos\n")
        f.write("def find_node_by_position(node, position):\n")
        f.write("   if node is None:\n")
        f.write("       return None\n")
        f.write("   if node.position == position:\n")
        f.write("       return node\n")
        f.write("   left_result = find_node_by_position(node.left, position)\n")
        f.write("   if left_result is not None:\n")
        f.write("       return left_result\n")
        f.write("   right_result = find_node_by_position(node.right, position)\n")
        f.write("   if right_result is not None:\n")
        f.write("       return right_result\n")
        f.write("   return None\n")
        f.write("def construct_dfa_states_and_transitions(syntax_tree, follow_pos):\n")
        f.write("   alphabet = set()\n")
        f.write("   def extract_alphabet(node):\n")
        f.write("       if node:\n")
        f.write("           if node.value.isalnum():\n")
        f.write("               alphabet.add(node.value)\n")
        f.write("           extract_alphabet(node.left)\n")
        f.write("           extract_alphabet(node.right)\n")
        f.write("   extract_alphabet(syntax_tree)\n")
        f.write("   start_state = frozenset(calculate_first_position(syntax_tree))\n")
        f.write("   states = {start_state}\n")
        f.write("   dfa_transitions = {}\n")
        f.write("   queue = [start_state]\n")
        f.write("   while queue:\n")
        f.write("       current_state = queue.pop(0)\n")
        f.write("       for char in alphabet:\n")
        f.write("           next_state = set()\n")
        f.write("           for pos in current_state:\n")
        f.write("               node = find_node_by_position(syntax_tree, pos)\n")
        f.write("               if node and node.value == char:\n")
        f.write("                   next_state.update(follow_pos.get(pos, set()))\n")
        f.write("           next_state_frozen = frozenset(next_state)\n")
        f.write("           if next_state and next_state_frozen not in states:\n")
        f.write("               states.add(next_state_frozen)\n")
        f.write("               queue.append(next_state_frozen)\n")
        f.write("           if next_state:\n")
        f.write("               dfa_transitions[(current_state, char)] = next_state_frozen\n")
        f.write("   return states, dfa_transitions\n")
        f.write("def find_accept_states(states, syntax_tree):\n")
        f.write("   end_position = max(label_leaves(syntax_tree) - 1, 0)\n")
        f.write("   accept_states = {state for state in states if end_position in state}\n")
        f.write("   return accept_states\n")
        f.write("def draw_dfa(dfa_transitions, start_state, accept_states):\n")
        f.write("   graph = Digraph(format='png', graph_attr={'rankdir': 'LR'})\n")
        f.write("   states = sorted(set(key[0] for key in dfa_transitions.keys()).union(set(dfa_transitions.values())))\n")
        f.write("   state_to_number = {state: chr(ord('1') + i) for i, state in enumerate(states)}\n")
        f.write("   graph.attr('node', shape='none', width='0', height='0')\n")
        f.write("   graph.node('start', label='', shape='none')\n")
        f.write("   start_state_letter = state_to_number.get(start_state, 'X')\n")
        f.write("   graph.edge('start', start_state_letter, arrowhead='vee')\n")
        f.write("   for state, letter in state_to_number.items():\n")
        f.write("       shape = 'doublecircle' if state in accept_states else 'circle'\n")
        f.write("       graph.node(letter, label=letter, shape=shape)\n")
        f.write("   for (from_state, input_char), to_state in dfa_transitions.items():\n")
        f.write("       label = input_char\n")
        f.write("       from_state_str = state_to_number[from_state]\n")
        f.write("       to_state_str = state_to_number[to_state]\n")
        f.write("       graph.edge(from_state_str, to_state_str, label=label)\n")
        f.write("   graph.render('dfa_graph')\n")
        f.write("def applyDirect(regex):\n")
        f.write("   regex = parse_regex(regex)\n")
        f.write("   postfix = ShuntingYard(regex).shuntingYard()\n")
        f.write("   aumentada = increaseR(postfix)\n")
        f.write("   syntax_tree = construct_syntax_tree(aumentada)\n")
        f.write("   label_leaves(syntax_tree)\n")
        f.write("   follow_pos = calculate_follow_pos(syntax_tree)\n")
        f.write("   states, dfa_transitions = construct_dfa_states_and_transitions(syntax_tree, follow_pos)\n")
        f.write("   start_state = frozenset(calculate_first_position(syntax_tree))\n")
        f.write("   accept_states = find_accept_states(states, syntax_tree)\n")
        f.write("   draw_dfa(dfa_transitions, start_state, accept_states)\n")
        f.write("   return dfa_transitions, start_state, accept_states\n\n")
        
        f.write("#NFA union of all DFAs\n")
        f.write("class DFAUnion:\n")
        f.write("   def __init__(self):\n")
        f.write("       self.dfas = []\n")
        f.write("   def add_dfa(self, dfa_transitions, start_state, accept_states, token_action):\n")
        f.write("       self.dfas.append((dfa_transitions, start_state, accept_states, token_action))\n")
        f.write("   def union(self):\n")
        f.write("       afnd_transitions = {}\n")
        f.write("       afnd_start_state = 'start'\n")
        f.write("       afnd_accept_states = set()\n")
        f.write("       token_actions = {}\n")
        f.write("       afnd_transitions[afnd_start_state] = {}\n")
        f.write("       for dfa_transitions, start_state, accept_states, token_action in self.dfas:\n")
        f.write("           if None not in afnd_transitions[afnd_start_state]:\n")
        f.write("               afnd_transitions[afnd_start_state][None] = set()\n")
        f.write("           afnd_transitions[afnd_start_state][None].add(start_state)\n")
        f.write("           for state, transitions in dfa_transitions.items():\n")
        f.write("               if state not in afnd_transitions:\n")
        f.write("                   afnd_transitions[state] = {}\n")
        f.write("               for symbol, next_states in transitions.items():\n")
        f.write("                   if symbol not in afnd_transitions[state]:\n")
        f.write("                       afnd_transitions[state][symbol] = set()\n")
        f.write("                   afnd_transitions[state][symbol].update(next_states)\n")
        f.write("           afnd_accept_states.update(accept_states)\n")
        f.write("           for accept_state in accept_states:\n")
        f.write("               token_actions[accept_state] = token_action\n")
        f.write("       return afnd_transitions, afnd_start_state, afnd_accept_states, token_actions\n")
        f.write("def draw_afnd(transitions, start_state, accept_states, token_actions):\n")
        f.write("   graph = Digraph(format='png')\n")
        f.write("   for state in transitions.keys():\n")
        f.write("       if state in accept_states:\n")
        f.write("           token_action = token_actions.get(state, '')\n")
        f.write("           graph.node(str(state), f'{token_action}', shape='doublecircle')\n")
        f.write("       else:\n")
        f.write("           graph.node(str(state), str(state))\n")
        f.write("       for symbol, next_states in transitions[state].items():\n")
        f.write("           for next_state in next_states:\n")
        f.write("               graph.edge(str(state), str(next_state), label=str(symbol) if symbol else 'ε')\n")
        f.write("   MAX_LABEL_LENGTH = 100\n")
        f.write("   def truncate_label(label):\n")
        f.write("       return (label[:MAX_LABEL_LENGTH] + '..') if len(label) > MAX_LABEL_LENGTH else label\n")
        f.write("   for accept_state in accept_states:\n")
        f.write("       token_action = token_actions.get(accept_state, '')\n")
        f.write("       token_action = truncate_label(token_action)\n")
        f.write("       graph.node(str(accept_state), f'{token_action}', shape='doublecircle')\n")
        f.write("       graph.render('afnd', view=False)\n")
        
        f.write("#Analyzing with automatas\n")
        f.write("dfa_union = DFAUnion()\n")
        f.write("def convert_transitions(dfa_transitions):\n")
        f.write("    converted_transitions = {}\n")
        f.write("    for (state_frozenset, symbol), next_state_frozenset in dfa_transitions.items():\n")
        f.write("        state_str = str(state_frozenset)\n")
        f.write("        next_state_str = str(next_state_frozenset)\n")
        f.write("        if state_str not in converted_transitions:\n")
        f.write("            converted_transitions[state_str] = {}\n")
        f.write("        if symbol not in converted_transitions[state_str]:\n")
        f.write("            converted_transitions[state_str][symbol] = set()\n")
        f.write("        converted_transitions[state_str][symbol].add(next_state_str)\n")
        f.write("    return converted_transitions\n")
        f.write("for token, regex in tokens.items():\n")
        f.write("    dfa_transitions, start_state, accept_states = applyDirect(regex)\n")
        f.write("    draw_dfa(dfa_transitions, start_state, accept_states)\n")
        f.write("    os.rename('dfa_graph.png', f'dfa_graph_{token}.png')\n")
        f.write("    converted_transitions = convert_transitions(dfa_transitions)\n")
        f.write("    dfa_union.add_dfa(converted_transitions, start_state, accept_states, token)\n")
        f.write("afnd_transitions, afnd_start_state, afnd_accept_states, token_actions = dfa_union.union()\n")
        f.write("draw_afnd(afnd_transitions, afnd_start_state, afnd_accept_states, token_actions)\n\n")
        
        f.write("#Analyzing chars\n")
        f.write("def cerradura_epsilon(estados, afnd_transitions):\n")
        f.write("   cerradura = set(estados)\n")
        f.write("   pila = list(estados)\n")
        f.write("   while pila:\n")
        f.write("       estado = pila.pop()\n")
        f.write("       if estado in afnd_transitions and None in afnd_transitions[estado]:\n")
        f.write("           for prox_estado in afnd_transitions[estado][None]:\n")
        f.write("               if prox_estado not in cerradura:\n")
        f.write("                   cerradura.add(prox_estado)\n")
        f.write("                   pila.append(prox_estado)\n")
        f.write("   return cerradura\n")
        f.write("def analizar_cadena(afnd_transitions, afnd_start_state, afnd_accept_states, token_actions, cadena_entrada):\n")
        f.write("   estados_actuales = cerradura_epsilon({afnd_start_state}, afnd_transitions)\n")
        f.write("   tokens = []\n")
        f.write("   for caracter in cadena_entrada:\n")
        f.write("       print(f'Procesando caracter: {caracter}')\n")
        f.write("       proximos_estados = set()\n")
        f.write("       for estado in estados_actuales:\n")
        f.write("           estado_str = str(estado)\n")
        f.write("           if estado_str in afnd_transitions and caracter in afnd_transitions[estado_str]:\n")
        f.write("               proximos_estados.update(afnd_transitions[estado_str][caracter])\n")
        f.write("       estados_actuales = cerradura_epsilon(proximos_estados, afnd_transitions)\n")
        f.write("   for estado in estados_actuales:\n")
        f.write("       estado_set = eval(estado) if isinstance(estado, str) else estado\n")
        f.write("       print(f'Buscando estado {estado_set} en token_actions: {token_actions}')\n")
        f.write("       if estado_set in token_actions:\n")
        f.write("           tokens.append(token_actions[estado_set])\n")
        f.write("   return tokens\n")
        f.write("cadena_entrada = 'A'\n")
        f.write("tokens = analizar_cadena(afnd_transitions, afnd_start_state, afnd_accept_states, token_actions, cadena_entrada)\n")
        f.write("if tokens:\n")
        f.write("   print(f'La acción del token es: {tokens}')\n")
        f.write("else:\n")
        f.write("   print('No se encontró un token válido para la cadena de entrada.')\n")

        
    print(">>> LexicalAnalyzer.py created successfully!")