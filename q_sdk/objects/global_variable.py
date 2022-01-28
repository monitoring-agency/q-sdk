import enum

from objects.base import Base


class GlobalVariable(Base):
    def __init__(self, key=None, value=None, id=None, comment=None):
        super(GlobalVariable, self).__init__()
        self.id = id
        self.key = key
        self.value = value
        self.comment = comment


class GlobalVariableParam(enum.Enum):
    KEY = "key"
    """Key of the variable"""
    VALUE = "value"
    """Value of the variable"""
