import enum

from objects.base import Base


class Contact(Base):
    def __init__(self, name=None, mail=None, linked_host_notifications=None, linked_host_notification_period=None,
                 linked_metric_notifications=None, linked_metric_notification_period=None, variables=None, id=None,
                 comment=None):
        super(Contact, self).__init__()
        self.id = id
        self.name = name
        self.mail = mail
        self.linked_host_notifications = linked_host_notifications
        self.linked_host_notification_period = linked_host_notification_period
        self.linked_metric_notifications = linked_metric_notifications
        self.linked_metric_notification_period = linked_metric_notification_period
        self.variables = variables
        self.comment = comment


class ContactParam(enum.Enum):
    NAME = "name"
    """Name of the Contact"""
    MAIL = "mail"
    """Mail of contact"""
    LINKED_HOST_NOTIFICATIONS = "linked_host_notifications"
    """Checks that will be executed for host notifications"""
    LINKED_HOST_NOTIFICATION_PERIOD = "linked_host_notification_period"
    """TimePeriod of the host notifications"""
    LINKED_METRIC_NOTIFICATIONS = "linked_metric_notifications"
    """Check that will be executed for metric notifications"""
    LINKED_METRIC_NOTIFICATION_PERIOD = "linked_metric_notification_period"
    """TimePeriod of the metric notifications"""
    VARIABLES = "variables"
    """Key Value Pairs of a contact"""
