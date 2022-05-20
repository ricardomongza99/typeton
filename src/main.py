from src.parser import Parser
import os

FILENAME = 'albert.ty'


def main():
    # Get relative path
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../programs/' + FILENAME)

    file = open(filename)
    data = file.read()
    file.close()

    parser = Parser()
    parser.parse(data)

    parser.quadGenerator.display()
    # parser.constant_table.display()
    # parser.directory.display(debug=True)
    parser.print_compiler_errors()

    # parser.parse(data)
    print('Done')


if __name__ == '__main__':
    main()



