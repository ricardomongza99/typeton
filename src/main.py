from semantic import run_tests, Cube
from parser import parser

FILENAME = 'sheep.ty'


def main():
    file = open('../programs/' + FILENAME)
    data = file.read()
    file.close()

    parser.parse(data)
    print('Done')


def run_semantic_tests():
    semantic = Cube()
    run_tests(semantic)


if __name__ == '__main__':
    main()
