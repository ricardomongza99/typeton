import unittest


class TestCube(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(cube.type_check('+', 'Int', 'Int'), 'Int')
        self.assertEqual(cube.type_check('+', 'Float', 'Float'), 'Float')
        self.assertEqual(cube.type_check('+', 'Int', 'Float'), 'Float')
        self.assertEqual(cube.type_check('+', 'Float', 'Int'), 'Float')
        self.assertEqual(cube.type_check('-', 'Int', 'Int'), 'Int')
        self.assertEqual(cube.type_check('-', 'Float', 'Float'), 'Float')
        self.assertEqual(cube.type_check('-', 'Int', 'Float'), 'Float')
        self.assertEqual(cube.type_check('-', 'Float', 'Int'), 'Float')
        self.assertEqual(cube.type_check('*', 'Int', 'Int'), 'Int')
        self.assertEqual(cube.type_check('*', 'Float', 'Float'), 'Float')
        self.assertEqual(cube.type_check('*', 'Int', 'Float'), 'Float')
        self.assertEqual(cube.type_check('*', 'Float', 'Int'), 'Float')
        self.assertEqual(cube.type_check('/', 'Int', 'Int'), 'Int')
        self.assertEqual(cube.type_check('/', 'Float', 'Float'), 'Float')
        self.assertEqual(cube.type_check('/', 'Int', 'Float'), 'Float')
        self.assertEqual(cube.type_check('/', 'Float', 'Int'), 'Float')

    def test_boolean(self):
        self.assertEqual(cube.type_check('&&', 'Bool', 'Bool'), 'Bool')
        self.assertEqual(cube.type_check('||', 'Bool', 'Bool'), 'Bool')

    def test_assign(self):
        self.assertEqual(cube.type_check('=', 'Int', 'Float'), 'Float')
        self.assertEqual(cube.type_check('=', 'Float', 'Int'), 'Float')
        self.assertEqual(cube.type_check('=', 'Int', 'Int'), 'Int')
        self.assertEqual(cube.type_check('=', 'Float', 'Float'), 'Float')
        self.assertEqual(cube.type_check('=', 'Bool', 'Bool'), 'Bool')

    def test_comparison(self):
        self.assertEqual(cube.type_check('>', 'Int', 'Int'), 'Bool')
        self.assertEqual(cube.type_check('>', 'Float', 'Float'), 'Bool')
        self.assertEqual(cube.type_check('>', 'Int', 'Float'), 'Bool')
        self.assertEqual(cube.type_check('>=', 'Int', 'Int'), 'Bool')
        self.assertEqual(cube.type_check('>=', 'Float', 'Float'), 'Bool')
        self.assertEqual(cube.type_check('>=', 'Int', 'Float'), 'Bool')
        self.assertEqual(cube.type_check('<', 'Int', 'Int'), 'Bool')
        self.assertEqual(cube.type_check('<', 'Float', 'Float'), 'Bool')
        self.assertEqual(cube.type_check('<', 'Int', 'Float'), 'Bool')
        self.assertEqual(cube.type_check('<=', 'Int', 'Int'), 'Bool')
        self.assertEqual(cube.type_check('<=', 'Float', 'Float'), 'Bool')
        self.assertEqual(cube.type_check('<=', 'Int', 'Float'), 'Bool')
        self.assertEqual(cube.type_check('==', 'Int', 'Int'), 'Bool')
        self.assertEqual(cube.type_check('==', 'Float', 'Float'), 'Bool')
        self.assertEqual(cube.type_check('==', 'Int', 'Float'), 'Bool')
        self.assertEqual(cube.type_check('!=', 'Int', 'Int'), 'Bool')
        self.assertEqual(cube.type_check('!=', 'Float', 'Float'), 'Bool')
        self.assertEqual(cube.type_check('!=', 'Int', 'Float'), 'Bool')
        self.assertEqual(cube.type_check('==', 'Bool', 'Bool'), 'Bool')
        self.assertEqual(cube.type_check('!=', 'Bool', 'Bool'), 'Bool')

    def test_illegal(self):
        self.assertIsNone(cube.type_check('+', 'Int', 'Bool'))
        self.assertIsNone(cube.type_check('+', 'Float', 'Bool'))
        self.assertIsNone(cube.type_check('*', 'Bool', 'Bool'))
        self.assertIsNone(cube.type_check('&&', 'Int', 'Bool'))
        self.assertIsNone(cube.type_check('&&', 'Float', 'Int'))
        self.assertIsNone(cube.type_check('=', 'Bool', 'Int'))
        self.assertIsNone(cube.type_check('<', 'Bool', 'Bool'))
        self.assertIsNone(cube.type_check('<', 'Bool', 'Int'))
        self.assertIsNone(cube.type_check('a', 'a', 'a'))


if __name__ == '__main__':
    unittest.main()
