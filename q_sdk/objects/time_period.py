from objects.base import Base


class TimePeriod(Base):
    def __init__(self, name, id=None, time_periods=None):
        super(TimePeriod, self).__init__()
        self.name = name
        self.id = id
        self.time_periods = time_periods
