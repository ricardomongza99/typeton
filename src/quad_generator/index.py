from typing import List

from src.allocator.allocator import Allocator
from src.directory.function_table import FunctionTable
from src.quad_generator.built_in import Builtin_Function_Actions
from src.quad_generator.conditional import ConditionalActions
from src.quad_generator.expression import ExpressionActions, Operand, Operator
from src.quad_generator.loop import LoopActions
from src.quad_generator.type import Quad
from src.utils.debug import Debug
from src.utils.display import make_table, TableOptions


class QuadGenerator:
    def __init__(self, scheduler: Allocator, directory: FunctionTable):
        self.__operand_address_stack: List[Operand] = []
        self.__operator_stack: List[Operator] = []
        self.__quad_list: List[Quad] = []

        # TODO rename to function directory
        self.directory = directory
        self.scheduler = scheduler

        self.conditional_actions = ConditionalActions(self.__quad_list)
        self.loop_actions = LoopActions(self.__quad_list)
        self.expression_actions = ExpressionActions(self.__quad_list,
                                                    self.__operand_address_stack,
                                                    self.__operator_stack)

        self.builtin_actions = Builtin_Function_Actions(self.__quad_list)

    # Expressions -------------------------------------------

    def get_next_quad(self):
        return len(self.__quad_list)

    def push_variable(self, id_):
        return self.expression_actions.push_variable(id_, self.directory)

    def push_operator(self, operator):
        return self.expression_actions.push_operator(operator, self.scheduler)

    def execute_if_possible(self, priority):
        return self.expression_actions.execute_if_possible(priority, self.scheduler)

    def push_constant(self, value, constant_table):
        return self.expression_actions.push_constant(value, constant_table)

    def execute_remaining(self):
        return self.expression_actions.execute_remaining(self.scheduler)

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
