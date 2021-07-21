import enum

from objects.base import Base


class GlobalVariable(Base):
    def __init__(self, key, value):
        super(GlobalVariable, self).__init__()
        self.key = key
        self.value = value


class GlobalVariableParam(enum.Enum):
    KEY = "key"
    """Key of the variable"""
    VALUE = "value"
    """Value of the variable"""
