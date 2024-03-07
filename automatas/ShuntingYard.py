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
        tokens = []
        i = 0
        while i < len(cleaned):
            if cleaned[i] == '\\':
                if i + 1 < len(cleaned):
                    tokens.append(cleaned[i] + cleaned[i + 1])
                    i += 2
                else:
                    raise ValueError("Invalid escaped character at the end of input string")
            elif cleaned[i] in {' ', '\t', '\n'}:
                # Handle whitespace characters
                tokens.append(f'\\{cleaned[i]}')
                i += 1
            else:
                tokens.append(cleaned[i])
                i += 1

        # Add implicit concatenation
        i = 0
        while i < len(tokens) - 1:
            if (tokens[i].isalnum() or tokens[i] == ')' or tokens[i] == '*') and \
            (tokens[i + 1].isalnum() or tokens[i + 1] == '('):
                tokens.insert(i + 1, '.')
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
        for token in self.tokens:
            # If token is an operand, append to output
            if token.isalnum():
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