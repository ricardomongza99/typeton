from semantic import run_tests, Cube
from virtual import run_tests as run_memory
from parser import parser, dir_func
import os


FILENAME = 'sheep.ty'


def main():
    # Get relative path
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../programs/' + FILENAME)

    file = open(filename)
    data = file.read()
    file.close()

    parser.parse(data)
    dir_func.display(debug=True)
    print('Done')


def run_semantic_tests():
    semantic = Cube()
    run_tests(semantic)


if __name__ == '__main__':
    run_semantic_tests()
    run_memory()
    main()
