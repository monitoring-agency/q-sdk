import enum

from objects.base import Base


class MetricTemplate(Base):
    """This class represents a MetricTemplate

    """
    def __init__(
            self, name, id=None, linked_check="", metric_templates=None,
            scheduling_interval="", scheduling_period="", notification_period="", variables=None
    ):
        super().__init__()
        self.name = name
        self.id = id
        self.linked_check = linked_check
        self.metric_templates = metric_templates
        self.scheduling_interval = scheduling_interval
        self.scheduling_period = scheduling_period
        self.notification_period = notification_period
        self.variables = variables


class MetricTemplateParam(enum.Enum):
    NAME = "name"
    """Name of the MetricTemplate"""
    LINKED_CHECK = "linked_check"
    """Linked Check"""
    METRIC_TEMPLATES = "metric_templates"
    """Linked MetricTemplates this MetricTemplates inherits from. Multiple are possible"""
    SCHEDULING_INTERVAL = "scheduling_interval"
    """Scheduling interval, in seconds"""
    SCHEDULING_PERIOD = "scheduling_period"
    """Scheduling period. References to TimePeriod"""
    NOTIFICATION_PERIOD = "notification_period"
    """Notification period. References to TimePeriod"""
    VARIABLES = "variables"
    """Dictionary of variables"""
