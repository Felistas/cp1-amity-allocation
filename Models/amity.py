import random
import sqlite3
from tabulate import tabulate


from Models.person import Fellow, Staff
from Models.room import Office, LivingSpace, Room


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
                    print('{} successfully created'.format(room_name))

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

    def add_person(self, role, first_name, last_name, accommodation="no"):
        role = role.upper()
        first_name = first_name.upper()
        last_name = last_name.upper()
        accommodation = accommodation.upper()
        if role == 'FELLOW':
            fellow = Fellow(role, first_name, last_name, accommodation)
            print('{} {} {} successfully added'.format(
                fellow.role, fellow.first_name, fellow.last_name))
            if accommodation == 'YES':
                # allocate  an office selected at room
                allocated_room = self.allocate_room("livingspace")

                if allocated_room is None or len(allocated_room.occupants) >= allocated_room.capacity:
                    # allocate to waiting list
                    self.living_space_waiting_list.append(fellow)
                    print(
                        'There are no living spaces available. You have been added to the living space waiting list')

                else:
                    # append person to office object
                    self.rooms['living_space'][allocated_room.name].occupants += [fellow]
                    print('You have been allocated to living space ' +
                          allocated_room.name)

            allocated_room = self.allocate_room("office")

            if allocated_room is None or len(allocated_room.occupants) >= allocated_room.capacity:
                # allocate to waiting list
                self.office_waiting_list.append(fellow)
                print(
                    'There are no offices available. You have been added to the office waiting list')
            else:
                # append person to office object
                self.rooms['office'][allocated_room.name].occupants += [fellow]
                print('You have been allocated to office ' + allocated_room.name)
        elif role == 'STAFF':
            staff = Staff(role, first_name, last_name,  accommodation)
            print('{} {} {} successfully added'.format(
                staff.role, staff.first_name, staff.last_name))
            if accommodation == 'YES':
                print("Staff cannot get accommodation")
                return
            else:
                allocated_room = self.allocate_room("office")
                if allocated_room is None or len(allocated_room.occupants) >= allocated_room.capacity:
                    self.office_waiting_list.append(staff)
                    print(
                        'There are currently no offices. You have been added to the office waiting list')
                else:
                    self.rooms['office'][allocated_room.name].occupants += [staff]
                    print('You have been allocated to office ' +
                          allocated_room.name)

    def reallocate_person(self, person_id, new_room_name):
        pass

    def load_people(self):
        pass

    def print_allocations(self, filename=None):
        print('List of fellows with living space')
        # for room in list(Amity.rooms['living_space'].keys()):
        #     print(room)
        for person in Room.occupants:

            print(Room.occupants)

    def print_unallocated(self, filename=None):
        # print people not allocated to office
        if len(Amity.office_waiting_list) == 0 and len(Amity.living_space_waiting_list) == 0:
            print("Everyone within the system has an office or livingspace")
        else:
            print("People not allocated to office \n")
            unallocated_office_space = ['\n'.join(str(
                person.person_id) + ' ' + person.first_name + ' ' + person.last_name for person in Amity.office_waiting_list)]
            print(tabulate(unallocated_office_space))
            # print people not allocated to living space
            print("People not allocated to living space \n")
            unallocated_living_space = ['\n'.join(str(
                person.person_id) + ' ' + person.first_name + ' ' + person.last_name for person in Amity.living_space_waiting_list)]
            print(tabulate(unallocated_living_space))

    def print_all_livingspaces(self):
        for room in list(Amity.rooms['living_space'].keys()):
            print(room)

    def print_all_offices(self):
        for room in list(Amity.rooms['office'].keys()):
            print(room)

    def save_state(self):
        # create database
        conn = sqlite3.coonect('amity.db')
        # create object to manage queries
        curs = conn.Cursor()
        curs.execute("CREATE TABLE IF NOT EXISTS data"
                     "(aID INTEGER PRIMARY KEY UNIQUE,"
                     "rooms TEXT, office_waiting_list TEXT, living_space_waiting_list TEXT, occupants TEXT)")
        rooms = pickle.dumps(Amity.rooms)
        occupants = pickle.dumps(Room.occupants)
        office_waiting_list = pickle.dumps(Amity.office_waiting_list)
        living_space_waiting_list = pickle.dumps(
            Amity.living_space_waiting_list)

        curs.execute("INSERT INTO data VALUES (null, ?, ?, ?, ?);",
                     (all_rooms, all_persons, unallocated_office, unallocated_livingspace))

        db_connect.commit()
        db_connect.close()
        return 'Data successfully exported to the Database'

    def load_state(self):
        try:
            conn = sqlite3.coonect('amity.db')
            curs = conn.cursor()

            curs.execute(
                "SELECT * FROM data WHERE aID = (SELECT MAX(aID) FROM data)")
            data = conn.fetchone()

            Amity.rooms = pickle.loads(data[1])
            Room.occupants = pickle.loads(data[2])
            Amity.office_waiting_list = pickle.loads(data[3])
            Amity.living_space_waiting_list = pickle.loads(data[4])

            curs.close()
            return 'Successfully loaded data from the Database!'

        except Error:
            remove('amity.db')
            return "Database not found, Please check the name and try again!"
