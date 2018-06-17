#
# Module Imports
from graph.create_interface import CreateInterface
from graph.delete_interface import DeleteInterface
from graph.update_interface import UpdateInterface
#
class CRUDInterface(CreateInterface, DeleteInterface, UpdateInterface):
    """
    Child class which inherits from Create, Delete, Read Interfaces.

    This class is useful for the developer to instantiate, and call
    all inherited functionality through it.
    """
    #
    def __init__(self, uri, user, password):
        CreateInterface.__init__(self, uri, user, password)
        DeleteInterface.__init__(self, uri, user, password)
        UpdateInterface.__init__(self, uri, user, password)