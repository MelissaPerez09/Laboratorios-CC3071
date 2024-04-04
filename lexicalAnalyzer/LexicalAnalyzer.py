#LexicalAnalyzer.py
from graphviz import Digraph
import os

tokens = {'print regex': '[A-C]([A-C])*', 'print new line': '\\\\n'}

#Parser regex of tokens
def parse_special_characters(regex):
   i = 0
   result = ''
   while i < len(regex):
       if i + 1 < len(regex) and regex[i] == '\\' and regex[i+1] in 'wnts':
           result += regex[i:i+2]
           i += 2
       else:
           result += regex[i]
           i += 1
   return result
def parse_optional(regex):
   i = 0
   result = ''
   while i < len(regex):
       if i + 1 < len(regex) and regex[i + 1] == '?':
           if regex[i] == ')':
               open_bracket_index = result.rfind('(')
               if open_bracket_index != -1:
                   result = result[:open_bracket_index] + '((' + result[open_bracket_index+1:] + ')|ε)'
           elif regex[i] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':
               if result:
                   result = result[:-1] + result[-1] + '(' + regex[i] + '|ε)'
               else:
                   result += '(' + regex[i] + '|ε)'
           i += 2
       else:
           result += regex[i]
           i += 1
   return result
def parse_repetitive(regex):
   i = 0
   result = ''
   while i < len(regex):
       if regex[i] == '\\':
           result += regex[i] + regex[i + 1]
           i += 2
       elif i + 1 < len(regex) and regex[i + 1] == '+':
           if regex[i] == ')':
               open_index = regex.rfind('(', 0, i)
               repeated = parse_repetitive(regex[open_index + 1:i])
               result = result[:open_index] + '(' + repeated + ')' + '(' + repeated + ')*'
               i += 2
           else:
               result += '(' + regex[i] + regex[i] + '*)'
               i += 2
       elif i + 1 < len(regex) and regex[i + 1] == '+':
           result += regex[i] + regex[i]
           i += 2
       else:
           result += regex[i]
           i += 1
   return result
def parse_range(char_range):
   result = []
   i = 0
   while i < len(char_range):
       if char_range[i:i+2] in ['\\w', '\\t', '\\n', '\\s']:
           result.append(char_range[i:i+2])
           i += 2
       elif i+2 < len(char_range) and char_range[i+1] == '-':
           start, end = char_range[i], char_range[i+2]
           result.extend([chr(c) for c in range(ord(start), ord(end)+1)])
           i += 3
       else:
           result.append(char_range[i])
           i += 1
   return result
def parse_set(regex):
   i = 0
   result=''
   while i < len(regex):
       if regex[i] == '[':
           j = i
           while regex[j] != ']':
               j += 1
           set_chars = regex[i+1:j]
           if set_chars[0] == '^':
               negated = True
               set_chars = set_chars[1:]
           else:
               negated = False
           parsed_chars = parse_range(set_chars)
           if negated:
               all_chars = set(chr(c) for c in range(32, 127))
               parsed_chars = all_chars - set(parsed_chars)
           result += '(' + '|'.join(parsed_chars) + ')'
           i = j + 1
       else:
           result += regex[i]
           i += 1
   return result
def parse_regex(regex):
   regex = parse_special_characters(regex)
   return parse_optional(parse_repetitive(parse_set(regex)))

