import ast
import sys
from typing import Dict, Any, List, Optional

class Token:
    def __init__(self, type: str, value: Any, line: int):
        self.type = type
        self.value = value
        self.line = line

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> List[ast.AST]:
        statements = []
        while not self.is_at_end():
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self) -> ast.AST:
        if self.match("FUNCTION"):
            return self.parse_function()
        elif self.match("IF"):
            return self.parse_if()
        elif self.match("IMPORT"):
            return self.parse_import()
        else:
            return self.parse_expression_statement()

    def parse_function(self) -> ast.FunctionDef:
        name = self.consume("IDENTIFIER", "Expected function name").value
        self.consume("LEFT_PAREN", "Expected '(' after function name")
        params = self.parse_parameters()
        self.consume("RIGHT_PAREN", "Expected ')' after parameters")
        body = self.parse_block()
        return ast.FunctionDef(name=name, args=params, body=body)

    def parse_parameters(self) -> List[str]:
        params = []
        if not self.check("RIGHT_PAREN"):
            while True:
                params.append(self.consume("IDENTIFIER", "Expected parameter name").value)
                if not self.match("COMMA"):
                    break
        return params

    def parse_block(self) -> List[ast.AST]:
        statements = []
        self.consume("LEFT_BRACE", "Expected '{' before block")
        while not self.check("RIGHT_BRACE") and not self.is_at_end():
            statements.append(self.parse_statement())
        self.consume("RIGHT_BRACE", "Expected '}' after block")
        return statements

    def parse_if(self) -> ast.If:
        condition = self.parse_expression()
        then_branch = self.parse_block()
        else_branch = None
        if self.match("ELSE"):
            else_branch = self.parse_block()
        return ast.If(test=condition, body=then_branch, orelse=else_branch)

    def parse_import(self) -> ast.Import:
        module = self.consume("STRING", "Expected module name").value
        return ast.Import(names=[ast.alias(name=module, asname=None)])

    def parse_expression_statement(self) -> ast.Expr:
        expr = self.parse_expression()
        self.consume("SEMICOLON", "Expected ';' after expression")
        return ast.Expr(value=expr)

    def parse_expression(self) -> ast.AST:
        return self.parse_assignment()

    def parse_assignment(self) -> ast.AST:
        expr = self.parse_equality()
        if self.match("EQUAL"):
            value = self.parse_assignment()
            if isinstance(expr, ast.Name):
                return ast.Assign(targets=[expr], value=value)
            raise SyntaxError("Invalid assignment target")
        return expr

    def parse_equality(self) -> ast.AST:
        expr = self.parse_comparison()
        while self.match("EQUAL_EQUAL", "BANG_EQUAL"):
            operator = self.previous()
            right = self.parse_comparison()
            expr = ast.Compare(left=expr, ops=[operator.type], comparators=[right])
        return expr

    def parse_comparison(self) -> ast.AST:
        expr = self.parse_term()
        while self.match("LESS", "LESS_EQUAL", "GREATER", "GREATER_EQUAL"):
            operator = self.previous()
            right = self.parse_term()
            expr = ast.Compare(left=expr, ops=[operator.type], comparators=[right])
        return expr

    def parse_term(self) -> ast.AST:
        expr = self.parse_factor()
        while self.match("PLUS", "MINUS"):
            operator = self.previous()
            right = self.parse_factor()
            expr = ast.BinOp(left=expr, op=operator.type, right=right)
        return expr

    def parse_factor(self) -> ast.AST:
        expr = self.parse_unary()
        while self.match("STAR", "SLASH"):
            operator = self.previous()
            right = self.parse_unary()
            expr = ast.BinOp(left=expr, op=operator.type, right=right)
        return expr

    def parse_unary(self) -> ast.AST:
        if self.match("BANG", "MINUS"):
            operator = self.previous()
            right = self.parse_unary()
            return ast.UnaryOp(op=operator.type, operand=right)
        return self.parse_primary()

    def parse_primary(self) -> ast.AST:
        if self.match("FALSE"): return ast.Constant(value=False)
        if self.match("TRUE"): return ast.Constant(value=True)
        if self.match("NUMBER"): return ast.Constant(value=self.previous().value)
        if self.match("STRING"): return ast.Constant(value=self.previous().value)
        if self.match("IDENTIFIER"):
            name = self.previous().value
            if self.match("LEFT_PAREN"):
                args = self.parse_arguments()
                return ast.Call(func=ast.Name(id=name), args=args)
            return ast.Name(id=name)
        if self.match("LEFT_PAREN"):
            expr = self.parse_expression()
            self.consume("RIGHT_PAREN", "Expected ')' after expression")
            return ast.Grouping(expression=expr)
        raise SyntaxError(f"Unexpected token: {self.peek()}")

    def parse_arguments(self) -> List[ast.AST]:
        args = []
        if not self.check("RIGHT_PAREN"):
            while True:
                args.append(self.parse_expression())
                if not self.match("COMMA"):
                    break
        self.consume("RIGHT_PAREN", "Expected ')' after arguments")
        return args

    def match(self, *types: str) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type: str) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == "EOF"

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, type: str, message: str) -> Token:
        if self.check(type):
            return self.advance()
        raise SyntaxError(f"{message} at line {self.peek().line}")

