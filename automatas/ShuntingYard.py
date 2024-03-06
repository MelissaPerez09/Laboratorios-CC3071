"""
ShunttungYard.py
Uses Shuting Yard algorithm to parse infix expression to postfix
"""

class ShuntingYard:
    # Constructor
    def __init__(self, input_string):
        self.tokens = self.tokenize(input_string)
        self.epsilon = "ε"

    """
    Tokenize the input string
    :param input_string: Input string
    Divide la cadena en tokens y coloca concatenaciones implícitas
    """
    def tokenize(self, input_string):
        cleaned = input_string.replace(" ", "")
        tokens = list(cleaned)
        i = 0
        while i < len(tokens) - 1:
            if (tokens[i].isalnum() or tokens[i] in ['*', '\t', '\n', '\s']) and (tokens[i+1].isalnum() or tokens[i+1] in ['(', '\t', '\n']):
                tokens.insert(i+1, '.')
            i += 1
        return tokens

    """
    Get precedence of operator
    :param operator: Operator
    devuelve la precedencia de un operador
    """
    def getPrecedence(self, operator):
        precedence = {'|': 1, '*': 3, '.': 2}
        return precedence.get(operator, 0)

    """
    Shunting Yard algorithm
    :param tokens: Tokens
    Convierte la expresión regular de la notación infija a la notación postfija
    Recorre la lista de tokens y los va colocando en la pila o en la salida dependiendo de su precedencia
    """
    def shuntingYard(self):
        # Lists to store output and stack
        output = []
        stack = []
        
        # Iterate through tokens
        escape_next = False

        for token in self.tokens:
            if escape_next:
                output.append('\\' + token)
                escape_next = False
            elif token == '\\':
                escape_next = True
            # If token is an operand, append to output
            elif token.isalnum() or token in [' ', '\t', '\n', '\s']:
                output.append(token if token != self.epsilon else "ε")
            # If token is an operator or parenthesis append to stack
            elif token == "(":
                stack.append(token)
            elif token == ")":
                # Pop parenthesis from stack
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                if stack:
                    stack.pop()
            else:
                # Pop operators from stack with higher precedence to output
                while stack and self.getPrecedence(stack[-1]) >= self.getPrecedence(token):
                    output.append(stack.pop())
                stack.append(token)

        # Pop remaining operators from stack
        while stack:
            output.append(stack.pop())

        # Return the postfix expression
        return "".join(output)

# programmed by @melissaperez_