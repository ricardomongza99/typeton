from src.parser import Parser
import os
from config.definitions import PROGRAMS_DIR
from src.singleton.debug import Debug

FILENAME = 'albert.ty'


def main():
    filename = os.path.join(PROGRAMS_DIR, FILENAME)
    file = open(filename)
    data = file.read()
    file.close()

    parser = Parser()
    parser.parse(data)

    parser.quadGenerator.display()
    parser.print_compiler_errors()
    # parser.constant_table.display()
    # parser.directory.display(debug=True)


    # parser.parse(data)
    print('Done')


if __name__ == '__main__':
    main()