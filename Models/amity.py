import random
import sqlite3
from tabulate import tabulate
from Models.person import Fellow, Staff
from Models.room import Office, LivingSpace


class Amity:
    rooms = {'living_space': [], 'office': []}
    office_waiting_list = []
    living_space_waiting_list = []

    def create_room(self, room_type, room_name):
        room_type = room_type.upper()
        # check for already existing room
        all_rooms = self.rooms['office'] + self.rooms['living_space']
        check_room = [
            room.room_name for room in all_rooms if room.room_name == room_name]
        if check_room:
            print('{} already exists'.format(room_name))
        else:
            # create office and livingspace
            if room_type == 'OFFICE':
                room = Office(room_name)
                self.rooms['office'].append(room)
                print('{} successfully created'.format(room_name))
            elif room_type == 'LIVINGSPACE':
                room = LivingSpace(room_name)
                self.rooms['living_space'].append(room)
                print('{} successfully created'.format(room_name))
    # pick a room at random to allocate a person

    def allocate_room(self, room_type):
        room_type = room_type.upper()
        if room_type == "OFFICE":
            offices = list(self.rooms['office'].keys())
            living_spaces = list(self.rooms['living_space'].keys())
            if len(offices):
                # select a random office
                return self.rooms['office'][random.choice(offices)]
        else:
            if len(living_spaces):
                # select a random living  space
                return self.rooms['living_space'][random.choice(living_spaces)]

    def add_person(self, role, first_name, last_name, accommodation="NO"):
        role = role.upper()
        first_name = first_name.upper()
        last_name = last_name.upper()
        accommodation = accommodation.upper()
        if role == 'FELLOW':
            # create fellow object
            fellow = Fellow(role, first_name, last_name, accommodation)
            print('{} {} {} successfully added'.format(
                fellow.role, fellow.first_name, fellow.last_name))
            if accommodation == 'YES':
                # check if there are available livigspaces and offices
                living_space_selected_random = self.allocate_room("livingspace")
                office_selected_random = self.allocate_room("office")
                # if there is no room available or the room is full
                # room for room in list(room['office'].keys()) if
                # len(self.rooms["office"][room]) < 6
                if len(living_space_selected_random.allocated_livingspace) == 6:
                    self.living_space_waiting_list.append(fellow)
                if len(office_selected_random.allocated_office) == 4:
                    self.office_waiting_list.append(fellow)
                # print('You have been added to a waiting list')
                else:
                    # append person to office object
                    self.rooms['living_space'][living_space_allocated_room.name].occupants += [fellow]
                    print('You have been allocated to living space ' +
                          living_space_allocated_room.name)
                    self.rooms['office'][office_allocated_room.name].occupants += [fellow]
                    print('You have been allocated to office ' +
                          office_allocated_room.name)
            elif accommodation == 'NO':
                allocated_room = self.allocate_room("office")
                if allocated_room is None or len(allocated_room.occupants) == allocated_room.capacity:
                    # allocate to waiting list
                    self.office_waiting_list.append(fellow)
                    print(
                        'There are no offices available. You have been added to the office waiting list')
                else:
                    # append person to office object
                    self.rooms['office'][allocated_room.name].occupants += [fellow]
                    print('You have been allocated to office ' +
                          allocated_room.name)
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
        offices = list(self.rooms["office"].keys())
        if len(offices) > 0:
            for office in offices:
                if len(self.rooms["office"][office]) > 0:
                    print("{}".format(office.room_name))
                    print("---------------------------")
                    people_allocated_that_living_space = []
                    for person in self.rooms["office"][office]:
                        name = person.first_name + " " + person.last_name
                        people_allocated_that_living_space.append(name)
                        print(', '.join(people_allocated_that_living_space))
                else:
                    print("There are no occupants in the room")
        else:
            print("No office spaces currenty added")
        living_spaces = list(self.rooms['living_space'].keys())
        if len(living_spaces) > 0:
            for livingspace in living_spaces:
                if len(self.rooms['living_space'][livingspace]) > 0:
                    print("{}".format(livingspace.name))
                    print("---------------------------")
                    people_allocated_that_office = []
                    for person in self.rooms['living_space'][livingspace]:
                        name = person.first_name + " " + person.last_name
                        people_allocated_that_office.append(name)
                        print(''.join(people_allocated_that_office))
                else:
                    print("There are no occupants in the room")

        else:
            print("There are no living spaces added currently")

    def print_unallocated(self, filename=None):
        # print people not allocated to office
        if len(Amity.office_waiting_list) == 0 and len(Amity.living_space_waiting_list) == 0:
            print("Everyone within the system has an office or livingspace")
        else:
            print("People not allocated to office \n")
            print("---------------------------")
            unallocated_office_space = ['\n'.join(str(
                person.person_id) + ' ' + person.first_name + ' ' + person.last_name for person in Amity.office_waiting_list)]
            print(unallocated_office_space)
            # print people not allocated to living space
            print("People not allocated to living space \n")
            print("---------------------------")
            unallocated_living_space = ['\n'.join(str(
                person.person_id) + ' ' + person.first_name + ' ' + person.last_name for person in Amity.living_space_waiting_list)]
            print(unallocated_living_space)

    def print_all_rooms(self):
        offices = list(Amity.rooms['living_space'].keys())
        if len(offices) > 0:
            for office in offices:
                print("OFFICES")
                print("---------------------------")
                print(office.room_name)
        else:
            print("There are no offices")
        living_spaces = list(self.rooms['living_space'].keys())
        if len(living_spaces) > 0:
            for living_space in living_spaces:
                print("LIVING SPACES")
                print("---------------------------")
                print(living_space.room_name)
        else:
            print("There are no livingspaces")

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
