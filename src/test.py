from src.parser.parser import parser
from lexer import lexer
import glob


def run_test(filename):
    print("Parsing code for test @ " + filename)

    file = open(filename)
    s = file.read()
    file.close()

    parser.parse(s)
    lexer.lineno = 1



    print('\n')


def run_tests():
    test_files = glob.glob("./tests/*/*.ty")
    print("Running all tests")

    for fileName in test_files:
        run_test(fileName)


if __name__ == "__main__":
    run_tests()
