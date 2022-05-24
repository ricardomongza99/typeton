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
    json_data = compiler.compile(data, debug=True)

    print("Will execute this")
    print(json_data)

    print('Done')


if __name__ == '__main__':
    main()