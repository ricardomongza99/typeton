from src.compiler import Compiler
import os
from src.config.definitions import PROGRAMS_DIR

FILENAME = 'albert.ty'


def main():
    filename = os.path.join(PROGRAMS_DIR, FILENAME)
    file = open(filename)
    data = file.read()
    file.close()

    compiler = Compiler()
    compiler.compile(data)

    compiler.display_quads()
    compiler.display_tables()
    compiler.display_errors()

    print('Done')


if __name__ == '__main__':
    main()