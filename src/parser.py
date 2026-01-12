from dataclasses import dataclass
from typing import List, Optional, Any, Tuple

Token = Tuple[str, str, int]  # (TYPE, LEXEME, POSITION)

# =========================
# AST NODE DEFINITIONS
# =========================

@dataclass
class Node:
    pass

@dataclass
class Program(Node):
    declarations: List[Node]

@dataclass
class Function(Node):
    ret_type: str
    name: str
    params: List[Tuple[str, str]]
    body: Node

@dataclass
class Declaration(Node):
    var_type: str
    name: str
    initializer: Optional[Node]

@dataclass
class Compound(Node):
    stmts: List[Node]

@dataclass
class If(Node):
    cond: Node
    then_branch: Node
    else_branch: Optional[Node]

@dataclass
class While(Node):
    cond: Node
    body: Node

@dataclass
class For(Node):
    init: Optional[Node]
    cond: Optional[Node]
    post: Optional[Node]
    body: Node

@dataclass
class Return(Node):
    expr: Optional[Node]

@dataclass
class ExprStmt(Node):
    expr: Optional[Node]

@dataclass
class Binary(Node):
    op: str
    left: Node
    right: Node

@dataclass
class Unary(Node):
    op: str
    operand: Node
    prefix: bool = True

@dataclass
class Literal(Node):
    value: Any

@dataclass
class Var(Node):
    name: str

@dataclass
class Assignment(Node):
    target: Node
    value: Node

@dataclass
class Call(Node):
    callee: Node
    args: List[Node]

@dataclass
class ArrayAccess(Node):
    array: Node
    index: Node


# =========================
# PARSER IMPLEMENTATION
# =========================