#Shunting Yard
class ShuntingYard:
   def __init__(self, input_string):
       self.tokens = self.tokenize(input_string)
       self.epsilon = 'ε'
   def tokenize(self, input_string):
       cleaned = input_string.replace(' ', '')
       tokens = []
       i = 0
       while i < len(cleaned):
           if cleaned[i] == '\\':
               if i + 1 < len(cleaned):
                   tokens.append(cleaned[i] + cleaned[i + 1])
                   i += 2
               else:
                   raise ValueError('Invalid escaped character at the end of input string')
           elif cleaned[i] in {' ', '\t', '\n'}:
               tokens.append(f'\\{cleaned[i]}')
               i += 1
           else:
               tokens.append(cleaned[i])
               i += 1
       i = 0
       while i < len(tokens) - 1:
           if (tokens[i].isalnum() or tokens[i] == ')' or tokens[i] == '*') and (tokens[i + 1].isalnum() or tokens[i + 1] == '('):
               tokens.insert(i + 1, '.')
           i += 1
       return tokens
   def getPrecedence(self, operator):
       precedence = {'|': 1, '*': 3, '.': 2}
       return precedence.get(operator, 0)
   def handleSpecialChars(self, token):
       if token in ['_', '\\', '\t', '\n', '\s']:
           return True
       return False
   def shuntingYard(self):
       expression = list(self.tokens)
       i = 0
       while i < len(expression) - 1:
           if (expression[i].isalnum() or self.handleSpecialChars(expression[i]) or expression[i] == ')') and (expression[i+1].isalnum() or self.handleSpecialChars(expression[i+1]) or expression[i+1] == '('):
               expression.insert(i+1, '.')
           i += 1
       expression = ''.join(expression)
       output = []
       stack = []
       for token in expression:
           if token.isalnum() or self.handleSpecialChars(token):
               output.append(token if token != self.epsilon else 'ε')
           elif token == '(':
               stack.append(token)
           elif token == ')':
               while stack and stack[-1] != '(':
                   output.append(stack.pop())
               if stack:
                   stack.pop()
           else:
               while stack and stack[-1] != '(' and self.getPrecedence(stack[-1]) >= self.getPrecedence(token):
                   output.append(stack.pop())
               stack.append(token)
       while stack:
           output.append(stack.pop())
       return ''.join(output)

#Direct method
class DirectAFD:
   def __init__(self, value, position=None):
       self.value = value
       self.position = position
       self.left = None
       self.right = None
def increaseR(regex):
   return regex + '#.'
def construct_syntax_tree(postfix):
   stack = []
   tokens = []
   i = 0
   while i < len(postfix):
       if postfix[i] == '\\':
           tokens.append(postfix[i:i+2])
           i += 2
       else:
           tokens.append(postfix[i])
           i += 1
   for token in tokens:
       if token not in {'|', '*', '.'}:
           stack.append(DirectAFD(token))
   position = 0
   for token in postfix:
       if token.isalnum():
           node = DirectAFD(token, position)
           stack.append(node)
           position += 1
       elif token in ['.', '|', '#']:
           if token == '#':
               node = DirectAFD(token, position)
               stack.append(node)
               position += 1
           else:
               right = stack.pop()
               left = stack.pop()
               node = DirectAFD(token)
               node.left = left
               node.right = right
               stack.append(node)
       elif token == '*':
           operand = stack.pop()
           node = DirectAFD(token)
           node.left = operand
           stack.append(node)
   return stack.pop()
def label_leaves(node, label=0):
   if node:
       if node.left is None and node.right is None:
           node.position = label
           return label + 1
       label = label_leaves(node.left, label)
       label = label_leaves(node.right, label)
   return label
def calculate_nullable(node):
   if node is None:
       return False
   if node.value == '#':
       return True
   if node.value == '|':
       return calculate_nullable(node.left) or calculate_nullable(node.right)
   if node.value == '.':
       return calculate_nullable(node.left) and calculate_nullable(node.right)
   if node.value == '*':
       return True
   return False
def calculate_first_position(node):
   if node is None:
       return set()
   if node.value.isalnum() or node.value == '#':
       return {node.position}
   if node.value == '|':
       return calculate_first_position(node.left) | calculate_first_position(node.right)
   if node.value == '.':
       if calculate_nullable(node.left):
           return calculate_first_position(node.left) | calculate_first_position(node.right)
       else:
           return calculate_first_position(node.left)
   if node.value == '*':
       return calculate_first_position(node.left)
   return set()
def calculate_last_position(node):
   if node is None:
       return set()
   if node.value.isalnum() or node.value == '#':
       return {node.position}
   if node.value == '|':
       return calculate_last_position(node.left) | calculate_last_position(node.right)
   if node.value == '.':
       if calculate_nullable(node.right):
           return calculate_last_position(node.left) | calculate_last_position(node.right)
       else:
           return calculate_last_position(node.right)
   if node.value == '*':
       return calculate_last_position(node.left)
   return set()
