
class Base(dict):

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self[item]
