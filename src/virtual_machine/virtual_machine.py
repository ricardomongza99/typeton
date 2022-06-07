from enum import Enum
from operator import le
import sys
import timeit
from turtle import right
from typing import List, Dict

import jsonpickle
from src.virtual_machine.heap_memory import Heap, RuntimeActions

from src.compiler.stack_allocator.types import ValueType
from src.compiler.code_generator.type import Quad, OperationType
from src.compiler.output import OutputFile
from src.compiler.symbol_table.constant_table import ConstantTable
from src.utils.observer import Event, Subscriber
from src.virtual_machine.types import ContextMemory, FunctionData, pure_address

EXPRESSIONS = {OperationType.ADD, OperationType.DIVIDE,
               OperationType.MULTIPLY, OperationType.SUBTRACT}

POINTER_EXPRESSIONS = {
    OperationType.POINTER_ADD,
    OperationType.DELETE_REF
}

ARRAYS = {
    OperationType.VERIFY,
    OperationType.ARRAY_ADD
}

BOOLEAN_EXPRESSIONS = {
    OperationType.AND,
    OperationType.OR,
    OperationType.LESS_THAN,
    OperationType.LESS_THAN,
    OperationType.EQUAL,
    OperationType.LESS_EQUAL,
    OperationType.GREAT_THAN,
    OperationType.GREAT_EQUAL
}

JUMPS = {
    OperationType.GOTO,
    OperationType.GOTOF,
    OperationType.GOTOV,
}

BUILT_IN = {
    OperationType.PRINT,
    OperationType.INPUT
}

FUNCTIONS = {
    OperationType.PARAM,
    OperationType.ENDFUNC,
    OperationType.ARE,
    OperationType.GOSUB,
    OperationType.RETURN,
    OperationType.CALL_ASSIGN
}


def _execute_typed_multiply(result_type, left_value, right_value):
    if result_type is ValueType.FLOAT:
        return float(left_value) * float(right_value)
    return int(left_value) * int(right_value)


def _execute_typed_subtract(result_type, left_value, right_value):
    if result_type is ValueType.FLOAT:
        return float(left_value) - float(right_value)
    return int(left_value) - int(right_value)


def _execute_typed_add(result_type: ValueType, left_value, right_value):
    if result_type is ValueType.FLOAT:
        return float(left_value) + float(right_value)
    return int(left_value) + int(right_value)


