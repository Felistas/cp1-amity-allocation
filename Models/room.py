class Room(object):
    def __init__(self, room_name):
        self.room_id = id(self)
        self.room_name = room_name

class LivingSpace(Room):
    maximum_livingspace = 4
    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name)
        self.allocated_livingspace = []

class Office(Room):
    maximum_officespace = 6
    def __init__(self, room_name):
        super(Office, self).__init__(room_name)
        self.allocated_office = []
