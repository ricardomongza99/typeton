from typing import Dict


class Debug:
    __instance = None
    __id_map = {}
    __compiler_errors = []
    __debug_actions = []
    __no_run = False

    @staticmethod
    def get_map():
        return Debug.__id_map

    @staticmethod
    def get_errors():
        return Debug.__compiler_errors


    @staticmethod
    def add_action(action):
        Debug.__debug_actions.append(action)

    @staticmethod
    def add_error(error):
        Debug.__compiler_errors.append(error)

    @staticmethod
    def set_no_run(toggle):
        Debug.__no_run = toggle

    @staticmethod
    def no_run():
        return Debug.__no_run

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Debug.__instance is None:
            Debug()
        return Debug.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Debug.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Debug.__instance = self
