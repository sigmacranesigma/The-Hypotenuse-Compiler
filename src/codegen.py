from parser import *

class PythonCodeGen:
    def __init__(self):
        self.lines = []
        self.indent = 0

    def emit(self, line=""):
        self.lines.append("    " * self.indent + line)

    def generate(self, node: Node) -> str:
        self.gen(node)
        return "\n".join(self.lines)

    # dispatch
    def gen(self, node):
        method = "gen_" + node.__class__.__name__
        if hasattr(self, method):
            return getattr(self, method)(node)
        else:
            raise NotImplementedError(f"No codegen for {type(node).__name__}")

    # top level stuffs
    def gen_Program(self, node: Program):
        for decl in node.declarations:
            self.gen(decl)

    def gen_Function(self, node: Function):
        params = ", ".join(name for _, name in node.params)
        self.emit(f"def {node.name}({params}):")
        self.indent += 1
        self.gen(node.body)
        self.indent -= 1
        self.emit()

    def gen_Compound(self, node: Compound):
        if not node.stmts:
            self.emit("pass")
        for stmt in node.stmts:
            self.gen(stmt)

    # statements
    def gen_Declaration(self, node: Declaration):
        if node.initializer:
            expr = self.gen_expr(node.initializer)
            self.emit(f"{node.name} = {expr}")
        else:
            self.emit(f"{node.name} = None")

    def gen_Return(self, node: Return):
        if node.expr:
            self.emit(f"return {self.gen_expr(node.expr)}")
        else:
            self.emit("return")

    def gen_ExprStmt(self, node: ExprStmt):
        if node.expr:
            self.emit(self.gen_expr(node.expr))

    def gen_If(self, node: If):
        self.emit(f"if {self.gen_expr(node.cond)}:")
        self.indent += 1
        self.gen(node.then_branch)
        self.indent -= 1
        if node.else_branch:
            self.emit("else:")
            self.indent += 1
            self.gen(node.else_branch)
            self.indent -= 1

    def gen_While(self, node: While):
        self.emit(f"while {self.gen_expr(node.cond)}:")
        self.indent += 1
        self.gen(node.body)
        self.indent -= 1

    def gen_For(self, node: For):
        # c style for while loop
        if node.init:
            self.gen(node.init)

        cond = self.gen_expr(node.cond) if node.cond else "True"
        self.emit(f"while {cond}:")
        self.indent += 1
        self.gen(node.body)
        if node.post:
            self.emit(self.gen_expr(node.post))
        self.indent -= 1

    # expressions yayyy
    def gen_expr(self, node: Node) -> str:
        if isinstance(node, Literal):
            return repr(node.value)

        if isinstance(node, Var):
            return node.name

        if isinstance(node, Binary):
            return f"({self.gen_expr(node.left)} {node.op} {self.gen_expr(node.right)})"

        if isinstance(node, Unary):
            if node.prefix:
                return f"({node.op}{self.gen_expr(node.operand)})"
            else:
                return f"({self.gen_expr(node.operand)}{node.op})"

        if isinstance(node, Assignment):
            return f"{self.gen_expr(node.target)} = {self.gen_expr(node.value)}"

        if isinstance(node, Call):
            args = ", ".join(self.gen_expr(a) for a in node.args)
            return f"{self.gen_expr(node.callee)}({args})"

        if isinstance(node, ArrayAccess):
            return f"{self.gen_expr(node.array)}[{self.gen_expr(node.index)}]"

        raise NotImplementedError(f"No expr codegen for {type(node).__name__}")
