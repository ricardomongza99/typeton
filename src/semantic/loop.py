from typing import Dict, List

from src.parser.errors import CompilerError
from src.semantic.type import Operand
from src.semantic.quadruple import Quad, OperationType
from src.semantic.type import ActionResult
from src.virtual.compilation import Scheduler
from src.virtual.types import ValueType
from src.semantic.cube import check as semantic_check

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
        return ActionResult()

    def set_loop_condition(self, boolean_result: Operand):
        if boolean_result.type_ is not ValueType.BOOL:
            return ActionResult(error=CompilerError("Type error: loop expression should be boolean"))

        quad = Quad(operation=OperationType.GOTOF, left_address=boolean_result.address)

        self.quad_list.append(quad)
        self.loop_jumps.append(len(self.quad_list) - 1)

        return ActionResult()

    def fill_and_reset_loop(self):
        goto_f_index = self.loop_jumps.pop()
        goto_start_index = self.loop_jumps.pop()

        quad = Quad(operation=OperationType.GOTO, result_address=goto_start_index)

        self.quad_list.append(quad)
        self.quad_list[goto_f_index].result_address = len(self.quad_list)

        return ActionResult()



