from typing import List

# NOTE: `type` is a reserved words in python, so
# we use the underscore at the end convention `type_`


class DimData:
    """ Stores dimensions data. Set during declaration of an array """

    def __init__(self, size):
        self.size = size
        self.m = None


class Variable:
    def __init__(self, id_, is_param=False):
        self.id_ = id_
        self.type_ = None
        self.class_id = None
        self.address_ = None
        self.dim_data_list: List[DimData] = []    # stays empty if not array
        self.initialized = False
        self.reference = None
        self.dimensions = []    # stays empty if not array
        self.isReturned = None
        self.is_param = is_param
