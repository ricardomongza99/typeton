import os

""" Gives easy access to frequently used directories """

""" typeton/src """
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

""" typeton/programs """
PROGRAMS_DIR = os.path.join(ROOT_DIR, '../programs')

""" typeton/tests/programs"""
TEST_PROGRAMS_DIR = os.path.join(ROOT_DIR, 'tests/programs')

""" Memory allocation spaces """
INT_RANGE_SIZE = 499
FLOAT_RANGE_SIZE = 499
BOOL_RANGE_SIZE = 499
STRING_RANGE_SIZE = 499
POINTER_RANGE_SIZE = 499
HEAP_RANGE_SIZE = 10000
