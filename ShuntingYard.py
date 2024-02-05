"""
ShunttungYard.py
Uses Shuting Yard algorithm to parse infix expression to postfix
"""

import re
class ShuntingYard:
    # Constructor
    def __init__(self, input_string):
        self.tokens = self.tokenize(input_string)
        self.epsilon = "ε"

    # Tokenize the input string
    def tokenize(self, input_string):
        cleaned = re.sub(r'\s+', "", input_string)
        return list(cleaned)

    # Get precedence of operator
    def getPrecedence(self, operator):
        precedence = {'|': 1, '+': 3, '?': 3, '*': 3, '.': 2}
        return precedence.get(operator, 0)

    # Shunting Yard algorithm
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
                while stack and self.getPrecedence(stack[-1]) > self.getPrecedence(token):
                    output.append(stack.pop())
                stack.append(token)

        # Pop remaining operators from stack
        while stack:
            output.append(stack.pop())

        # Return the postfix expression
        return "".join(output)
