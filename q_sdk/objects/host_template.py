import enum

from objects.base import Base


class HostTemplate(Base):
    def __init__(self, name, address="", linked_check=None, host_templates=None, scheduling_interval="",
                 scheduling_period=None, notification_period=None, variables=None):
        super(HostTemplate, self).__init__()
        self.name = name
        self.address = address
        self.linked_check = linked_check
        self.host_templates = host_templates
        self.scheduling_interval = scheduling_interval
        self.scheduling_period = scheduling_period
        self.notification_period = notification_period
        self.variables = variables


class HostTemplateParam(enum.Enum):
    NAME = "name"
    """Name of a HostTemplate"""
    ADDRESS = "address"
    """Address of a HostTemplate"""
    LINKED_CHECK = "linked_check"
    """Check linked to a HostTemplate"""
    HOST_TEMPLATES = "host_templates"
    """HostTemplates this Template inherits from"""
    SCHEDULING_INTERVAL = "scheduling_interval"
    """Interval the checks should be scheduled, in seconds"""
    SCHEDULING_PERIOD = "scheduling_period"
    """TimePeriod for scheduling the check"""
    NOTIFICATION_PERIOD = "notification_period"
    """TimePeriod for a notification period"""
    VARIABLES = "variables"
    """Key Value Pairs for variables"""
