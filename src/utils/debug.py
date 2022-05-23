class Debug:
    __instance = None
    __id_map = {}
    __no_run = False

    @staticmethod
    def map():
        return Debug.__id_map

    @staticmethod
    def reset():
        Debug.__id_map = {}

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
