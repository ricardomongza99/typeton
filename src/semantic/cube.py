
class Cube:
    def __init__(self):
        self._cube = {}
        # Fill cube
        self._add(arithmetic_symbols, arithmetic_combinations)
        self._add(comparison_symbols, comparison_combinations)
        self._add(comparison_symbols_bool, comparison_combinations_bool)
        self._add(assign_symbol, assign_combinations)
        self._add(boolean_symbols, boolean_combinations)

    def _add(self, operators, combinations):
        """
        Adds combination key to dictionary with its result type

        :param operators: list of operators where the following combinations apply
        :param combinations: list of combinations [left, right, result]
        """
        for operator in operators:
            for left_type, right_type, result_type in combinations:
                self._cube[f'{operator}:{left_type}:{right_type}'] = result_type

    def check(self, operator, left_type, right_type):
        """
        Checks and returns expected type for given parameters.

        :param operator: the operator to apply
        :param left_type: the left operand type
        :param right_type: the right operand type
        :return: the resulting type if exists, None otherwise
       """
        result_type = self._cube.get(f'{operator}:{left_type}:{right_type}')
        return result_type


arithmetic_symbols = ['+', '-', '*', '/']
arithmetic_combinations = [
    ['Int', 'Int', 'Int'],
    ['Float', 'Float', 'Float'],
    ['Int', 'Float', 'Float'],
    ['Float', 'Int', 'Float'],
]

comparison_symbols = ['==', '!=', '<', '<=', '>', '>=']
comparison_combinations = [
    ['Int', 'Int', 'Bool'],
    ['Float', 'Float', 'Bool'],
    ['Int', 'Float', 'Bool'],
    ['Float', 'Int', 'Bool'],
]

comparison_symbols_bool = ['==', '!=']
comparison_combinations_bool = [
    ['Bool', 'Bool', 'Bool']
]

assign_symbol = ['=']
assign_combinations = [
    ['Int', 'Int', 'Int'],
    ['Float', 'Float', 'Float'],
    ['Int', 'Float', 'Float'],
    ['Float', 'Int', 'Float'],
    ['Bool', 'Bool', 'Bool'],
]

boolean_symbols = ['&&', '||']
boolean_combinations = [
    ['Bool', 'Bool', 'Bool']
]