def calculate_follow_pos(node, follow_pos=None):
   if follow_pos is None:
       follow_pos = {i: set() for i in range(label_leaves(node))}  # Initialize follow_pos with positions
   if node.value == '.':
       for pos in calculate_last_position(node.left):
           follow_pos[pos].update(calculate_first_position(node.right))
   elif node.value == '*':
       for pos in calculate_last_position(node):
           follow_pos[pos].update(calculate_first_position(node))
   if node.left:
       calculate_follow_pos(node.left, follow_pos)
   if node.right:
       calculate_follow_pos(node.right, follow_pos)
   return follow_pos
def find_node_by_position(node, position):
   if node is None:
       return None
   if node.position == position:
       return node
   left_result = find_node_by_position(node.left, position)
   if left_result is not None:
       return left_result
   right_result = find_node_by_position(node.right, position)
   if right_result is not None:
       return right_result
   return None
def construct_dfa_states_and_transitions(syntax_tree, follow_pos):
   alphabet = set()
   def extract_alphabet(node):
       if node:
           if node.value.isalnum():
               alphabet.add(node.value)
           extract_alphabet(node.left)
           extract_alphabet(node.right)
   extract_alphabet(syntax_tree)
   start_state = frozenset(calculate_first_position(syntax_tree))
   states = {start_state}
   dfa_transitions = {}
   queue = [start_state]
   while queue:
       current_state = queue.pop(0)
       for char in alphabet:
           next_state = set()
           for pos in current_state:
               node = find_node_by_position(syntax_tree, pos)
               if node and node.value == char:
                   next_state.update(follow_pos.get(pos, set()))
           next_state_frozen = frozenset(next_state)
           if next_state and next_state_frozen not in states:
               states.add(next_state_frozen)
               queue.append(next_state_frozen)
           if next_state:
               dfa_transitions[(current_state, char)] = next_state_frozen
   return states, dfa_transitions
def find_accept_states(states, syntax_tree):
   end_position = max(label_leaves(syntax_tree) - 1, 0)
   accept_states = {state for state in states if end_position in state}
   return accept_states
def draw_dfa(dfa_transitions, start_state, accept_states):
   graph = Digraph(format='png', graph_attr={'rankdir': 'LR'})
   states = sorted(set(key[0] for key in dfa_transitions.keys()).union(set(dfa_transitions.values())))
   state_to_number = {state: chr(ord('1') + i) for i, state in enumerate(states)}
   graph.attr('node', shape='none', width='0', height='0')
   graph.node('start', label='', shape='none')
   start_state_letter = state_to_number.get(start_state, 'X')
   graph.edge('start', start_state_letter, arrowhead='vee')
   for state, letter in state_to_number.items():
       shape = 'doublecircle' if state in accept_states else 'circle'
       graph.node(letter, label=letter, shape=shape)
   for (from_state, input_char), to_state in dfa_transitions.items():
       label = input_char
       from_state_str = state_to_number[from_state]
       to_state_str = state_to_number[to_state]
       graph.edge(from_state_str, to_state_str, label=label)
   graph.render('dfa_graph')
def applyDirect(regex):
   regex = parse_regex(regex)
   postfix = ShuntingYard(regex).shuntingYard()
   aumentada = increaseR(postfix)
   syntax_tree = construct_syntax_tree(aumentada)
   label_leaves(syntax_tree)
   follow_pos = calculate_follow_pos(syntax_tree)
   states, dfa_transitions = construct_dfa_states_and_transitions(syntax_tree, follow_pos)
   start_state = frozenset(calculate_first_position(syntax_tree))
   accept_states = find_accept_states(states, syntax_tree)
   draw_dfa(dfa_transitions, start_state, accept_states)
   return dfa_transitions, start_state, accept_states

