import json
from src.compiler.code_generator.type import Quad, OperationType


class VirtualMachine:
    def __init__(self):
        self._ip = 0    # instruction pointer

        self._constant_table = None
        self._quads = None
        self._function_data = None

        self._memory = {}

    def run(self, json_data):
        self._load(json_data)

        print('🦭🦭🦭typeton🦭🦭🦭')
        while self._ip < len(self._quads):
            quad = self._quads[self._ip]
            self._execute(quad)
        print('🦭🦭🦭🦭🦭🦭🦭🦭🦭')

    # -- LOAD DATA methods ----------------------------

    def _load(self, json_data):
        data = json.loads(json_data)

        self._constant_table = self._get_constant_table(data)
        self._quads = self._get_quads(data)
        self._function_data = data['function_data']

    @staticmethod
    def _get_constant_table(data):
        constant_table = {}
        for key, value in data['constant_table'].items():
            constant_table[int(key)] = value
        return constant_table

    @staticmethod
    def _get_quads(data):
        quads = []
        for quad in data['quads']:
            operation = OperationType(quad[0])
            left_address = int(quad[1]) if quad[1] else None
            right_address = int(quad[2]) if quad[2] else None
            result_address = int(quad[3])

            quads.append(Quad(operation, left_address, right_address, result_address))
        return quads

    # -- EXECUTION methods  ----------------------------

    def _execute(self, quad):
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
            result = right_value >= right_value
        elif operation is OperationType.AND:
            result = right_value and left_value
        elif operation is OperationType.OR:
            result = right_value or left_value
        # ASSIGN
        elif operation is OperationType.ASSIGN:
            self._set_value(left_value, result_address)
        # PRINT
        elif operation is OperationType.PRINT:
            print(f'{self._memory[result_address]}')
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
        """ Gets value at specified address from either memory or constant table (depending of range) """
        # TODO: get constant ranges, not hard-coded
        if 0 <= address < 6000:
            # is global, local or temp
            return self._memory[address]
        elif 6000 <= address < 8000:
            # is constant
            return self._constant_table[address]

    def _set_value(self, value, address):
        """ Sets value to specified address in memory """
        if 0 <= address < 6000:
            # is global, local or temp
            self._memory[address] = value

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
