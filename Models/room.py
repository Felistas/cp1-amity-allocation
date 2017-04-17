class Room(object):
    occupants = []

    def __init__(self, room_name):
        self.room_id = id(self)
        self.room_name = room_name


class LivingSpace(Room):
    living_space_capacity = 4

    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name)


class Office(Room):
    office_capacity = 6

    def __init__(self, room_name):
        super(Office, self).__init__(room_name)
