
class Cube:
    def __init__(self):
        self._cube = {}
        # Fill cube
        self._add(arithmetic_symbols, arithmetic_combinations)
        self._add(comparison_symbols, comparison_combinations)
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
                self._cube[f'{operator}:{right_type}:{left_type}'] = result_type

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
    ['Int', 'Float', 'Float'],
    ['Int', 'Int', 'Int'],
    ['Float', 'Float', 'Float']
]

comparison_symbols = ['==', '!=', '<', '<=', '>', '>=']
comparison_combinations = [
    ['Int', 'Float', 'Bool'],
    ['Int', 'Int', 'Bool'],
    ['Float', 'Float', 'Bool'],
]

assign_symbol = ['=']
assign_combinations = [
    ['Int', 'Float', 'Float'],
    ['Int', 'Int', 'Int'],
    ['Float', 'Float', 'Float'],
    ['Bool', 'Bool', 'Bool'],
]

boolean_symbols = ['&&', '||']
boolean_combinations = [
    ['Bool', 'Bool', 'Bool']
]

