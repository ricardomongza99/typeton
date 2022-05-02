
class Cube:
    def __init__(self):
        self.__cube = {}
        self.load_types()

    def load_types(self):
        init_cube(self)

    def insert(self, operators, compatible_types):
        for op in operators:
            for options in compatible_types:
                left, right, result = options
                self.__cube[f'{op}:{left}:{right}'] = result
                self.__cube[f'{op}:{right}:{left}'] = result

    def check(self, operator, left, right):
        value = self.__cube[f'{operator}:{left}:{right}']

        if value is not None:
            return True, value

        return False, None


def init_cube(cube):
    cube.insert(["-", "+", "*", "/"], [
        ['int', 'float', 'float'],
        ['int', 'int', 'int'],
        ['float', 'float', 'float']
    ])

    cube.insert([">", ">=", "<", "<=", "==", "!="], [
        ['int', 'float', 'bool'],
        ['int', 'int', 'bool'],
        ['float', 'float', 'bool'],
        ['bool', 'bool', 'bool'],
    ])

    cube.insert(["="], [
        ['int', 'float', 'float'],
        ['int', 'int', 'int'],
        ['float', 'float', 'float'],
        ['bool', 'bool', 'bool'],
    ])

    cube.insert(["&&", "||"], [
        ['bool', 'bool', 'bool'],
    ])


def run_tests(cube):
    tests = [
        ["+", "int", "int", "int"],
        ["+", "float", "float", "float"],
        ["+", "float", "int", "float"],
        ["-", "int", "int", "int"],
        ["-", "float", "float", "float"],
        ["-", "float", "int", "float"],
        ["*", "int", "int", "int"],
        ["*", "float", "float", "float"],
        ["*", "float", "int", "float"],
        ["/", "int", "int", "int"],
        ["/", "float", "float", "float"],
        ["/", "float", "int", "float"],

        ["&&", "bool", "bool", "bool"],
        ["||", "bool", "bool", "bool"],

        ["=", 'int', 'float', 'float'],
        ["=", 'int', 'int', 'int'],
        ["=", 'float', 'float', 'float'],
        ["=", 'bool', 'bool', 'bool'],

        [">", 'int', 'float', 'bool'],
        [">", 'int', 'int', 'bool'],
        [">", 'float', 'float', 'bool'],
        [">", 'bool', 'bool', 'bool'],

        ["<", 'int', 'float', 'bool'],
        ["<", 'int', 'int', 'bool'],
        ["<", 'float', 'float', 'bool'],
        ["<", 'bool', 'bool', 'bool'],

        ["<=", 'int', 'float', 'bool'],
        ["<=", 'int', 'int', 'bool'],
        ["<=", 'float', 'float', 'bool'],
        ["<=", 'bool', 'bool', 'bool'],

        [">=", 'int', 'float', 'bool'],
        [">=", 'int', 'int', 'bool'],
        [">=", 'float', 'float', 'bool'],
        [">=", 'bool', 'bool', 'bool'],

        ["==", 'int', 'float', 'bool'],
        ["==", 'int', 'int', 'bool'],
        ["==", 'float', 'float', 'bool'],
        ["==", 'bool', 'bool', 'bool'],

        ["!=", 'int', 'float', 'bool'],
        ["!=", 'int', 'int', 'bool'],
        ["!=", 'float', 'float', 'bool'],
        ["!=", 'bool', 'bool', 'bool'],

    ]

    errors = 0
    for t in tests:

        is_valid, value = cube.check(t[0], t[1], t[2])
        if not is_valid:
            errors += 1
            print("error on test:", t, "expected: ", t[3], ", actual: ", value)
    if errors == 0:
        print("All tests passed")
