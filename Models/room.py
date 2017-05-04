class Room(object):
    """Creates the super class Room that defines the common attributes for the other classes"""

    def __init__(self, room_name):
        self.room_id = id(self)
        self.room_name = room_name
        self.occupants = []


class LivingSpace(Room):
    """Creates class LivingSpace that overides the Room class"""
    capacity = 4

    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name)


class Office(Room):
    """Creates class Office that overides the Room class"""
    capacity = 6

    def __init__(self, room_name):
        super(Office, self).__init__(room_name)
