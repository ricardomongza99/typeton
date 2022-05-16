from .function import Function
from ..virtual.compilation import Scheduler


class Directory:
    """ A directory of functions """
    def __init__(self):
        self.functions = {}
        self.current_id = 'global'
        self.add('global')
        self.is_function = True

    @property
    def current_function(self) -> Function:
        return self.functions[self.current_id]

    def add(self, id_):
        """ Add Func to `funcs` dictionary if not existent """
        if self.functions.get(id_) is None:
            self.current_id = id_
            self.functions[id_] = Function('Void')

    def add_variable(self, id_):
        """ Add Var to the current function's vars table """
        self.current_function.vars_table.add(id_)

    def will_set_type(self, type_operator):
        """ Prepares for assigning type. Sets `is_func` to true if operator is function related -> """
        self.is_function = type_operator == '->'

    def set_type(self, type_, memory: Scheduler):
        """ Sets corresponding type either to function or to variable"""
        if self.is_function:
            self.current_function.type_ = type_
        else:
            self.current_function.vars_table.set_type(type_, memory)

    def display(self, debug=False):
        """ Displays directory of functions tables """
        print("-" * 20)
        print("DIRECTORY FUNCTIONS")
        print("-" * 20)
        print('{:10} {:10}'.format('ID', 'TYPE'))
        print("-" * 20)
        for id_, func in self.functions.items():
            print('{:10} {:10}'.format(id_, func.type_))
        print("-" * 20)
        print()
        if debug:
            for id_, func in self.functions.items():
                func.vars_table.display(id_)
                print()