class Interpreter:
    def __init__(self):
        self.globals = {}
        self.environment = self.globals
        self.locals = {}

    def interpret(self, statements: List[ast.AST]) -> None:
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            print(f"Runtime error: {error}")

    def execute(self, stmt: ast.AST) -> None:
        if isinstance(stmt, ast.Expr):
            self.evaluate(stmt.value)
        elif isinstance(stmt, ast.FunctionDef):
            self.execute_function(stmt)
        elif isinstance(stmt, ast.If):
            self.execute_if(stmt)
        elif isinstance(stmt, ast.Import):
            self.execute_import(stmt)
        elif isinstance(stmt, ast.Assign):
            self.execute_assign(stmt)

    def execute_function(self, stmt: ast.FunctionDef) -> None:
        func = ast.Function(
            name=stmt.name,
            params=stmt.args,
            body=stmt.body,
            closure=self.environment
        )
        self.environment[stmt.name] = func

    def execute_if(self, stmt: ast.If) -> None:
        if self.is_truthy(self.evaluate(stmt.test)):
            self.execute_block(stmt.body, self.environment)
        elif stmt.orelse is not None:
            self.execute_block(stmt.orelse, self.environment)

    def execute_import(self, stmt: ast.Import) -> None:
        module_name = stmt.names[0].name
        try:
            module = __import__(module_name)
            self.environment[module_name] = module
        except ImportError as e:
            raise RuntimeError(f"Failed to import module '{module_name}': {e}")

    def execute_assign(self, stmt: ast.Assign) -> None:
        value = self.evaluate(stmt.value)
        for target in stmt.targets:
            if isinstance(target, ast.Name):
                self.environment[target.id] = value
            else:
                raise RuntimeError("Invalid assignment target")

    def execute_block(self, statements: List[ast.AST], environment: Dict[str, Any]) -> None:
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def evaluate(self, expr: ast.AST) -> Any:
        if isinstance(expr, ast.Constant):
            return expr.value
        elif isinstance(expr, ast.Name):
            return self.lookup_variable(expr)
        elif isinstance(expr, ast.BinOp):
            return self.evaluate_binary(expr)
        elif isinstance(expr, ast.UnaryOp):
            return self.evaluate_unary(expr)
        elif isinstance(expr, ast.Call):
            return self.evaluate_call(expr)
        elif isinstance(expr, ast.Compare):
            return self.evaluate_comparison(expr)
        elif isinstance(expr, ast.Grouping):
            return self.evaluate(expr.expression)
        raise RuntimeError(f"Unknown expression type: {type(expr)}")

    def evaluate_binary(self, expr: ast.BinOp) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        if expr.op == "PLUS":
            if isinstance(left, (str, int, float)) and isinstance(right, (str, int, float)):
                return left + right
            raise RuntimeError("Operands must be numbers or strings")
        elif expr.op == "MINUS":
            self.check_number_operands(expr.op, left, right)
            return left - right
        elif expr.op == "STAR":
            self.check_number_operands(expr.op, left, right)
            return left * right
        elif expr.op == "SLASH":
            self.check_number_operands(expr.op, left, right)
            if right == 0:
                raise RuntimeError("Division by zero")
            return left / right
        raise RuntimeError(f"Unknown binary operator: {expr.op}")

    def evaluate_unary(self, expr: ast.UnaryOp) -> Any:
        right = self.evaluate(expr.operand)
        
        if expr.op == "MINUS":
            self.check_number_operand(expr.op, right)
            return -right
        elif expr.op == "BANG":
            return not self.is_truthy(right)
        raise RuntimeError(f"Unknown unary operator: {expr.op}")

    def evaluate_call(self, expr: ast.Call) -> Any:
        callee = self.evaluate(expr.func)
        if not callable(callee):
            raise RuntimeError("Can only call functions")
        
        args = [self.evaluate(arg) for arg in expr.args]
        return callee(*args)

    def evaluate_comparison(self, expr: ast.Compare) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.comparators[0])
        
        if expr.ops[0] == "EQUAL_EQUAL":
            return self.is_equal(left, right)
        elif expr.ops[0] == "BANG_EQUAL":
            return not self.is_equal(left, right)
        elif expr.ops[0] == "LESS":
            self.check_number_operands(expr.ops[0], left, right)
            return left < right
        elif expr.ops[0] == "LESS_EQUAL":
            self.check_number_operands(expr.ops[0], left, right)
            return left <= right
        elif expr.ops[0] == "GREATER":
            self.check_number_operands(expr.ops[0], left, right)
            return left > right
        elif expr.ops[0] == "GREATER_EQUAL":
            self.check_number_operands(expr.ops[0], left, right)
            return left >= right
        raise RuntimeError(f"Unknown comparison operator: {expr.ops[0]}")

    def is_truthy(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    def is_equal(self, a: Any, b: Any) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def check_number_operand(self, operator: str, operand: Any) -> None:
        if isinstance(operand, (int, float)):
            return
        raise RuntimeError(f"Operand must be a number for operator {operator}")

    def check_number_operands(self, operator: str, left: Any, right: Any) -> None:
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise RuntimeError(f"Operands must be numbers for operator {operator}")

    def lookup_variable(self, name: ast.Name) -> Any:
        distance = self.locals.get(name)
        if distance is not None:
            return self.environment[name.id]
        return self.globals.get(name.id)

def run_file(path: str) -> None:
    with open(path, 'r') as file:
        source = file.read()
    
    # TODO: Implement lexer to convert source to tokens
    tokens = []  # This will be populated by the lexer
    
    parser = Parser(tokens)
    statements = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(statements)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        print("Usage: python learn_step1_interpreter.py <script.pcsj>") 