import re
from typing import List, Tuple

# Tokens are emitted as: (TYPE, LEXEME, POSITION)

TOKENS = [
    # Comments + whitespace
    ("COMMENT_MULTI", re.compile(r"/\*.*?\*/", re.DOTALL)),
    ("COMMENT_LINE", re.compile(r"//[^\n]*")),
    ("WHITESPACE", re.compile(r"\s+")),

    # Keywords
    ("IF", re.compile(r"\bif\b")),
    ("ELSE", re.compile(r"\belse\b")),
    ("WHILE", re.compile(r"\bwhile\b")),
    ("FOR", re.compile(r"\bfor\b")),
    ("RETURN", re.compile(r"\breturn\b")),
    ("BREAK", re.compile(r"\bbreak\b")),
    ("CONTINUE", re.compile(r"\bcontinue\b")),

    ("INT", re.compile(r"\bint\b")),
    ("CHAR", re.compile(r"\bchar\b")),
    ("VOID", re.compile(r"\bvoid\b")),
    ("FLOAT", re.compile(r"\bfloat\b")),
    ("DOUBLE", re.compile(r"\bdouble\b")),
    ("LONG", re.compile(r"\blong\b")),
    ("SHORT", re.compile(r"\bshort\b")),
    ("SIGNED", re.compile(r"\bsigned\b")),
    ("UNSIGNED", re.compile(r"\bunsigned\b")),
    ("STRUCT", re.compile(r"\bstruct\b")),
    ("ENUM", re.compile(r"\benum\b")),
    ("UNION", re.compile(r"\bunion\b")),
    ("BOOLEAN", re.compile(r"\b_Bool\b")),

    # Literals
    ("STRING_LITERAL", re.compile(r'"(\\.|[^"\\])*"')),
    ("CHAR_LITERAL", re.compile(r"'(\\.|[^'\\])'")),
    ("FLOAT_LITERAL", re.compile(r"\d+\.\d+")),
    ("INT_LITERAL", re.compile(r"\d+")),

    # Operators 
    ("INCREMENT", re.compile(r"\+\+")),
    ("DECREMENT", re.compile(r"--")),
    ("EQ", re.compile(r"==")),
    ("NE", re.compile(r"!=")),
    ("LE", re.compile(r"<=")),
    ("GE", re.compile(r">=")),
    ("LSHIFT", re.compile(r"<<")),
    ("RSHIFT", re.compile(r">>")),
    ("AND", re.compile(r"&&")),
    ("OR", re.compile(r"\|\|")),

    # Single-char operators
    ("ASSIGN", re.compile(r"=")),
    ("PLUS", re.compile(r"\+")),
    ("MINUS", re.compile(r"-")),
    ("MULTIPLY", re.compile(r"\*")),
    ("DIVIDE", re.compile(r"/")),
    ("MODULO", re.compile(r"%")),
    ("NOT", re.compile(r"!")),
    ("BITAND", re.compile(r"&")),
    ("BITOR", re.compile(r"\|")),
    ("XOR", re.compile(r"\^")),
    ("TILDE", re.compile(r"~")),
    ("QUESTION", re.compile(r"\?")),

    # Delimiters
    ("LPAREN", re.compile(r"\(")),
    ("RPAREN", re.compile(r"\)")),
    ("LBRACE", re.compile(r"\{")),
    ("RBRACE", re.compile(r"\}")),
    ("LBRACKET", re.compile(r"\[")),
    ("RBRACKET", re.compile(r"\]")),
    ("SEMICOLON", re.compile(r";")),
    ("COMMA", re.compile(r",")),
    ("COLON", re.compile(r":")),
    ("DOT", re.compile(r"\.")),

    # Identifiers
    ("IDENTIFIER", re.compile(r"[A-Za-z_][A-Za-z0-9_]*")),

    # Fallback
    ("UNKNOWN", re.compile(r".")),
]


def get_tokens(text: str) -> List[Tuple[str, str, int]]:
    """
    Convert source code into a list of tokens.
    Each token is (TYPE, LEXEME, POSITION).
    """
    tokens = []
    pos = 0

    while pos < len(text):
        for name, pattern in TOKENS:
            match = pattern.match(text, pos)
            if not match:
                continue

            lexeme = match.group(0)
            start = pos
            pos = match.end()

            # Skip whitespace and comments
            if name in ("WHITESPACE", "COMMENT_LINE", "COMMENT_MULTI"):
                break

            tokens.append((name, lexeme, start))
            break
        else:
            raise RuntimeError(f"Lexer stuck at position {pos}")

    return tokens
