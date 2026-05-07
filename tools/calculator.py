"""
Calculator tool with safe expression parsing.
"""

import ast
import operator
from typing import Union

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _eval_node(node: ast.AST) -> Union[int, float]:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numbers are allowed.")

    if isinstance(node, ast.BinOp):
        if type(node.op) not in OPS:
            raise ValueError("Operator not supported.")
        return OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in OPS:
            raise ValueError("Unary operator not supported.")
        return OPS[type(node.op)](_eval_node(node.operand))

    raise ValueError("Invalid expression.")


def calculate(expression: str) -> str:
    """Safely calculate a math expression string."""
    try:
        parsed = ast.parse(expression, mode="eval")
        result = _eval_node(parsed.body)
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {e}"
