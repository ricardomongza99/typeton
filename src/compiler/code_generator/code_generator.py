from typing import List

import jsonpickle

from src.compiler.allocator.allocator import Allocator
from src.compiler.code_generator.built_in import Builtin_Function_Actions
from src.compiler.code_generator.conditional import ConditionalActions
from src.compiler.code_generator.expression import Operand, Operator, ExpressionActions
from src.compiler.code_generator.function import FunctionActions
from src.compiler.code_generator.loop import LoopActions
from src.compiler.code_generator.type import Quad
from src.utils.debug import Debug
from src.utils.display import make_table, TableOptions


class CodeGenerator:
    def __init__(self, scheduler: Allocator):
        self.__operand_address_stack: List[Operand] = []
        self.__operator_stack: List[Operator] = []
        self.__quad_list: List[Quad] = []

        self.scheduler = scheduler

        self.conditional_actions = ConditionalActions(self.__quad_list)
        self.function_actions = FunctionActions(self.__quad_list)
        self.loop_actions = LoopActions(self.__quad_list)
        self.builtin_actions = Builtin_Function_Actions(self.__quad_list)

        self.expression_actions = ExpressionActions(self.__quad_list,
                                                    self.__operand_address_stack,
                                                    self.__operator_stack)

    # Expressions -------------------------------------------

    def print_operand_stack(self):
        a = Debug.map()
        r = "Operands: "
        for operand in self.__operand_address_stack:
            r += a[operand.address] + " "
        print(r)
        print()

    def print_operator_stack(self):
        r = "Operators: "
        for operator in self.__operator_stack:
            r += operator.type_.value + " "
        print(r)

    def get_next_quad(self):
        return len(self.__quad_list)

    def push_variable(self, id_, type_, address):
        self.expression_actions.push_variable(id_, type_, address)

    def push_operator(self, operator):
        self.expression_actions.push_operator(operator, self.scheduler)

    def execute_if_possible(self, priority):
        self.expression_actions.execute_if_possible(priority, self.scheduler)

    def push_constant(self, value, constant_table):
        self.expression_actions.push_constant(value, constant_table)

    def execute_remaining(self):
        self.expression_actions.execute_remaining(self.scheduler)

    # -------------------------------------------------------

    # Conditionals -------------------------------------------

    def fill_end_single(self):
        return self.conditional_actions.fill_end_single()

    def get_conditional(self):
        return self.conditional_actions.get_conditional(self.__operand_address_stack)

    def fill_and_goto(self):
        return self.conditional_actions.fill_and_goto()

    def fill_end(self):
        self.conditional_actions.fill_end()

    # -------------------------------------------------------

    # Loop -------------------------------------------

    def save_loop_start(self):
        self.loop_actions.save_loop_start()

    def set_loop_condition(self):
        self.loop_actions.set_loop_condition(self.__operand_address_stack)

    def fill_and_reset_loop(self):
        return self.loop_actions.fill_and_reset_loop()

    # -------------------------------------------------------

    # Helpers

    def display(self):
        address_map = Debug.map()
        table = make_table("Quadruples",
                           ["#", "Operator", "Left", "Right", "Result"],
                           map(lambda quad:
                               [
                                   '{:^10}'.format(quad[0]),
                                   '{:^10}'.format(quad[1].operation.value),
                                   '{:<5} -->{:>5}'.format(address_map[quad[1].left_address], quad[1].left_address)
                                   if address_map.get(quad[1].left_address) is not None else "." * 8,
                                   '{:<5} --> {:<5}'.format(address_map[quad[1].right_address], quad[1].right_address)
                                   if address_map.get(quad[1].right_address) is not None else "." * 15,
                                   '{:<5} -->{:>5}'.format(address_map[quad[1].result_address], quad[1].result_address)
                                   if address_map.get(quad[1].result_address) is not None else quad[1].result_address

                               ], enumerate(self.__quad_list)),
                           options=TableOptions(20, 20)
                           )
        print(table)

    def __push_quad(self, quad: Quad):
        self.__quad_list.append(quad)

    def execute_builtin_call(self):
        self.builtin_actions.execute_call(self.__operator_stack, self.__operand_address_stack)

    def get_output_quads(self):
        """ Returns quads list of types [str, str, str, str] used by the output file """

        return jsonpickle.encode(self.__quad_list)