#NFA union of all DFAs
class DFAUnion:
   def __init__(self):
       self.dfas = []
   def add_dfa(self, dfa_transitions, start_state, accept_states, token_action):
       self.dfas.append((dfa_transitions, start_state, accept_states, token_action))
   def union(self):
       afnd_transitions = {}
       afnd_start_state = 'start'
       afnd_accept_states = set()
       token_actions = {}
       afnd_transitions[afnd_start_state] = {}
       for dfa_transitions, start_state, accept_states, token_action in self.dfas:
           if None not in afnd_transitions[afnd_start_state]:
               afnd_transitions[afnd_start_state][None] = set()
           afnd_transitions[afnd_start_state][None].add(start_state)
           for state, transitions in dfa_transitions.items():
               if state not in afnd_transitions:
                   afnd_transitions[state] = {}
               for symbol, next_states in transitions.items():
                   if symbol not in afnd_transitions[state]:
                       afnd_transitions[state][symbol] = set()
                   afnd_transitions[state][symbol].update(next_states)
           afnd_accept_states.update(accept_states)
           for accept_state in accept_states:
               token_actions[accept_state] = token_action
       return afnd_transitions, afnd_start_state, afnd_accept_states, token_actions
def draw_afnd(transitions, start_state, accept_states, token_actions):
   graph = Digraph(format='png')
   for state in transitions.keys():
       if state in accept_states:
           token_action = token_actions.get(state, '')
           graph.node(str(state), f'{token_action}', shape='doublecircle')
       else:
           graph.node(str(state), str(state))
       for symbol, next_states in transitions[state].items():
           for next_state in next_states:
               graph.edge(str(state), str(next_state), label=str(symbol) if symbol else 'ε')
   MAX_LABEL_LENGTH = 100
   def truncate_label(label):
       return (label[:MAX_LABEL_LENGTH] + '..') if len(label) > MAX_LABEL_LENGTH else label
   for accept_state in accept_states:
       token_action = token_actions.get(accept_state, '')
       token_action = truncate_label(token_action)
       graph.node(str(accept_state), f'{token_action}', shape='doublecircle')
       graph.render('afnd', view=False)
#Analyzing with automatas
dfa_union = DFAUnion()
def convert_transitions(dfa_transitions):
    converted_transitions = {}
    for (state_frozenset, symbol), next_state_frozenset in dfa_transitions.items():
        state_str = str(state_frozenset)
        next_state_str = str(next_state_frozenset)
        if state_str not in converted_transitions:
            converted_transitions[state_str] = {}
        if symbol not in converted_transitions[state_str]:
            converted_transitions[state_str][symbol] = set()
        converted_transitions[state_str][symbol].add(next_state_str)
    return converted_transitions
for token, regex in tokens.items():
    dfa_transitions, start_state, accept_states = applyDirect(regex)
    draw_dfa(dfa_transitions, start_state, accept_states)
    os.rename('dfa_graph.png', f'dfa_graph_{token}.png')
    converted_transitions = convert_transitions(dfa_transitions)
    dfa_union.add_dfa(converted_transitions, start_state, accept_states, token)
afnd_transitions, afnd_start_state, afnd_accept_states, token_actions = dfa_union.union()
draw_afnd(afnd_transitions, afnd_start_state, afnd_accept_states, token_actions)

#Analyzing chars
def cerradura_epsilon(estados, afnd_transitions):
   cerradura = set(estados)
   pila = list(estados)
   while pila:
       estado = pila.pop()
       if estado in afnd_transitions and None in afnd_transitions[estado]:
           for prox_estado in afnd_transitions[estado][None]:
               if prox_estado not in cerradura:
                   cerradura.add(prox_estado)
                   pila.append(prox_estado)
   return cerradura
def analizar_cadena(afnd_transitions, afnd_start_state, afnd_accept_states, token_actions, cadena_entrada):
   estados_actuales = cerradura_epsilon({afnd_start_state}, afnd_transitions)
   for caracter in cadena_entrada:
       proximos_estados = set()
       for estado in estados_actuales:
           estado_str = str(estado)
           if estado_str in afnd_transitions and caracter in afnd_transitions[estado_str]:
               proximos_estados.update(afnd_transitions[estado_str][caracter])
       estados_actuales = cerradura_epsilon(proximos_estados, afnd_transitions)
   for estado in estados_actuales:
       estado_str = str(estado)
       if estado_str in afnd_accept_states:
           return token_actions[estado_str]
   return None
cadena_entrada = 'A'
accion_token = analizar_cadena(afnd_transitions, afnd_start_state, afnd_accept_states, token_actions, cadena_entrada)
if accion_token:
   print(f'La acción del token es: {accion_token}')
else:
   print('No se encontró un token válido para la cadena de entrada.')
