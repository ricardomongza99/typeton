import os

""" Gives easy access to frequently used directories """

""" typeton/src """
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

""" typeton/programs """
PROGRAMS_DIR = os.path.join(ROOT_DIR, '../programs')

""" typeton/tests/programs"""
TEST_PROGRAMS_DIR = os.path.join(ROOT_DIR, 'tests/programs')