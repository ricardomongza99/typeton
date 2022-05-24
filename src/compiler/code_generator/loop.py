from src.compiler.errors import CompilerError
from src.compiler.code_generator.type import Operand
from src.compiler.code_generator.type import Quad, OperationType
from src.compiler.allocator.types import ValueType

"""
Conditional semantic actions
"""


class LoopActions:
    def __init__(self, quad_list):
        self.loop_jumps = []
        self.quad_list = quad_list

    def save_loop_start(self):
        loop_start = len(self.quad_list)
        self.loop_jumps.append(loop_start)

    def set_loop_condition(self, operand_list):
        boolean_result: Operand = operand_list.pop()
        if boolean_result.type_ is not ValueType.BOOL:
            return CompilerError("Type error: loop expression should be boolean")

        quad = Quad(operation=OperationType.GOTOF, left_address=boolean_result.address)

        self.quad_list.append(quad)
        self.loop_jumps.append(len(self.quad_list) - 1)

    def fill_and_reset_loop(self):
        goto_f_index = self.loop_jumps.pop()
        goto_start_index = self.loop_jumps.pop()

        quad = Quad(operation=OperationType.GOTO, result_address=goto_start_index)

        self.quad_list.append(quad)
        self.quad_list[goto_f_index].result_address = len(self.quad_list)




