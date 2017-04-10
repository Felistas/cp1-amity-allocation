class Room(object):
    persons = []

    def __init__(self, room_name):
        self.room_id = id(self)
        self.name = room_name


class LivingSpace(Room):
    capacity = 4

    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name)
        self.allocated_livingspace = []


class Office(Room):
    capacity = 6

    def __init__(self, room_name):
        super(Office, self).__init__(room_name)
        self.allocated_office = []
