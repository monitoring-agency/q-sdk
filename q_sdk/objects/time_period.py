import enum

from objects.base import Base


class TimePeriod(Base):
    def __init__(self, name, id=None, time_periods=None):
        super(TimePeriod, self).__init__()
        self.name = name
        self.id = id
        self.time_periods = time_periods


class TimePeriodParam(enum.Enum):
    NAME = "name"
    """Name of the TimePeriod"""
    TIME_PERIODS = "time_periods"
    """This value defines the periods. The value should be in the form:
    {
        "Monday": [],
        "Tuesday": [
            {"start_time": "0000", "stop_time": "2400"}
        ],
        "Wednesday": [
            {"start_time": "0800", "stop_time": "1200"},
            {"start_time": "1300", "stop_time": "1700"}
        ],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": []
    }
    
    As you can see, all days have to be in the dict.
    """
