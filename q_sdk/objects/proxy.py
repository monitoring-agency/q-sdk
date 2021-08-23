import enum

from objects.base import Base


class Proxy(Base):
    def __init__(self, name, address, port, secret, web_address, web_port, web_secret, disabled, comment, id=None):
        super(Proxy, self).__init__()
        self.id = id
        self.name = name
        self.address = address
        self.port = port
        self.secret = secret
        self.web_address = web_address
        self.web_port = web_port
        self.web_secret = web_secret
        self.disabled = disabled
        self.comment = comment


class ProxyParam(enum.Enum):
    NAME = "name"
    """Name of the proxy"""
    ADDRESS = "address"
    """Address of the proxy"""
    PORT = "port"
    """Port of the proxy"""
    WEB_ADDRESS = "web_address"
    """Address q-web is reachable from"""
    WEB_PORT = "web_port"
    """Port q-web is reachable from"""
    DISABLED = "disabled"
    """Specify True if proxy should be disabled"""
    COMMENT = "comment"
    """Comment"""
