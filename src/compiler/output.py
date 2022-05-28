from typing import List, Dict

from src.compiler.code_generator.type import Quad
from src.compiler.symbol_table.constant_table import ConstantTable
from src.virtual_machine.types import FunctionData


class OutputFile:
    def __init__(self, constant_table, function_data, quad_list):
        self.constant_table: ConstantTable = constant_table
        self.function_data: Dict[str, FunctionData] = function_data
        self.quad_list: List[Quad] = quad_list
