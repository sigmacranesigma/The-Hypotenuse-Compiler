import re    #not in use yet, will be used later on

#tokens should be self-explanatory, everything has a tag, whitespace is ignored later on
#order matters, FLOAT must be before INTEGER to avoid misclassification
Tokens = [
    ("FLOAT", r"\d+\.\d+"),
    ("INTEGER", r"\d+"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MULTIPLY", r"\*"),
    ("DIVIDE", r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("WHITESPACE", r"\s+"),
    ('ASSIGN', r'='),
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("SEMICOLON", r";"),
    ('COMMA', r","),
    ('COLON', r':'),
    ("STRING", r'"(.*?)"')
]
