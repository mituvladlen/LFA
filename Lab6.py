import re
from enum import Enum


class TokenType(Enum):
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    SIN = "SIN"
    COS = "COS"


class Token:
    def __init__(self, type_, value):
        self.type = type_.value  # Store only the string value
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.token_patterns = [
            (r'\d+\.\d+|\d+', TokenType.NUMBER),
            (r'\+', TokenType.PLUS),
            (r'-', TokenType.MINUS),
            (r'\*', TokenType.MULTIPLY),
            (r'/', TokenType.DIVIDE),
            (r'\(', TokenType.LPAREN),
            (r'\)', TokenType.RPAREN),
            (r'sin', TokenType.SIN),
            (r'cos', TokenType.COS)
        ]

    def tokenize(self):
        tokens = []
        while self.pos < len(self.text):
            match = None
            for pattern, token_type in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(self.text, self.pos)
                if match:
                    tokens.append(Token(token_type, match.group(0)))
                    self.pos = match.end()
                    break

            if not match:
                if self.text[self.pos].isspace():
                    self.pos += 1
                    continue
                raise ValueError(f"Unexpected character: {self.text[self.pos]}")

        return tokens


# AST Node Classes
class ASTNode:
    def pretty_print(self, level=0):
        raise NotImplementedError("Subclasses must implement pretty_print")


class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def pretty_print(self, level=0):
        return f"{'    ' * level}└── NUMBER({self.value})"


class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def pretty_print(self, level=0):
        result = f"{'    ' * level}└── OPERATION({self.operator})\n"
        result += self.left.pretty_print(level + 1) + "\n"
        result += self.right.pretty_print(level + 1)
        return result


class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def pretty_print(self, level=0):
        result = f"{'    ' * level}└── FUNCTION({self.operator})\n"
        result += self.operand.pretty_print(level + 1)
        return result


# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        if self.current_token() and self.current_token().type == token_type.value:
            self.pos += 1
        else:
            raise ValueError(f"Expected token {token_type}, got {self.current_token()}")

    def parse(self):
        return self.expr()

    def factor(self):
        token = self.current_token()

        if token.type == TokenType.NUMBER.value:
            self.eat(TokenType.NUMBER)
            return NumberNode(float(token.value))

        elif token.type == TokenType.LPAREN.value:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        elif token.type in {TokenType.SIN.value, TokenType.COS.value}:
            self.eat(TokenType(token.type))
            operand = self.factor()
            return UnaryOpNode(token.type, operand)

        raise ValueError(f"Unexpected token: {token}")

    def term(self):
        node = self.factor()

        while self.current_token() and self.current_token().type in {TokenType.MULTIPLY.value, TokenType.DIVIDE.value}:
            token = self.current_token()
            self.eat(TokenType(token.type))
            node = BinaryOpNode(node, token.type, self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token() and self.current_token().type in {TokenType.PLUS.value, TokenType.MINUS.value}:
            token = self.current_token()
            self.eat(TokenType(token.type))
            node = BinaryOpNode(node, token.type, self.term())

        return node


# Example usage
input_text = "64+cos(2) - sin(2)"
lexer = Lexer(input_text)
tokens = lexer.tokenize()
print("Tokens:")
for token in tokens:
    print(token)  # Print each token on a new line

parser = Parser(tokens)
ast = parser.parse()
print("\nAST:")
print(ast.pretty_print())
