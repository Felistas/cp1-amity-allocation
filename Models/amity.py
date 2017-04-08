import random
from room import Office,LivingSpace
from person import Fellow,Staff
class Amity:

    rooms = {'living_space':{},'office':{}}
    office_waitiing_list = []
    living_space_waitiing_list = []
    def create_room(self,room_type,room_name):
        room_type = room_type.upper()
        rooms = self.rooms['living_space'] + self.rooms['office']

        for room_name in room_name:
            check_room = [room.room_name for room in rooms if room.room_name == room_name]
            if check_room:
                print ('{} already exists'.format(room_name))
            else:
                if room_type == 'OFFICE':
                    room = Office(room_name)
                    self.rooms['office'].append(room)
                    print ('{} successfully created'.format(room_name))
                elif room_type == 'LIVINGSPACE':
                    room = LivingSpace(room_name)
                    self.rooms['living_space'].append(room)
    def allocate_room(self, room_type):
        if room_type == "OFFICE":
            offices = list(self.rooms['office'])
            if len(offices) > 0:
                # select a random office
                return random.choice(offices)
            else:
                return "No office available"
        else:
            living_spaces = list(self.rooms['living_space'])
            if len(living_spaces) > 0:
                # select a random livingspace
                return random.choice(living_spaces)
            else:
                return "No living space available"

    def add_person(self, role, first_name, last_name, accommodation):
        role = role.upper()
        first_name = first_name.upper()
        last_name = last_name.upper()
        accommodation = accommodation.upper()
        if role == 'FELLOW':
            fellow = Fellow(role,first_name,last_name,accommodation)
            self.person.append(fellow)
            print ('{} {} {} succefully added'.format(fellow.role,fellow.first_name,fellow.last_name))
            # allocate  an office selected at random
            allocated_room = self.allocate_room("office")
            if allocated_room == "No office available":
                # allocate to waiting list
                self.office_waiting_list.append(room)
                print('There are no rooms available. You have been added to the waiting list')
            else:
                # append person to office object
                self.rooms['office'].append(room)
                print('You have been allocated to a room')
        elif role == 'STAFF':
            staff = Staff(first_name,last_name,role,accommodation)
            self.person.append(staff)
            print ('{} {} {} succefully added'.format(role,first_name,last_name))
            #allocate office to staff
            allocated_room = self.allocate_room("office")
            if allocated_room == 'No office available':
                self.office_waiting_list.append(staff)
                print('There are currently no offices. You have been added to the waiting list')
            else:
                self.rooms['office'].room.append(staff)


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
