from typing import List
from src.compiler.code_generator.type import Quad, OperationType, Operand
from src.utils.observer import Subscriber, Event, Publisher
from src.compiler.errors import CompilerError, CompilerEvent


class ArrayActions(Publisher):
    def __init__(self, quad_list, operand_stack):
        super().__init__()

        self._operand_stack: List[Operand] = operand_stack
        self._quad_list: List[Quad] = quad_list
        self._dimension_address_stack = []

    def push_dimensions(self, dimensions):
        self._dimension_address_stack += dimensions

    def verify_dimensions(self, scheduler):
        for operand in self._operand_stack:
            print(f'{operand.type_} {operand.address}', end=' ')
        print()

        if len(self._operand_stack) == 0:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Operand stack empty")))
        left_operand = self._operand_stack.pop()

        quad = Quad(
            operation=OperationType.VERIFY,
            left_address=left_operand.address,
            right_address=None,
            result_address=None
        )
        self._quad_list.append(quad)