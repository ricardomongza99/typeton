

_cube = {}


def check(operator, left_type, right_type):
    """
    Checks and returns expected type for given parameters.

    :param operator: the operator to apply
    :param left_type: the left operand type
    :param right_type: the right operand type
    :return: the resulting type if exists, None otherwise
   """
    result_type = _cube.get(f'{operator}:{left_type}:{right_type}')
    return result_type


def _add(operators, combinations):
    """
    Adds combination key to dictionary with its result type

    :param operators: list of operators where the following combinations apply
    :param combinations: list of combinations [left, right, result]
    """
    for operator in operators:
        for left_type, right_type, result_type in combinations:
            _cube[f'{operator}:{left_type}:{right_type}'] = result_type


_arithmetic_symbols = ['+', '-', '*', '/']
_arithmetic_combinations = [
    ['Int', 'Int', 'Int'],
    ['Float', 'Float', 'Float'],
    ['Int', 'Float', 'Float'],
    ['Float', 'Int', 'Float'],
]

_comparison_symbols = ['==', '!=', '<', '<=', '>', '>=']
_comparison_combinations = [
    ['Int', 'Int', 'Bool'],
    ['Float', 'Float', 'Bool'],
    ['Int', 'Float', 'Bool'],
    ['Float', 'Int', 'Bool'],

]

_comparison_symbols_bool = ['==', '!=']
_comparison_combinations_bool = [
    ['Bool', 'Bool', 'Bool']
]

_assign_symbol = ['=']
_assign_combinations = [
    ['Int', 'Int', 'Int'],
    ['String', 'String', 'String'],
    ['Float', 'Float', 'Float'],
    ['Int', 'Float', 'Float'],
    ['Float', 'Int', 'Float'],
    ['Bool', 'Bool', 'Bool'],
]

_boolean_symbols = ['&&', '||']
_boolean_combinations = [
    ['Bool', 'Bool', 'Bool']
]

# Fill cube
_add(_arithmetic_symbols, _arithmetic_combinations)
_add(_comparison_symbols, _comparison_combinations)
_add(_comparison_symbols_bool, _comparison_combinations_bool)
_add(_assign_symbol, _assign_combinations)
_add(_boolean_symbols, _boolean_combinations)
