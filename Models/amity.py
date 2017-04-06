from room import Office,LivingSpace
from person import Fellow,Staff
class Amity:
    person = []
    rooms = {'living_space':[],'office':[]}
    office_waitiing_list = []
    living_space_waitiing_list = []

    def create_room(self,room_name,room_type):
        room_name == room_name.upper()
        room_type == room_type.upper()
        rooms = self.rooms['living_space'] + self.rooms['office']
        check_room = [room.room_name for room in rooms if room.room_name == room_name]
        if check_room:
            return 'The room already exists'
        if room_type == 'office':
            room = Office(room_name)
            Amity.rooms['office'].append(room)
        else:
            room = LivingSpace(room_name)
            Amity.rooms['living_space'].append(room)

    def add_person(self, first_name, last_name, accommodation):
        pass
    def reallocate_person(self,person_id,new_room_name):
        pass
    def load_people(self):
        pass
    def print_allocation(self):
        pass
    def print_unallocated(self):
        pass
    def print_room(self):
        pass
    def save_state(self):
        pass
    def load_state(self):
        pass


amity = Amity()
amity.create_room('tsavo',"office")
amity.create_room('tsao',"office")
print(amity.rooms)
