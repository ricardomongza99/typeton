from typing import List, Dict

import jsonpickle

from src.compiler.code_generator.type import Quad, OperationType
from src.compiler.output import OutputFile
from src.compiler.symbol_table.constant_table import ConstantTable
from src.virtual_machine.types import ContextMemory, FunctionData


class VirtualMachine:
    def __init__(self):
        self._ip = 0  # instruction pointer

        self._constant_table: ConstantTable = ConstantTable()
        self._quads = None
        self._function_data: Dict[str, FunctionData] = {}

        self._memory = {}
        self.context_memory: List[ContextMemory] = []
        self.global_memory = None

    def __init_global_function(self):
        size_data = self._function_data["global"].size_data
        self.global_memory = ContextMemory(size_data, self._constant_table, None)
        self.context_memory = []

    def run(self, json_data):

        self._load(json_data)
        self.__init_global_function()
        self.context_memory.append(
            ContextMemory(self._function_data["main"].size_data, self._constant_table, self.global_memory))

        print('🦭🦭🦭typeton🦭🦭🦭')
        while self._ip < len(self._quads):
            quad = self._quads[self._ip]
            self._execute(quad)
        print('🦭🦭🦭🦭🦭🦭🦭🦭🦭')

    # -- LOAD DATA methods ----------------------------

    def _load(self, json_data):
        compiled_program: OutputFile = jsonpickle.decode(
            json_data,
            classes=(FunctionData, Quad, ConstantTable),
            keys=True
        )

        # Note: Keys are turned into strings for dictionaries when using JSON decode
        self._constant_table = compiled_program.constant_table
        self._quads = jsonpickle.decode(compiled_program.quad_list)

        # complex objects require additional decoding
        for key, value in compiled_program.function_data.items():
            self._function_data[key] = jsonpickle.decode(value)

    # -- EXECUTION methods  ----------------------------

    def _execute(self, quad):
        # print(f'{quad.operation.value}\t{quad.left_address}\t{quad.right_address}\t{quad.result_address}')
        operation = quad.operation
        left_address = quad.left_address
        right_address = quad.right_address
        result_address = quad.result_address

        # get values, none if not existent
        left_value = None if left_address is None else self._get_value(left_address)
        right_value = None if right_address is None else self._get_value(right_address)

        result = None
        old_ip = self._ip

        # ARITHMETIC
        if operation is OperationType.ADD:
            result = left_value + right_value
        elif operation is OperationType.SUBTRACT:
            result = left_value - right_value
        elif operation is OperationType.MULTIPLY:
            result = left_value * right_value
        elif operation is OperationType.DIVIDE:
            result = left_value / right_value
        elif operation is OperationType.EQUAL:
            result = left_value == right_value
        elif operation is OperationType.LESS_THAN:
            result = left_value < right_value
        elif operation is OperationType.LESS_EQUAL:
            result = left_value <= right_value
        elif operation is OperationType.GREAT_THAN:
            result = left_value > right_value
        elif operation is OperationType.GREAT_EQUAL:
            result = left_value >= right_value
        elif operation is OperationType.AND:
            result = right_value and left_value
        elif operation is OperationType.OR:
            result = right_value or left_value
        # ASSIGN
        elif operation is OperationType.ASSIGN:
            self._set_value(left_value, result_address)
        # PRINT
        elif operation is OperationType.PRINT:
            print(f'{self.context_memory[-1].get(result_address)}')
        # JUMPS
        elif operation is OperationType.GOTO:
            self._ip = result_address
        elif operation is OperationType.GOTOF:
            if not left_value:
                self._ip = result_address
        elif operation is OperationType.GOTOV:
            if left_value:
                self._ip = result_address

        # if result has a value (ARITHMETIC), set value
        if result is not None:
            self._set_value(result, result_address)

        # if instruction pointer has not changed, go to next instruction
        if old_ip == self._ip:
            self._ip += 1

    # -- MEMORY methods -----------------------

    def _get_value(self, address):
        return self.context_memory[-1].get(address)

    def _set_value(self, value, address):
        """ Sets value to specified address in memory """
        self.context_memory[-1].save(address, value)

    # -- DEBUG methods ---------------------------

    def _display_constants(self):
        print('{:5} {:10}'.format('ADDR', 'VALUE'))
        for key, value in self._constant_table.items():
            print('{:<5} {:<10}'.format(key, value))

    def _display_quads(self):
        print('    {:<5} {:<5} {:<5} {:<5}'.format('OP', 'LEFT', 'RIGHT', 'RESULT'))
        for index, quad in enumerate(self._quads):
            quad.display(index)

