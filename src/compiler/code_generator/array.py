

from enum import Enum
from typing import List
from src.compiler.code_generator.type import Quad, OperationType, Operand, Dimension
from src.compiler.symbol_table.function_table.variable_table.variable import Variable
from src.utils.observer import Subscriber, Event, Publisher
from src.compiler.errors import CompilerError, CompilerEvent
from src.compiler.stack_allocator.index import StackAllocator
from src.compiler.stack_allocator.types import ValueType
from src.compiler.stack_allocator.helpers import Layers


class ArrayEvents(Enum):
    ADD_TEMP = 0


class ArrayActions(Publisher):
    def __init__(self, quad_list, operand_stack, pointer_types):
        super().__init__()

        self._operand_stack: List[Operand] = operand_stack
        self._quad_list: List[Quad] = quad_list
        self._pointer_types = pointer_types

        self._dimensions_stack: List[Dimension] = []

    def push_dimensions(self, dimensions):
        print("push dimensions")
        self._dimensions_stack.extend(dimensions)

    def initialize_array(self, size, variable: Variable):
        print("initialize array")
        """ Generates quad that initializes array """

        quad = Quad(
            OperationType.POINTER_ASSIGN,
            left_address=OperationType.ALLOCATE_HEAP,
            right_address=size,
            result_address=variable.address_
        )

        self._quad_list.append(quad)

    def verify_dimensions(self):
        print("verify dimensions")
        """ Generates verify quad """
        if not self._operand_stack:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Operand stack empty")))
        left_operand = self._operand_stack[-1]

        if not self._dimensions_stack:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Variable does not have enough dimensions")))

        dimension = self._dimensions_stack[-1]

        quad = Quad(
            operation=OperationType.VERIFY,
            left_address=left_operand.address,
            right_address=None,
            result_address=dimension.size_address
        )
        self._quad_list.append(quad)

    def calculate_dimension(self, stack_allocator: StackAllocator):
        """ Creates quad that multiplies index by m """
        print("calculate dimension")

        if not self._operand_stack:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Operand stack empty")))
        left_operand = self._operand_stack.pop()

        if not self._dimensions_stack:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Variable does not have enough dimensions")))

        dimension = self._dimensions_stack.pop()

        result_address = stack_allocator.allocate_address(ValueType.INT, Layers.TEMPORARY)

        quad = Quad(
            operation=OperationType.MULTIPLY,
            left_address=left_operand.address,
            right_address=dimension.m_address,
            result_address=result_address
        )
        self._quad_list.append(quad)
        self._operand_stack.append(Operand(type_=ValueType.INT, address=result_address))

    def get_array_pointer(self, stack_allocator: StackAllocator):
        print("get array pointer")
        # Error handling: missing indexes for array
        self._dimensions_stack.pop()
        # if self._dimensions_stack:
        #     self.broadcast(Event(CompilerEvent.STOP_COMPILE,
        #                          CompilerError(f"Variable is missing {len(self._dimensions_stack)} dimension")))

        self._generate_sum_quads(stack_allocator)
        self._generate_base_sum_quad(stack_allocator)

    def _generate_sum_quads(self, stack_allocator: StackAllocator):
        print("generate sum quads")
        """ Generates sum quads for calculations indexes * ms """""
        while True:
            if len(self._operand_stack) <= 1:
                self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Operand stack empty")))

            if not stack_allocator.is_segment(self._operand_stack[-2].address, Layers.TEMPORARY):
                break

            left_operand = self._operand_stack.pop()
            right_operand = self._operand_stack.pop()

            result_address = stack_allocator.allocate_address(ValueType.POINTER, Layers.TEMPORARY)
            self._operand_stack.append(Operand(ValueType.POINTER, result_address))

            # Reserve temp int
            self.broadcast(Event(ArrayEvents.ADD_TEMP, (ValueType.POINTER, result_address, None)))

            quad = Quad(
                operation=OperationType.ADD,
                left_address=f'&{left_operand.address}',
                right_address=f'&{right_operand.address}',
                result_address=f'&{result_address}'
            )
            self._quad_list.append(quad)

    def _generate_base_sum_quad(self, stack_allocator: StackAllocator):
        """ Generates last array access quad to pointer. Adds base """

        if len(self._operand_stack) <= 1:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError("Operand stack empty")))

        left_operand = self._operand_stack.pop()
        right_operand = self._operand_stack.pop()

        pointer_address = stack_allocator.allocate_address(ValueType.POINTER, Layers.TEMPORARY)
        self._operand_stack.append(Operand(ValueType.POINTER, pointer_address))

        # Reserve temp pointer
        self.broadcast(Event(ArrayEvents.ADD_TEMP, (ValueType.POINTER, pointer_address, None)))

        self._pointer_types[pointer_address] = right_operand.type_

        quad = Quad(
            operation=OperationType.POINTER_ADD,
            left_address=f'&{right_operand.address}',
            right_address=f'& {left_operand.address}',
            result_address=f'&{pointer_address}'
        )
        self._quad_list.append(quad)
