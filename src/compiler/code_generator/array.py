from typing import List
from src.compiler.code_generator.type import Quad, OperationType, Operand
from src.utils.observer import Subscriber, Event, Publisher
from src.compiler.errors import CompilerError, CompilerEvent
from src.compiler.stack_allocator.index import StackAllocator
from src.compiler.stack_allocator.types import ValueType
from src.compiler.stack_allocator.helpers import Layers


class ArrayActions(Publisher):
    def __init__(self, quad_list, operand_stack):
        super().__init__()

        self._operand_stack: List[Operand] = operand_stack
        self._quad_list: List[Quad] = quad_list
        self._dimension_address_stack = []

    def push_dimensions(self, addresses):
        self._dimension_address_stack.extend(addresses)

    def verify_dimensions(self):
        if len(self._operand_stack) == 0:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Operand stack empty")))
        left_operand = self._operand_stack[-1]

        if len(self._dimension_address_stack) == 0:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Variable does not have enough dimensions")))
        dimension = self._dimension_address_stack.pop()

        quad = Quad(
            operation=OperationType.VERIFY,
            left_address=left_operand.address,
            right_address=None,
            result_address=dimension
        )
        self._quad_list.append(quad)

    def get_array_pointer(self, stack_allocator: StackAllocator):
        print(self._dimension_address_stack)

        if len(self._operand_stack) <= 1:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Operand stack empty")))
        left_operand = self._operand_stack.pop()
        right_operand = self._operand_stack.pop()

        # TODO: allocate pointer address
        result_address = stack_allocator.allocate_address(ValueType.POINTER, Layers.TEMPORARY)
        #result = scheduler.allocate_address(ValueType.Pointer, Layers.TEMPORARY)

        quad = Quad(
            operation=OperationType.ADD,
            left_address=left_operand.address,
            right_address=right_operand.address,
            result_address=result_address
        )
        self._quad_list.append(quad)