# TODO separate  functions (and make static) into a different files
#
# class VirtualMachine:
#     def __init__(self):
#         self.quad_pointer = 0
#         self.memory_allocator = SizeData(0, 0, 0, 0)  # controls limits
#
#         self.quad_list: List[Quad] = []
#         self.function_data_list = []
#         self.global_memory = None
#         self.constant_memory = None
#         self.context_memory_stack: List[ContextMemory] = []
#
#     def load_data(self, json_bytecode):
#         print("hello world")
#         # load_constant_table()
#         # load_quad_list()
#         # load_directory()
#         # load_memory_data()
#
#     def run(self):
#         while self.quad_pointer < len(self.quad_list) - 1:
#             self.execute_quad()
#
#     def execute_quad(self):
#         quad = self.quad_list[self.quad_pointer]
#         self.__execute_sequential_operation(quad)
#
#     def __execute_sequential_operation(self, quad):
#         memory = self.context_memory_stack[-1]
#         left = memory.get(quad.left_address)
#         right = memory.get(quad.right_address)
#         result = 0
#
#         if quad.operation is OperationType.ADD:
#             result = left + right
#         elif quad.operation is OperationType.SUBTRACT:
#             result = left - right
#         elif quad.operation is OperationType.MULTIPLY:
#             result = left * right
#         elif quad.operation is OperationType.DIVIDE:
#             result = left / right
#         else:
#             self.__execute_boolean_expression(quad)
#
#         self.quad_pointer += 1
#         self.__execute__assign(quad.result_address, result)
#
#     def __execute_boolean_expression(self, quad):
#         memory = self.context_memory_stack[-1]
#         left = memory.get(quad.left_address)
#         right = memory.get(quad.right_address)
#         result = 0
#
#         if quad.operation is OperationType.AND:
#             result = left and right
#         elif quad.operation is OperationType.OR:
#             result = left or right
#         elif quad.operation is OperationType.EQUAL:
#             result = left == right
#         elif quad.operation is OperationType.LESS_THAN:
#             result = left < right
#         elif quad.operation is OperationType.GREAT_THAN:
#             result = left > right
#         elif quad.operation is OperationType.LESS_EQUAL:
#             result = left <= right
#         elif quad.operation is OperationType.GREAT_EQUAL:
#             result = left >= right
#         else:
#             self.__execute_builtin_functions(quad)
#
#         self.quad_pointer += 1
#         self.__execute__assign(quad.result_address, result)
#
#     def __execute_builtin_functions(self, quad):
#         memory = self.context_memory_stack[-1]
#
#         if quad.operation is OperationType.PRINT:
#             print(memory.get(quad.result_address))
#         else:
#             self.__execute_conditional_operation(quad)
#
#     def __execute_conditional_operation(self, quad):
#         memory = self.context_memory_stack[-1]
#
#         if quad.operation is OperationType.GOTO:
#             self.quad_pointer = quad.right_address
#         elif quad.operation is OperationType.GOTOF:
#             if memory.get(quad.right_address) is False:
#                 self.quad_pointer = quad.result_address
#         elif quad.operation is OperationType.GOTOV:
#             if memory.get(quad.right_address) is True:
#                 self.quad_pointer = quad.result_address
#         else:
#             self.__execute_function_calls(quad)
#
#     def __execute_function_calls(self, quad):
#         pass
#
#     def __execute__assign(self, address, value):
#         self.context_memory_stack[-1].save(address, value)
