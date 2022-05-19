
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

    def check(self, operator, left, right):
        """
        Checks and returns expected type for given parameters.

        :param operator: the operator to apply
        :param left: the left operand type
        :param right: the right operand type
        :return: the resulting type if exists, None otherwise
       """
        result = self._cube[f'{operator}:{left}:{right}']

        return result


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
    ['Bool', 'Bool', 'Bool'],
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


def run_tests(cube):
    tests = [
        ["+", "Int", "Int", "Int"],
        ["+", "Float", "Float", "Float"],
        ["+", "Float", "Int", "Float"],
        ["-", "Int", "Int", "Int"],
        ["-", "Float", "Float", "Float"],
        ["-", "Float", "Int", "Float"],
        ["*", "Int", "Int", "Int"],
        ["*", "Float", "Float", "Float"],
        ["*", "Float", "Int", "Float"],
        ["/", "Int", "Int", "Int"],
        ["/", "Float", "Float", "Float"],
        ["/", "Float", "Int", "Float"],

        ["&&", "Bool", "Bool", "Bool"],
        ["||", "Bool", "Bool", "Bool"],

        ["=", 'Int', 'Float', 'Float'],
        ["=", 'Int', 'Int', 'Int'],
        ["=", 'Float', 'Float', 'Float'],
        ["=", 'Bool', 'Bool', 'Bool'],

        [">", 'Int', 'Float', 'Bool'],
        [">", 'Int', 'Int', 'Bool'],
        [">", 'Float', 'Float', 'Bool'],
        [">", 'Bool', 'Bool', 'Bool'],

        ["<", 'Int', 'Float', 'Bool'],
        ["<", 'Int', 'Int', 'Bool'],
        ["<", 'Float', 'Float', 'Bool'],
        ["<", 'Bool', 'Bool', 'Bool'],

        ["<=", 'Int', 'Float', 'Bool'],
        ["<=", 'Int', 'Int', 'Bool'],
        ["<=", 'Float', 'Float', 'Bool'],
        ["<=", 'Bool', 'Bool', 'Bool'],

        [">=", 'Int', 'Float', 'Bool'],
        [">=", 'Int', 'Int', 'Bool'],
        [">=", 'Float', 'Float', 'Bool'],
        [">=", 'Bool', 'Bool', 'Bool'],

        ["==", 'Int', 'Float', 'Bool'],
        ["==", 'Int', 'Int', 'Bool'],
        ["==", 'Float', 'Float', 'Bool'],
        ["==", 'Bool', 'Bool', 'Bool'],

        ["!=", 'Int', 'Float', 'Bool'],
        ["!=", 'Int', 'Int', 'Bool'],
        ["!=", 'Float', 'Float', 'Bool'],
        ["!=", 'Bool', 'Bool', 'Bool'],
    ]

    errors = 0
    for t in tests:

        value = cube.check(t[0], t[1], t[2])
        if value is None:
            errors += 1
            print("error on test:", t, "expected: ", t[3], ", actual: ", value)
    if errors == 0:
        print("All tests passed")
