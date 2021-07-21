import enum

from objects.base import Base


class ContactGroup(Base):
    def __init__(self, name, linked_contacts=None):
        super(ContactGroup, self).__init__()
        self.name = name
        self.linked_contacts = linked_contacts


class ContactGroupParam(enum.Enum):
    NAME = "name"
    """Name of the ContactGroup"""
    LINKED_CONTACTS = "linked_contacts"
    """Contacts that are linked to this group"""
