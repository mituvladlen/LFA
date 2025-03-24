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

# Example usage
input_text = "69 + 3.14 - 6 * 2 / (1 + 2)"
lexer = Lexer(input_text)
tokens = lexer.tokenize()
print("Input:", input_text)
for token in tokens:
    print(token)
