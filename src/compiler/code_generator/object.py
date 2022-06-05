from typing import List
from unittest import result
from weakref import ref
from src.compiler.code_generator.expression import ExpressionActions, ExpressionEvents
from src.compiler.code_generator.type import Operand, OperationType, Quad
from src.compiler.errors import CompilerError, CompilerEvent

from src.compiler.heap_allocator.index import HeapAllocator
from src.compiler.stack_allocator.helpers import Layers
from src.compiler.stack_allocator.index import StackAllocator
from src.compiler.stack_allocator.types import ValueType
from src.compiler.symbol_table.class_table import Class
from src.compiler.symbol_table.function_table.variable_table.variable import Variable
from src.utils.observer import Publisher, Event

"""
Conditional semantic actions
"""


class ObjectActions(Publisher):
    def __init__(self, quad_list, operand_list, heap_allocator: HeapAllocator, stack_allocator: StackAllocator, pointer_types):
        super().__init__()
        self.pointer_types = pointer_types
        self.class_stack: List[Class] = []
        self.variable_stack: List[Variable] = []
        self.object_property_stack = []
        self.object_address_stack = []
        self.operand_list = operand_list
        self.quad_list = quad_list
        self.stack_allocator = stack_allocator
        self.heap_allocator = heap_allocator

    # def push_variable(self, var):

    def free_heap_memory(self, variable: Variable):

        if variable.class_id is None:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError(
                f'{variable.id_} is not a freeable variable')))

        if variable.initialized is False:
            self.broadcast(CompilerEvent.STOP_COMPILE, CompilerError(
                f'object {variable.id_} has not been initialized'))

        end = self.heap_allocator.free_reference(variable.reference)
        q = Quad(OperationType.POINTER_ASSIGN, -1, end, variable.address_)
        self.quad_list.append(q)

    def push_variable(self, variable: Variable):
        self.variable_stack.append(variable)

    def push_object_property(self, property_name):
        self.object_property_stack.append(property_name)

    def push_object_address(self, address):
        self.object_address_stack.append(address)

    def resolve_object_assignment(self):
        class_data = self.class_stack.pop()
        object_address = self.object_address_stack.pop()
        property_name = self.object_property_stack.pop()

        if property_name not in class_data.variables:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError(
                f'{property_name} not found in Class {class_data.id_}')))

        property_data = class_data.variables[property_name]

        property_pointer = self.stack_allocator.allocate_address(
            ValueType.POINTER, Layers.TEMPORARY)
        self.broadcast(Event(ExpressionEvents.ADD_TEMP,
                       (ValueType.POINTER, property_pointer, property_data.class_id)))

        print("adding property pointer", property_pointer)

        quad = Quad(OperationType.POINTER_ADD, left_address=f'&{object_address}',
                    right_address=property_data.offset, result_address=f'&{property_pointer}')

        self.quad_list.append(quad)
        self.operand_list.append(
            Operand(ValueType.POINTER, property_pointer, class_id=class_data.id_, is_class_param=True))

        self.pointer_types[property_pointer] = property_data.type_
        if property_data.class_id is not None:
            self.pointer_types[property_pointer] = property_data.class_id

    def get_object_property(self):

        class_data = self.class_stack.pop()
        object_address = self.object_address_stack.pop()
        property_name = self.object_property_stack.pop()

        if property_name not in class_data.variables:
            self.broadcast(CompilerEvent.STOP_COMPILE, CompilerError(
                f'{property_name} not found in Class {class_data.id_}'))

        property_data = class_data.variables[property_name]

        temp = self.stack_allocator.allocate_address(
            property_data.type_, Layers.TEMPORARY)
        self.broadcast(Event(ExpressionEvents.ADD_TEMP,
                             (property_data.type_, temp, property_data.class_id)))

        print("adding get object temp", temp, property_data.type_)

        property_pointer = self.stack_allocator.allocate_address(
            ValueType.POINTER, Layers.TEMPORARY)
        self.broadcast(Event(ExpressionEvents.ADD_TEMP,
                       (ValueType.POINTER, property_pointer, property_data.class_id)))

        quad = Quad(OperationType.POINTER_ADD, left_address=f'&{object_address}',
                    right_address=property_data.offset, result_address=f'&{property_pointer}')

        self.quad_list.append(quad)

        if property_data.type_ == ValueType.POINTER:
            quad = Quad(OperationType.ASSIGN,
                        left_address=f'*{property_pointer}', result_address=f'&{temp}')
            self.pointer_types[temp] = property_data.class_id

        else:
            quad = Quad(OperationType.ASSIGN,
                        left_address=f'*{property_pointer}', result_address=temp)

        self.quad_list.append(quad)
        self.operand_list.append(
            Operand(property_data.type_, temp, is_class_param=True))

        # self.pointer_types[]

    def allocate_heap(self):
        object: Class = self.class_stack.pop()
        variable: Class = self.class_stack.pop()

        var: Variable = self.variable_stack.pop()
        var.initialized = True

        if variable.id_ != object.id_:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError(
                f'variable {variable.id_} cannot be assigned Class type of {object.id_}')))

        reference = self.heap_allocator.allocate_reference(variable.size)
        operand: Operand = self.operand_list.pop()
        var.reference = reference
        print(var.id_, "var.id_ is None")

        if var.id_ is None:
            operand.address = f'*{operand.address}'

        quad = Quad(OperationType.POINTER_ASSIGN, left_address=reference,
                    result_address=operand.address)

        self.quad_list.append(quad)
        self.pointer_types[operand.address] = var.class_id

    def push_class_data(self, class_data: Class):
        self.class_stack.append(class_data)
