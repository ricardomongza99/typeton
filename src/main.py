from src.compiler import Compiler
from src.virtual_machine import VirtualMachine
import os
import sys
from src.config.definitions import PROGRAMS_DIR

DEFAULT_PROGRAM = 'sort.ty'

def main():
    # Check por program argument
    filename = os.path.join(PROGRAMS_DIR, DEFAULT_PROGRAM)
    if (len(sys.argv)) > 1:
        if sys.argv[1] != '-debug':
            filename = os.path.join(PROGRAMS_DIR, sys.argv[1])

    # Open file with error handling
    try:
        file = open(filename, 'r')
    except OSError:
        print ("Could not find file at: ", filename)
        sys.exit()


    data = file.read()
    file.close()

    # Run Compiler
    compiler = Compiler()
    
    # Check -debug flag
    is_debug = False
    if (len(sys.argv) == 2):
        is_debug = sys.argv[1] == '-debug'
    elif (len(sys.argv) > 2):
        is_debug = sys.argv[2] == '-debug'

    json_data = compiler.compile(data, debug=is_debug)

    # Run Virtual Machine
    virtual_machine = VirtualMachine()
    virtual_machine.run(json_data)


if __name__ == '__main__':
    main()
