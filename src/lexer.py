import re    #not in use yet, will be used later on
import sys
# whoever comments unnecessarily will be murdered
#order matters, there might be errors if certain elements are not in the right order

Tokens = [
    ('IF', re.compile(r'\bif\b')),
    ('ELSE', re.compile(r'\belse\b')),
    ('WHILE', re.compile(r'\bwhile\b')),
    ('FOR', re.compile(r'\bfor\b')),
    ('RETURN', re.compile(r'\breturn\b')),

    ('PLUS', re.compile(r'\+')),
    ('MINUS', re.compile(r'-')),
    ('MULTIPLY', re.compile(r'\*')),
    ('DIVIDE', re.compile(r'/')),
    ('LPAREN', re.compile(r'\(')),
    ('RPAREN', re.compile(r'\)')),
    ('ASSIGN', re.compile(r'=')),
    ('SEMICOLON', re.compile(r';')),
    ('COMMA', re.compile(r',')),
    ('COLON', re.compile(r':')),

    ('IDENTIFIER', re.compile(r'[A-Za-z_][A-Za-z0-9_]*')),
    ('WHITESPACE', re.compile(r'\s+'))
]

#under construction, not finished yet, and will not work properly
#function to get token list goes here
def get_tokens(argv[1]):
    # here turns the input into a list then cuts it into smaller parts
    var = argv
    while var:
        for token in Tokens:
            match = token[1].match(var)
            if match:
                lexeme = match.group(0)
                if token[0] != 'WHITESPACE':  #skip whitespace tokens
                    print(f'Token: {token[0]}, Lexeme: {lexeme}')
                var = var[len(lexeme):]  #move forward in the input string
                break
        else:
            print(f'Unknown token: {var[0]}')
            var = var[1:]  #skip unknown character

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit()
    else:
        get_tokens(sys.argv)
