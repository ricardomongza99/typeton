from src.compiler import Compiler
import os
from src.config.definitions import PROGRAMS_DIR

FILENAME = 'albert.ty'


def main():
    filename = os.path.join(PROGRAMS_DIR, FILENAME)
    file = open(filename)
    data = file.read()
    file.close()

    parser = Compiler()
    parser.parse(data)

    parser.code_generator.display()
    parser.print_compiler_errors()
    parser.display_tables()

    print('Done')


if __name__ == '__main__':
    main()