from src.semantic.expression import Operand, Operator
from src.semantic.quadruple import Quad

"""
Conditional semantic actions
"""


class Builtin_Function_Actions:
    def __init__(self, quad_list):
        self.quad_list = quad_list

    def execute_call(self, operators, operands):
        operator: Operator = operators.pop()

        if operator.type_ is operator.type_.PRINT:
            return self.execute_print(operator, operands)

    def execute_print(self, operator, operands):
        expression: Operand = operands.pop()

        quad = Quad(operation=operator.type_.value, result_address=expression.address)
        self.quad_list.append(quad)
