class OperationError(Exception):
    """Basic exception for errors raised by dizme_rest"""
    def __init__(self, msg=None):
        if msg is None:
            # Set some default useful error message
            msg = "An error occured with car %s" % car
        super(OperationError, self).__init__(msg)
