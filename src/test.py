from parser import parser
import glob


def run_test(filename):
    print("Parsing code")

    file = open(filename)
    s = file.read()
    file.close()

    parser.parse(s)
    print('Parsed Successfully')


def run_tests():
    test_files = glob.glob("./tests/*/*.ld")
    print("Running all tests")

    for fileName in test_files:
        run_test(fileName)


if __name__ == "__main__":
    run_tests()
