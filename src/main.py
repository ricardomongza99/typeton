from src.semantic.cube import run_tests, Cube
from src.memory.virtual import run_tests as run_memory
from src.parser.parser import Parser
import os


FILENAME = 'sheep.ty'


def main():
    # Get relative path
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../programs/' + FILENAME)

    file = open(filename)
    data = file.read()
    file.close()

    parser = Parser()
    parser.parse(data)
    parser.display_function_directory()

    # parser.parse(data)
    print('Done')


def run_semantic_tests():
    semantic = Cube()
    run_tests(semantic)


if __name__ == '__main__':
    #run_semantic_tests()
    #run_memory()
    main()