class Parser:
    """
    Recursive-descent parser for a C-like language.
    Uses precedence climbing for expressions.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.i = 0  # current token index

    # -------------------------
    # Utility methods
    # -------------------------

    def peek(self) -> Token:
        """Look at the current token without consuming it."""
        return self.tokens[self.i]

    def advance(self) -> Token:
        """Consume and return the current token."""
        tok = self.tokens[self.i]
        self.i += 1
        return tok

    def accept(self, kind: str) -> Optional[Token]:
        """
        If the current token matches `kind`, consume it.
        Otherwise return None.
        """
        if self.peek()[0] == kind:
            return self.advance()
        return None

    def expect(self, kind: str) -> Token:
        """
        Require the current token to be of `kind`.
        Throws a syntax error if it isn't.
        """
        tok = self.peek()
        if tok[0] == kind:
            return self.advance()
        raise SyntaxError(f"Expected {kind} at {tok[2]}, got {tok[0]}")

    # -------------------------
    # Top-level grammar
    # -------------------------

    def parse_program(self) -> Program:
        """
        program → { external_declaration } EOF
        """
        decls = []
        while self.peek()[0] != "EOF":
            decls.append(self.parse_external())
        return Program(decls)

    def parse_external(self) -> Node:
        """
        Handles:
          - function definitions
          - global variable declarations
        """
        if self.peek()[0] in (
            "INT","CHAR","VOID","FLOAT","DOUBLE",
            "LONG","SHORT","SIGNED","UNSIGNED",
            "STRUCT","ENUM","UNION","BOOLEAN"
        ):
            type_name = self.advance()[1]
            name = self.expect("IDENTIFIER")[1]

            # Function
            if self.accept("LPAREN"):
                params = []
                if not self.accept("RPAREN"):
                    while True:
                        ptype = self.advance()[1]
                        pname = self.expect("IDENTIFIER")[1]
                        params.append((ptype, pname))
                        if not self.accept("COMMA"):
                            self.expect("RPAREN")
                            break

                body = self.parse_compound()
                return Function(type_name, name, params, body)

            # Variable
            init = None
            if self.accept("ASSIGN"):
                init = self.parse_expression()
            self.expect("SEMICOLON")
            return Declaration(type_name, name, init)

        raise SyntaxError(f"Unexpected token {self.peek()}")

    # -------------------------
    # Statements
    # -------------------------

    def parse_statement(self) -> Node:
        tok = self.peek()[0]

        if tok == "LBRACE":
            return self.parse_compound()

        if tok == "IF":
            self.advance()
            self.expect("LPAREN")
            cond = self.parse_expression()
            self.expect("RPAREN")
            then_branch = self.parse_statement()
            else_branch = None
            if self.accept("ELSE"):
                else_branch = self.parse_statement()
            return If(cond, then_branch, else_branch)

        if tok == "WHILE":
            self.advance()
            self.expect("LPAREN")
            cond = self.parse_expression()
            self.expect("RPAREN")
            body = self.parse_statement()
            return While(cond, body)

        if tok == "RETURN":
            self.advance()
            expr = None
            if self.peek()[0] != "SEMICOLON":
                expr = self.parse_expression()
            self.expect("SEMICOLON")
            return Return(expr)

        # Expression statement
        expr = None
        if tok != "SEMICOLON":
            expr = self.parse_expression()
        self.expect("SEMICOLON")
        return ExprStmt(expr)

    def parse_compound(self) -> Compound:
        """ { statement* } """
        self.expect("LBRACE")
        stmts = []
        while self.peek()[0] != "RBRACE":
            stmts.append(self.parse_statement())
        self.expect("RBRACE")
        return Compound(stmts)

    # -------------------------
    # Expressions (precedence)
    # -------------------------

    def parse_expression(self) -> Node:
        return self.parse_assignment()

    def parse_assignment(self) -> Node:
        node = self.parse_logical_or()
        if self.accept("ASSIGN"):
            return Assignment(node, self.parse_assignment())
        return node

    def parse_logical_or(self) -> Node:
        node = self.parse_logical_and()
        while self.accept("OR"):
            node = Binary("||", node, self.parse_logical_and())
        return node

    def parse_logical_and(self) -> Node:
        node = self.parse_equality()
        while self.accept("AND"):
            node = Binary("&&", node, self.parse_equality())
        return node

    def parse_equality(self) -> Node:
        node = self.parse_relational()
        while True:
            if self.accept("EQ"):
                node = Binary("==", node, self.parse_relational())
            elif self.accept("NE"):
                node = Binary("!=", node, self.parse_relational())
            else:
                break
        return node

    def parse_relational(self) -> Node:
        node = self.parse_additive()
        while True:
            if self.accept("LT"):
                node = Binary("<", node, self.parse_additive())
            elif self.accept("GT"):
                node = Binary(">", node, self.parse_additive())
            elif self.accept("LE"):
                node = Binary("<=", node, self.parse_additive())
            elif self.accept("GE"):
                node = Binary(">=", node, self.parse_additive())
            else:
                break
        return node

    def parse_additive(self) -> Node:
        node = self.parse_multiplicative()
        while True:
            if self.accept("PLUS"):
                node = Binary("+", node, self.parse_multiplicative())
            elif self.accept("MINUS"):
                node = Binary("-", node, self.parse_multiplicative())
            else:
                break
        return node

    def parse_multiplicative(self) -> Node:
        node = self.parse_unary()
        while True:
            if self.accept("MULTIPLY"):
                node = Binary("*", node, self.parse_unary())
            elif self.accept("DIVIDE"):
                node = Binary("/", node, self.parse_unary())
            elif self.accept("MODULO"):
                node = Binary("%", node, self.parse_unary())
            else:
                break
        return node

    def parse_unary(self) -> Node:
        if self.accept("PLUS"):
            return Unary("+", self.parse_unary())
        if self.accept("MINUS"):
            return Unary("-", self.parse_unary())
        if self.accept("NOT"):
            return Unary("!", self.parse_unary())
        return self.parse_postfix()

    def parse_postfix(self) -> Node:
        node = self.parse_primary()
        while True:
            if self.accept("LPAREN"):
                args = []
                if not self.accept("RPAREN"):
                    while True:
                        args.append(self.parse_expression())
                        if not self.accept("COMMA"):
                            self.expect("RPAREN")
                            break
                node = Call(node, args)
            elif self.accept("LBRACKET"):
                idx = self.parse_expression()
                self.expect("RBRACKET")
                node = ArrayAccess(node, idx)
            else:
                break
        return node

    def parse_primary(self) -> Node:
        tok = self.peek()
        if tok[0] == "IDENTIFIER":
            self.advance()
            return Var(tok[1])
        if tok[0] in ("INT_LITERAL", "FLOAT_LITERAL", "STRING_LITERAL", "CHAR_LITERAL"):
            self.advance()
            return Literal(tok[1])
        if self.accept("LPAREN"):
            expr = self.parse_expression()
            self.expect("RPAREN")
            return expr
        raise SyntaxError(f"Unexpected token {tok}")
