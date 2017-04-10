import random

from Models.person import Fellow, Staff
from Models.room import Office, LivingSpace


class Amity:
    rooms = {'living_space': {}, 'office': {}}
    office_waiting_list = []
    living_space_waiting_list = []

    def create_room(self, room_type, room_names):
        room_type = room_type.upper()
        rooms = list(self.rooms['living_space'].keys())
        rooms += list(self.rooms['office'].keys())
        for room_name in room_names:
            check_room = room_name in rooms
            if check_room:
                print('{} already exists'.format(room_name))
            else:
                if room_type == 'OFFICE':
                    room = Office(room_name)
                    self.rooms['office'].update({room_name: room})
                    print('{} successfully created'.format(room_name))
                elif room_type == 'LIVINGSPACE':
                    room = LivingSpace(room_name)
                    self.rooms['living_space'].update({room_name: room})

    def allocate_room(self, room_type):
        room_type = room_type.upper()
        if room_type == "OFFICE":
            offices = list(self.rooms['office'])
            if len(offices) > 0:
                # select a random office
                return self.rooms['office'][random.choice(offices)]
            else:
                return None
        else:
            living_spaces = list(self.rooms['living_space'])
            if len(living_spaces) > 0:
                # select a random living  space
                return self.rooms['living_space'][random.choice(living_spaces)]
            else:
                return None

    def add_person(self, role, first_name, last_name, accommodation=""):
        role = role.upper()
        first_name = first_name.upper()
        last_name = last_name.upper()
        accommodation = bool(accommodation)
        if role == 'FELLOW':
            fellow = Fellow(role, first_name, last_name, accommodation)
            print('{} {} {} successfully added'.format(fellow.role, fellow.first_name, fellow.last_name))
            if accommodation is True:

                # allocate  an office selected at room
                allocated_room = self.allocate_room("livingspace")

                if allocated_room is None or len(allocated_room.persons) >= allocated_room.capacity:
                    # allocate to waiting list
                    self.office_waiting_list.append(fellow)
                    print('There are no rooms available. You have been added to the waiting list')
                else:
                    # append person to office object
                    self.rooms['living_space'][allocated_room.name].persons += [fellow]
                    print('You have been allocated to room ' + allocated_room.name)

            allocated_room = self.allocate_room("office")

            if allocated_room is None or len(allocated_room.persons) >= allocated_room.capacity:
                # allocate to waiting list
                self.office_waiting_list.append(fellow)
                print('There are no offices available. You have been added to the waiting list')
            else:
                # append person to office object
                self.rooms['office'][allocated_room.name].persons += [fellow]
                print('You have been allocated to office ' + allocated_room.name)
        elif role == 'STAFF':
            if accommodation:
                print("Staff cannot get accommodation")
                return
            staff = Staff(first_name, last_name, role, accommodation)
            # self.person.append(staff)
            # allocate office to staff
            allocated_room = self.allocate_room("office")

            if allocated_room is None or len(allocated_room.persons) >= allocated_room.capacity:
                self.office_waiting_list.append(staff)
                print('There are currently no offices. You have been added to the waiting list')
            else:
                self.rooms['office'][allocated_room.name].persons += [staff]
                print('{} {} {} successfully added'.format(role, first_name, last_name))

    def reallocate_person(self, person_id, new_room_name):
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
