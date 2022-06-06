from multiprocessing import Event
from src.compiler.errors import CompilerError, CompilerEvent
from src.compiler.code_generator.type import Operand
from src.compiler.code_generator.type import Quad, OperationType
from src.compiler.stack_allocator.types import ValueType
from src.utils.observer import Publisher, Subscriber

"""
Conditional semantic actions
"""


class LoopActions(Publisher):
    def __init__(self, quad_list):
        self.loop_jumps = []
        self.quad_list = quad_list

    def save_loop_start(self):
        loop_start = len(self.quad_list)
        self.loop_jumps.append(loop_start)

    def set_loop_condition(self, operand_list):
        boolean_result: Operand = operand_list.pop()
        if boolean_result.type_ is not ValueType.BOOL:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Type Error, if expression should be boolean")))

        quad = Quad(operation=OperationType.GOTOF, left_address=boolean_result.address)

        self.quad_list.append(quad)
        self.loop_jumps.append(len(self.quad_list) - 1)

    def fill_and_reset_loop(self):
        goto_f_index = self.loop_jumps.pop()
        goto_start_index = self.loop_jumps.pop()

        quad = Quad(operation=OperationType.GOTO, result_address=goto_start_index)

        self.quad_list.append(quad)
        self.quad_list[goto_f_index].result_address = len(self.quad_list)
