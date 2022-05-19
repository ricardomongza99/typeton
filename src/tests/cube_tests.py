import unittest
from ..semantic import Cube


cube = Cube()


class TestCube(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(cube.check('+', 'Int', 'Int'), 'Int')
        self.assertEqual(cube.check('+', 'Float', 'Float'), 'Float')
        self.assertEqual(cube.check('+', 'Int', 'Float'), 'Float')
        self.assertEqual(cube.check('+', 'Float', 'Int'), 'Float')
        self.assertEqual(cube.check('-', 'Int', 'Int'), 'Int')
        self.assertEqual(cube.check('-', 'Float', 'Float'), 'Float')
        self.assertEqual(cube.check('-', 'Int', 'Float'), 'Float')
        self.assertEqual(cube.check('-', 'Float', 'Int'), 'Float')
        self.assertEqual(cube.check('*', 'Int', 'Int'), 'Int')
        self.assertEqual(cube.check('*', 'Float', 'Float'), 'Float')
        self.assertEqual(cube.check('*', 'Int', 'Float'), 'Float')
        self.assertEqual(cube.check('*', 'Float', 'Int'), 'Float')
        self.assertEqual(cube.check('/', 'Int', 'Int'), 'Int')
        self.assertEqual(cube.check('/', 'Float', 'Float'), 'Float')
        self.assertEqual(cube.check('/', 'Int', 'Float'), 'Float')
        self.assertEqual(cube.check('/', 'Float', 'Int'), 'Float')

    def test_boolean(self):
        self.assertEqual(cube.check('&&', 'Bool', 'Bool'), 'Bool')
        self.assertEqual(cube.check('||', 'Bool', 'Bool'), 'Bool')

    def test_assign(self):
        self.assertEqual(cube.check('=', 'Int', 'Float'), 'Float')
        self.assertEqual(cube.check('=', 'Float', 'Int'), 'Float')
        self.assertEqual(cube.check('=', 'Int', 'Int'), 'Int')
        self.assertEqual(cube.check('=', 'Float', 'Float'), 'Float')
        self.assertEqual(cube.check('=', 'Bool', 'Bool'), 'Bool')

    def test_comparison(self):
        self.assertEqual(cube.check('>', 'Int', 'Int'), 'Bool')
        self.assertEqual(cube.check('>', 'Float', 'Float'), 'Bool')
        self.assertEqual(cube.check('>', 'Int', 'Float'), 'Bool')
        self.assertEqual(cube.check('>=', 'Int', 'Int'), 'Bool')
        self.assertEqual(cube.check('>=', 'Float', 'Float'), 'Bool')
        self.assertEqual(cube.check('>=', 'Int', 'Float'), 'Bool')
        self.assertEqual(cube.check('<', 'Int', 'Int'), 'Bool')
        self.assertEqual(cube.check('<', 'Float', 'Float'), 'Bool')
        self.assertEqual(cube.check('<', 'Int', 'Float'), 'Bool')
        self.assertEqual(cube.check('<=', 'Int', 'Int'), 'Bool')
        self.assertEqual(cube.check('<=', 'Float', 'Float'), 'Bool')
        self.assertEqual(cube.check('<=', 'Int', 'Float'), 'Bool')
        self.assertEqual(cube.check('==', 'Int', 'Int'), 'Bool')
        self.assertEqual(cube.check('==', 'Float', 'Float'), 'Bool')
        self.assertEqual(cube.check('==', 'Int', 'Float'), 'Bool')
        self.assertEqual(cube.check('!=', 'Int', 'Int'), 'Bool')
        self.assertEqual(cube.check('!=', 'Float', 'Float'), 'Bool')
        self.assertEqual(cube.check('!=', 'Int', 'Float'), 'Bool')
        self.assertEqual(cube.check('==', 'Bool', 'Bool'), 'Bool')
        self.assertEqual(cube.check('!=', 'Bool', 'Bool'), 'Bool')

    def test_illegal(self):
        self.assertIsNone(cube.check('+', 'Int', 'Bool'))
        self.assertIsNone(cube.check('+', 'Float', 'Bool'))
        self.assertIsNone(cube.check('*', 'Bool', 'Bool'))
        self.assertIsNone(cube.check('&&', 'Int', 'Bool'))
        self.assertIsNone(cube.check('&&', 'Float', 'Int'))
        self.assertIsNone(cube.check('=', 'Bool', 'Int'))
        self.assertIsNone(cube.check('<', 'Bool', 'Bool'))
        self.assertIsNone(cube.check('<', 'Bool', 'Int'))
        self.assertIsNone(cube.check('a', 'a', 'a'))


if __name__ == '__main__':
    unittest.main()
