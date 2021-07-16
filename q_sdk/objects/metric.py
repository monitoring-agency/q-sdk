from objects.base import Base


class Metric(Base):
    """This class represents a Metric

    """
    def __init__(
            self, name, disabled, id=None, linked_check="", linked_host="", metric_templates=None,
            scheduling_interval="", scheduling_period="", notification_period="", variables=None
    ):
        super().__init__()
        self.name = name
        self.id = id
        self.linked_check = linked_check
        self.linked_host = linked_host
        self.disabled = disabled
        self.metric_templates = metric_templates
        self.scheduling_interval = scheduling_interval
        self.scheduling_period = scheduling_period
        self.notification_period = notification_period
        self.variables = variables
