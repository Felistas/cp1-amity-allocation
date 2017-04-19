class Room(object):

    def __init__(self, room_name):
        self.room_id = id(self)
        self.room_name = room_name
        self.occupants = []


class LivingSpace(Room):
    capacity = 4

    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name)


class Office(Room):
    capacity = 6

    def __init__(self, room_name):
        super(Office, self).__init__(room_name)
