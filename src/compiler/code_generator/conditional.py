from src.compiler.errors import CompilerError
from src.compiler.code_generator.type import Quad, OperationType, Operand
from src.compiler.stack_allocator.types import ValueType

"""
Conditional semantic actions
"""


class ConditionalActions:
    def __init__(self, quad_list):
        self.goto_jumps = []
        self.goto_f_jumps = []
        self.quad_list = quad_list

    def get_conditional(self, operand_list):
        expression: Operand = operand_list.pop()
        if expression.type_ is not ValueType.BOOL:
            return CompilerError("Type Error, if expression should be boolean")

        quad = Quad(
            operation=OperationType.GOTOF,
            left_address=expression.address, right_address=None
        )

        self.goto_f_jumps.append(len(self.quad_list))  # current quad
        self.quad_list.append(quad)

    def fill_and_goto(self):  # used after each else / elseif to fill gotof
        self.__fill_gotof(1)
        if len(self.goto_jumps) > 0:
            self.__fill_goto()

        goto_quad = Quad(operation=OperationType.GOTO,
                         left_address=None, result_address=None)
        self.goto_jumps.append(len(self.quad_list))
        self.quad_list.append(goto_quad)

    def fill_end_single(self):
        self.__fill_gotof(0)

    def fill_end(self):  # used to fill last goto
        index = self.goto_jumps.pop()
        self.quad_list[index].result_address = len(self.quad_list)  # next quad

    def __fill_gotof(self, skip):
        pending_jump_index = self.goto_f_jumps.pop()
        self.quad_list[pending_jump_index].result_address = len(
            self.quad_list)+skip

    def __fill_goto(self):
        pending_jump_index = self.goto_jumps.pop()
        self.quad_list[pending_jump_index].result_address = len(self.quad_list)
