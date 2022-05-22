from typing import List

from src.directory.function_table import FunctionTable
from src.semantic.built_in import Builtin_Function_Actions
from src.semantic.conditional import ConditionalActions
from src.semantic.expression import ExpressionActions, Operand, Operator
from src.semantic.loop import LoopActions
from src.semantic.quadruple import Quad
from src.semantic.type import ActionResult
from src.singleton.debug import Debug
from src.utils.display import make_table, TableOptions
from src.virtual.compilation import Scheduler


class QuadGenerator:
    def __init__(self, scheduler: Scheduler, directory: FunctionTable):
        self.__operand_address_stack: List[Operand] = []  # stores the
        # ed virtual address, not actual value
        self.__operator_stack: List[Operator] = []

        self.__quad_list: List[Quad] = []
        self.directory = directory
        self.scheduler = scheduler

        self.conditional_actions = ConditionalActions(self.__quad_list)
        self.loop_actions = LoopActions(self.__quad_list)
        self.expression_actions = ExpressionActions(self.__operand_address_stack, self.__operator_stack)
        self.builtin_actions = Builtin_Function_Actions(self.__quad_list)

    # Expressions -------------------------------------------

    def get_next_quad(self):
        return len(self.__quad_list)

    def push_variable(self, id_):
        result = self.expression_actions.push_variable(id_, self.directory)
        return self.__handle_result(result)

    def push_operator(self, operator):
        results = self.expression_actions.push_operator(operator, self.scheduler)
        return self.__handle_result(results)

    def execute_if_possible(self, priority):
        result = self.expression_actions.execute_if_possible(priority, self.scheduler)
        return self.__handle_result(result)

    def push_constant(self, value, constant_table):
        result = self.expression_actions.push_constant(value, constant_table)
        return self.__handle_result(result)

    def execute_remaining(self):
        results = self.expression_actions.execute_remaining(self.scheduler)
        return self.__handle_result(results)

    # -------------------------------------------------------

    # Conditionals -------------------------------------------

    def fill_end_single(self):
        self.conditional_actions.fill_end_single()

    def get_conditional(self):
        result = self.conditional_actions.get_conditional(self.expression_actions.get_operands())
        self.__handle_result(result)

    def fill_and_goto(self):
        result = self.conditional_actions.fill_and_goto()
        self.__handle_result(result)

    def fill_end(self):
        self.conditional_actions.fill_end()

    # -------------------------------------------------------

    # Loop -------------------------------------------

    def save_loop_start(self):
        self.__handle_result(self.loop_actions.save_loop_start())

    def set_loop_condition(self):
        self.__handle_result(self.loop_actions.set_loop_condition(self.expression_actions.get_operands().pop()))

    def fill_and_reset_loop(self):
        self.__handle_result(self.loop_actions.fill_and_reset_loop())

    # -------------------------------------------------------

    # Helpers

    def __handle_result(self, results):
        if type(results) is ActionResult:
            if results.has_quad():
                self.__push_quad(results.quad)
            return results.error

        errors = []
        for result in results:
            if result.has_quad():
                self.__push_quad(result.quad)
            elif result.has_error():
                errors.append(result.error)
        return errors

    def display(self):
        address_map = Debug.get_map()
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
