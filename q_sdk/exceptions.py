
class HttpStatusCodeException(Exception):
    def __init__(self, status_code, msg):
        self.status_code = status_code
        self.msg = msg
        super(HttpStatusCodeException, self).__init__(msg)
