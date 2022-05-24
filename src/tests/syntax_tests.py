import unittest
from ..compiler import Compiler
import os
from ..config.definitions import TEST_PROGRAMS_DIR

parser = Compiler()


def test_files(test_case, directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        file = open(filepath)
        data = file.read()
        file.close()

        parser.parse(data)
        test_case.assertIsNone(parser.syntax_error, f'Error trying to parse file {filename}')


class TestSyntax(unittest.TestCase):
    def test_params(self):
        directory = os.path.join(TEST_PROGRAMS_DIR, 'syntax/params')
        test_files(self, directory)

    def test_blocks(self):
        directory = os.path.join(TEST_PROGRAMS_DIR, 'syntax/blocks')
        test_files(self, directory)

    def test_statements(self):
        directory = os.path.join(TEST_PROGRAMS_DIR, 'syntax/statements')
        test_files(self, directory)

    def test_expressions(self):
        directory = os.path.join(TEST_PROGRAMS_DIR, 'syntax/expressions')
        test_files(self, directory)

    def test_variables(self):
        directory = os.path.join(TEST_PROGRAMS_DIR, 'syntax/variables')
        test_files(self, directory)


if __name__ == '__main__':
    unittest.main()
