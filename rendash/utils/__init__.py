from . import text

class AttrDict(dict):
    """https://stackoverflow.com/a/14620633
    """

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
