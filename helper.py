


class map():
    
    def __init__(self, filename):
        raise NotImplementedError


class tile():

    def __init__(self,position):
        raise NotImplementedError

class ground(tile):

    def __init__(self,position,color):
        super().__init__(position)