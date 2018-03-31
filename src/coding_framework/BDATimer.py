import time


class BDATimer:
    """
    Simple timer that follows the RAII idiom. Prints the object lifetime duration in seconds to stdout.
    """
    ####################
    # Private members
    __tick_before = None
    ####################

    def __init__(self):
        """
        Constructor.
        """
        self.__tick_before = int(time.time() * 1000)

    def __del__(self):
        """
        Destructor.
        """
        seconds = int((int(time.time() * 1000) - self.__tick_before) / 1000)
        print(seconds)