class VirtualMachine(Subscriber):
    def __init__(self):
        super().__init__()
        self._ip = 0  # instruction pointer
        self.operation_count = 0

        self._constant_table: ConstantTable = ConstantTable()
        self._quads: Quad = None
        self._function_data: Dict[str, FunctionData] = {}
        self.pending_return = []
        self.object_heap: Heap = None

        self._memory = {}
        self.context_memory: List[ContextMemory] = []
        self.context_pending_assigment = []
        self.context_jump_locations = []
        self.global_memory = None

    def handle_event(self, event: Event):
        if event.type_ == RuntimeActions.STOP_RUNTIME:
            print()
            print(f'💀 Runtime Error: {event.payload}')
            self._stop()

    def __init_global_function(self):
        size_data = self._function_data["global"].size_data
        self.global_memory = ContextMemory(
            size_data, self._constant_table, None, self.object_heap)
        self.context_memory = []

    def run(self, json_data):

        self._load(json_data)
        self.__init_global_function()
        self.context_memory.append(
            ContextMemory(self._function_data["main"].size_data, self._constant_table, self.global_memory, self.object_heap))

        self._ip = self._function_data['main'].start_quad

        print('🦭🦭🦭typeton🦭🦭🦭')

        start = timeit.default_timer()
        while self._ip < len(self._quads):
            quad = self._quads[self._ip]
            self._execute(quad)
            self.operation_count += 1
        stop = timeit.default_timer()
        print('🦭🦭🦭🦭🦭🦭🦭🦭🦭')
        operations = "{:,}".format(self.operation_count)
        time = '{:.2f}'.format(stop)
        print(f'{operations} operations in {time} seconds')

    # -- LOAD DATA methods ----------------------------

    def _load(self, json_data):
        compiled_program: OutputFile = jsonpickle.decode(
            json_data,
            classes=(FunctionData, Quad, ConstantTable),
            keys=True
        )

        self.object_heap = Heap(compiled_program.heap_start)
        self.object_heap.add_subscriber(self, {})

        # Note: Keys are turned into strings for dictionaries when using JSON decode
        self._constant_table = compiled_program.constant_table
        self._quads = jsonpickle.decode(compiled_program.quad_list)

        # complex objects require additional decoding
        for key, value in compiled_program.function_data.items():
            self._function_data[key] = jsonpickle.decode(value)

    def _execute(self, quad):
        operation = quad.operation

        # quad.display(self._ip)

        if operation in POINTER_EXPRESSIONS:
            self.__pointer_expression(quad)
        elif operation in EXPRESSIONS:
            self.__execute_expression(quad)

        elif operation in ARRAYS:
            self.__execute_array_call(quad)
        elif operation in BOOLEAN_EXPRESSIONS:
            self.__execute_boolean_expression(quad)
        elif operation in JUMPS:
            self.__execute_jump(quad)
        elif operation in FUNCTIONS:
            self.__execute_function_call(quad)
        elif operation in BUILT_IN:
            self.__execute_builtin_function(quad)
        elif operation is OperationType.POINTER_ASSIGN:
            self.__execute_pointer_assign(quad)
            self._ip += 1
        # elif operation is OperationType.POINTER_ASSIGN:
        #     self.__execute_assing(quad.result_address, quad.left_address)
        #     self._ip += 1
        elif operation is OperationType.ASSIGN:
            self.__execute_assign(quad.result_address,
                                  self._get_value(quad.left_address))
            self._ip += 1
        else:
            print(f'Unknown Command {quad.operation}')
            self._ip = len(self._quads) + 1

    # -- EXECUTION methods  ----------------------------

    def _stop(self):
        self._ip = len(self._quads) + 1
        sys.exit()

    def _execute_typed_divide(self, result_type, left_value, right_value):
        if right_value == 0 or left_value == 0:
            self.handle_event(Event(RuntimeActions.STOP_RUNTIME, 'Division by zero'))

        if result_type is ValueType.INT:
            return int(int(left_value) / int(right_value))
        return float(left_value) / float(right_value)

    def __pointer_expression(self, quad):

        if quad.operation is OperationType.DELETE_REF:
            heap_ref = quad.result_address
            self.context_memory[-1].release_reference(heap_ref)

        elif quad.operation is OperationType.POINTER_ADD:
            action_left, p_left = pure_address(quad.left_address)
            action_right, p_right = pure_address(quad.right_address)

            if action_left is not None:
                p_left = self._get_value(quad.left_address)
            if action_right is not None:
                p_right = self._get_value(quad.right_address)

            if p_left is None or p_right is None:
                self.handle_event(Event(RuntimeActions.STOP_RUNTIME, 'NULL pointer exception'))

            result = _execute_typed_add(ValueType.INT, p_left, p_right)
            self.__execute_assign(quad.result_address, result)

        self._ip += 1

    def __execute_expression(self, quad):
        left = self._get_value(quad.left_address)
        right = self._get_value(quad.right_address)
        type_ = self.context_memory[-1].get_type(quad.result_address)
        result = 0

        if quad.operation is OperationType.ADD:
            result = _execute_typed_add(type_, left, right)
        if quad.operation is OperationType.SUBTRACT:
            result = _execute_typed_subtract(type_, left, right)
        elif quad.operation is OperationType.MULTIPLY:
            result = _execute_typed_multiply(type_, left, right)
        elif quad.operation is OperationType.DIVIDE:
            result = self._execute_typed_divide(type_, left, right)

        self._ip += 1
        self.__execute_assign(quad.result_address, result)

    def __execute_array_call(self, quad):
        left = self._get_value(quad.left_address)
        result = self._get_value(quad.result_address)

        if quad.operation == OperationType.VERIFY:
            if not(0 <= left < result):
                self.handle_event(Event(RuntimeActions.STOP_RUNTIME, 'Array Index out of range'))
        elif quad.operation is OperationType.ARRAY_ADD:
            value = _execute_typed_add(ValueType.INT, quad.left_address, self._get_value(quad.right_address))
            action, addr = pure_address(quad.result_address)
            self.context_memory[-1].save_reference(addr, value)

        self._ip += 1

    def __execute_boolean_expression(self, quad):
        left = self._get_value(quad.left_address)
        right = self._get_value(quad.right_address)
        result = 0

        if quad.operation is OperationType.AND:
            result = left and right
        elif quad.operation is OperationType.OR:
            result = left or right
        elif quad.operation is OperationType.EQUAL:
            result = left == right
        elif quad.operation is OperationType.LESS_THAN:
            result = left < right
        elif quad.operation is OperationType.GREAT_THAN:
            result = left > right
        elif quad.operation is OperationType.LESS_EQUAL:
            result = left <= right
        elif quad.operation is OperationType.GREAT_EQUAL:
            result = left >= right

        self._ip += 1
        self.__execute_assign(quad.result_address, result)

    def __execute_builtin_function(self, quad):
        if quad.operation is OperationType.PRINT:
            print(self._get_value(quad.result_address))
        elif quad.operation is OperationType.INPUT:
            result = input()
            type_ = self.context_memory[-1].get_type(quad.result_address)

            if type_ == ValueType.INT:
                result = int(result)
            elif type_ == ValueType.FLOAT:
                result = float(result)

            self.__execute_assign(quad.result_address, result)

        self._ip += 1

    def __execute_jump(self, quad):
        if quad.operation is OperationType.GOTO:
            self._ip = quad.result_address
        elif quad.operation is OperationType.GOTOF:
            if self._get_value(quad.left_address) is False:
                self._ip = quad.result_address
            else:
                self._ip += 1
        elif quad.operation is OperationType.GOTOV:
            if self._get_value(quad.left_address) is True:
                self._ip = quad.result_address
            else:
                self._ip += 1

    def __execute_function_call(self, quad):
        if quad.operation is OperationType.PARAM:
            self._map_argument_to_parameter(
                quad.left_address, quad.right_address)
            self._ip += 1
        elif quad.operation is OperationType.ENDFUNC:
            if len(self.context_jump_locations) == 0:
                self._delete_context_memory()
                self._ip += 1
                print("Main function ended")
                return

            self._ip = self.context_jump_locations.pop()
            self._delete_context_memory()
        elif quad.operation is OperationType.ARE:
            self._assign_context_memory(quad.result_address)
            self._ip += 1
        elif quad.operation is OperationType.GOSUB:
            self.context_memory.append(self.context_pending_assigment.pop())
            self.context_jump_locations.append(self._ip + 1)
            self._ip = self.get_function_start(quad.result_address)
        elif quad.operation is OperationType.RETURN:
            value = self._get_value(quad.result_address)
            self.pending_return.append(value)
            self._ip += 1
        elif quad.operation is OperationType.CALL_ASSIGN:
            return_value = self.pending_return.pop()
            self.context_memory[-1].save(quad.result_address, return_value)
            self._ip += 1

    def __allocate_heap_memory(self, size):
        return self.object_heap.allocate_reference(size)

    def __execute_pointer_assign(self, quad):

        if quad.left_address is OperationType.ALLOCATE_HEAP:
            p_left = self.__allocate_heap_memory(quad.right_address)
        else:
            action_left, p_left = pure_address(quad.left_address)
            if action_left is not None:
                p_left = self._get_value(quad.left_address)

        action_res, _ = pure_address(quad.result_address)
        if action_res is not None:
            self.__execute_object_parameter_assign(quad.result_address, p_left)
            return

        if p_left == -1:
            p_left = None

        self.context_memory[-1].save_reference(quad.result_address, p_left)

    def __execute_object_parameter_assign(self, address, value):
        self.context_memory[-1].save(address, value)

    def __execute_assign(self, address, value):
        # print(f'Assign {address} = {value}')
        self.context_memory[-1].save(address, value)

    def _get_value(self, address):
        if address is not None:
            return self.context_memory[-1].get(address)

    def _set_value(self, value, address):
        """ Sets value to specified address in memory """
        self.context_memory[-1].save(address, value)

    # -- DEBUG methods ---------------------------

    def _map_argument_to_parameter(self, argument_address, parameter_index):
        previous_context = self.context_memory[-1]
        argument_value = previous_context.get(argument_address)

        new_context = self.context_pending_assigment[-1]
        new_context.map_parameter(
            argument_value, argument_address, parameter_index)

    def _assign_context_memory(self, id_):
        size_data = self._function_data[id_].size_data
        ctx = ContextMemory(
            size_data, self._constant_table, self.global_memory, self.object_heap)
        # don't assign until all parameters are calculated using previous era
        self.context_pending_assigment.append(ctx)

    def get_function_start(self, id_):
        return self._function_data[id_].start_quad

    def _delete_context_memory(self):
        self.context_memory.pop()

    # def _map_param_value(self, ):

    def _display_constants(self):
        print('{:5} {:10}'.format('ADDR', 'VALUE'))
        for key, value in self._constant_table.items():
            print('{:<5} {:<10}'.format(key, value))

    def _display_quads(self):
        print('    {:<5} {:<5} {:<5} {:<5}'.format(
            'OP', 'LEFT', 'RIGHT', 'RESULT'))
        for index, quad in enumerate(self._quads):
            quad.display(index)
