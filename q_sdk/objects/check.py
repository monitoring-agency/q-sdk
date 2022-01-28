import enum

from objects.base import Base


class Check(Base):
    """Represents a Check

    :param id: ID of the check
    :param name: Name of the check
    :param cmd: Commandline to execute
    :param comment: Associated comment
    """
    def __init__(self, name=None, id=None, cmd=None, comment=None):
        super().__init__()
        self.name = name
        self.id = id
        self.cmd = cmd
        self.comment = comment


class CheckParam(enum.Enum):
    NAME = "name"
    """Name of the check"""
    CMD = "cmd"
    """Commandline of the check"""
    CHECK_TYPE = "check_type"
    """Type of the check"""

