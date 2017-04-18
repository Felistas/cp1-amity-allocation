import random
import sqlite3
from tabulate import tabulate
from Models.person import Fellow, Staff
from Models.room import Office, LivingSpace


class Amity:
    rooms = {'living_space': [], 'office': []}
    people = []
    office_waiting_list = []
    living_space_waiting_list = []

    def create_room(self, room_type, room_names):
        room_type = room_type.upper()
        # check for already existing room
        for room_name in room_names:
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
            offices = self.rooms['office']
            living_spaces = self.rooms['living_space']
            if len(offices):
                # select a random office
                return random.choice(self.rooms['office'])

        elif room_type == 'LIVINGSPACE':
            living_spaces = self.rooms['living_space']
            if len(living_spaces):
                # select a random living  space
                return random.choice(self.rooms['living_space'])
        else:
            return 'Invalid room type'

    def add_person(self, role, first_name, last_name, accommodation="NO"):
        role = role.upper()
        first_name = first_name.upper()
        last_name = last_name.upper()
        accommodation = accommodation.upper()
        if role == 'FELLOW':
            # create fellow object
            fellow = Fellow(role, first_name, last_name, accommodation)
            self.people.append(fellow)
            print('{} {} {} successfully added'.format(
                fellow.role, fellow.first_name, fellow.last_name))
            # allocate office
            office_selected_random = self.allocate_room("office")
            if office_selected_random:
                if len(office_selected_random.occupants) < office_selected_random.office_capacity:
                    office_selected_random.occupants.append(fellow)
                    print('You have been allocated to office' +
                          office_selected_random.room_name)
            else:
                self.office_waiting_list.append(fellow)
                print('You have been added to office waiting list')
            if accommodation == 'YES':
                    # check if there are available livigspaces and offices
                living_space_selected_random = self.allocate_room("livingspace")
                if living_space_selected_random:
                    if len(living_space_selected_random.occupants) < living_space_selected_random.living_space_capacity:
                        living_space_selected_random.occupants.append(fellow)
                        print('You have been allocated to living space' +
                              living_space_selected_random.room_name)
                else:
                    self.living_space_waiting_list.append(fellow)
                    print('You have been added to livingspace waiting list')
        elif role == 'STAFF':
            staff = Staff(role, first_name, last_name,  accommodation)
            self.people.append(staff)
            print('{} {} {} successfully added'.format(
                staff.role, staff.first_name, staff.last_name))
            if accommodation == 'YES':
                print("Staff cannot get accommodation")
            else:
                office_selected_random = self.allocate_room("office")
                if office_selected_random:
                    if len(office_selected_random.occupants) < office_selected_random.office_capacity:
                        office_selected_random.occupants.append(staff)
                        print('You have been allocated to office' +
                              office_selected_random.room_name)
                else:
                    self.office_waiting_list.append(staff)
                    print('You have been added to office waiting list')

    def print_person_id(self, first_name, last_name):
        """ Print the person id given the person name"""
        first_name = first_name.upper()
        last_name = last_name.upper()
        ids = [person.person_id for person in self.people if first_name ==
               person.first_name and last_name == person.last_name]
        for person_id in ids:
            if person_id:
                print(person_id, first_name, last_name)
            else:
                print("Person does not exist")

    def reallocate_person(self, person_id, room_name):
        ''' check if the room the user chooses exists
        check if there is capacity in the room provided
        check the room type of the room provided
        check if the person ID provided exist
        check the role of the person and assert staff cannot get accommodation
        if fellow check if he/she is the livingspace waiting list then reallocate_person
        if in another room check the room type of the previous room
        remove the fellow from the previous room
        append person to the new room
        check person should not be reallocated to the same room
        '''
        # check if the room exists

        for room_name in room_name:
            all_rooms = self.rooms['office'] + self.rooms['living_space']
            room = [room.room_name for room in all_rooms if room_name ==
                    room.room_name]
            new_room_type = room.room_type
            if room:
                room_type = room_type.upper()
                if room.room_type == 'OFFICE':
                    if len(room.occupants) < room.office_capacity:
                        pass
                    else:
                        print("{} is full".format(room.room_name))
                elif room.room_type == 'LIVINGSPACE':
                    if len(room.occupants) < room.living_space_capacity:
                        # check if the person id given is correct
                        ids = [
                            person.person_id for person in self.people if person_id == person.person_id]
                        for person_id in ids:
                            role = role.upper()
                            if person_id:
                                # check the role of the person
                                if person.role == "STAFF":
                                    print(
                                        "Staff cannot be reallocated to a livingpsace")
                                else:
                                    for person in self.living_space_waiting_list:
                                        if person.person_id == person_id:
                                            room.occupants.append(person)
                                        elif person in room.occupants:
                                            person_room_type = room.room_type
                                            if person_room_type != new_room_type:
                                                print(
                                                    "Person cannot be reallocated to different room type")
                                            else:
                                                room.occupants.remove(person)
                                                new_room = room.room_name
                                                new_room.occupants.append(
                                                    fellow)
                            else:
                                print("Person does not exist")
                    else:
                        print("{} is full".format(room.room_name))

            else:
                return 'Room does not exist'

    def load_people(self):
        pass

    def print_available_rooms(self):
        offices = self.rooms['office']
        if len(office.occupants) < office.office_capacity:
            for office in offices:
                empty_offices = []
                empty_offices.append(office)
        else:
            print("No empty offices available")
        living_spaces = self.rooms['living_space']
        if len(living_space.occupants) < living_space.living_space_capacity:
            for living_space in living_spaces:
                empty_living_spaces = []
                empty_living_spaces.append(living_space)
        else:
            print("No empty living spaces available")

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
