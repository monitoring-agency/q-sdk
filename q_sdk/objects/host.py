import enum

from objects.base import Base


class Host(Base):
    def __init__(
        self, name, linked_proxy, id=None, address="", linked_check=None, disabled=False, host_templates=None,
        scheduling_interval=None, scheduling_period=None, notification_period=None, variables=None, comment=""
    ):
        super(Host, self).__init__()
        self.name = name
        self.linked_proxy = linked_proxy
        self.id = id
        self.address = address
        self.linked_check = linked_check
        self.disabled = disabled
        self.host_templates = host_templates
        self.scheduling_interval = scheduling_interval
        self.scheduling_period = scheduling_period
        self.notification_period = notification_period
        self.variables = variables
        self.comment = comment


class HostParam(enum.Enum):
    NAME = "name"
    """Name of a host"""
    ADDRESS = "address"
    """Address of a host"""
    LINKED_CHECK = "linked_check"
    """Linked check of a host"""
    DISABLED = "disabled"
    """If True, Host is disabled"""
    HOST_TEMPLATES = "host_templates"
    """Templates of a host"""
    SCHEDULING_INTERVAL = "scheduling_interval"
    """Interval the check will be scheduled, in seconds"""
    SCHEDULING_PERIOD = "scheduling_period"
    """TimePeriod for scheduling the check"""
    NOTIFICATION_PERIOD = "notification_period"
    """TimePeriod for executing notifications for the host"""
    VARIABLES = "variables"
    """Key Value Pairs of the host."""
