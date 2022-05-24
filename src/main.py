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

    parser.quadGenerator.display()
    parser.print_compiler_errors()
    parser.constant_table.display()
    parser.directory.display(debug=True)

    print('Done')


if __name__ == '__main__':
    main()