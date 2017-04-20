import random
import pickle
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
                    print('Office {} successfully created'.format(room_name))
                elif room_type == 'LIVINGSPACE':
                    room = LivingSpace(room_name)
                    self.rooms['living_space'].append(room)
                    print('Living Space {} successfully created'.format(room_name))

    def allocate_room(self, room_type):
        room_type = room_type.upper()
        if room_type == "OFFICE":
            offices = self.rooms['office']
            if len(offices):
                return random.choice(self.rooms['office'])
        elif room_type == 'LIVINGSPACE':
            living_spaces = self.rooms['living_space']
            if len(living_spaces):
                # select a random living  space
                return random.choice(self.rooms['living_space'])
        else:
            return 'Invalid room type'

    def add_person(self, role, first_name, last_name, accommodation="NO"):
        if first_name.isalpha() is False and last_name.isalpha() is False and role.isalpha():
            print("Invalid input")
        else:
            role = role.upper()
            first_name = first_name.upper()
            last_name = last_name.upper()
            accommodation = (accommodation.upper()
                             if accommodation is not None else "NO")
            if role == 'FELLOW':
                # create fellow object
                fellow = Fellow(role, first_name, last_name, accommodation)
                self.people.append(fellow)
                print('Fellow {} {} {} successfully added'.format(
                    fellow.role, fellow.first_name, fellow.last_name))
                # allocate office
                office_selected_random = self.allocate_room("office")
                if office_selected_random:
                    if len(office_selected_random.occupants) < office_selected_random.capacity:
                        office_selected_random.occupants.append(fellow)
                        print('You have been allocated to office' +
                              office_selected_random.room_name)
                else:
                    self.office_waiting_list.append(fellow)
                    print('You have been added to office waiting list')
                if accommodation == 'YES':
                        # check if there are available livigspaces and offices
                    living_space_selected_random = self.allocate_room(
                        "livingspace")
                    if living_space_selected_random:
                        if len(living_space_selected_random.occupants) < living_space_selected_random.capacity:
                            living_space_selected_random.occupants.append(
                                fellow)
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
                        if len(office_selected_random.occupants) < office_selected_random.capacity:
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
        check the room type of the room provided and dont reallocate to different room type
        check if the person ID provided exist
        check the role of the person and assert staff cannot get accommodation
        remove the fellow from the previous room
        append person to the new room
        check person should not be reallocated to the same room
        '''
        # check if the room exists
        person = [person for person in self.people if int(person_id) ==
                  person.person_id]
        if len(person) == 0:
            return '{} does not exist'.format(person.first_name)
        person = person[0]
        all_rooms = self.rooms['office'] + self.rooms['living_space']
        new_room = None
        for room in all_rooms:
            if room.room_name == room_name:
                new_room = room
        previous_rooms = []
        for room in all_rooms:
            if person in room.occupants:
                previous_rooms.append(room)
        if len(previous_rooms) == 0:
            return '{} had been allocated a room'.format(person.first_name)
        if new_room is not None:
            room_type = type(new_room)
            role = person.role.upper()
            if role == 'STAFF' and room_type == LivingSpace:
                return 'Cannot reallocate staff to livingspace'
            if not type(new_room) in [type(room) for room in previous_rooms]:
                return 'Cannot reallocate from one room type to another one'
            if len(new_room.occupants) == new_room.capacity:
                return 'Room is full'
            if new_room in previous_rooms:
                return 'Cannot reallocate to the same room'
            for room in previous_rooms:
                if person in room.occupants:
                    room.occupants.remove(person)
            new_room.occupants.append(person)
            return 'Successfully reallocated to {}'.format(new_room.room_name)
        return '{} does not exist'.format(new_room.room_name)

    def allocate_office_waiting_list(self):
        offices = self.rooms['office']
        if len(offices) > 0:
            if len(self.office_waiting_list) > 0:
                for person in self.office_waiting_list:
                    random_office = self.allocate_room("office")
                    if len(random_office.occupants) < random_office.capacity:
                        random_office.occupants.append(person)
                        print("You have be allocted to room {}".format(
                            person.first_name))
            else:
                print("There are no people in the waiting list")
        else:
            print("No office available")

    def allocate_livingspace_waiting_list(self):
        living_spaces = self.rooms['living_space']
        if len(living_spaces) > 0:
            if len(self.living_space_waiting_list) > 0:
                for person in self.living_space_waiting_list:
                    random_living_space = self.allocate_room("livingspace")
                    if len(random_living_space.occupants) < random_living_space.capacity:
                        random_living_space.occupants.append(person)
                        print("You have be allocted to room {}".format(
                            person.first_name))
            else:
                print("There are no people in the waiting list")
        else:
            print("No livingspaces available")

    def load_people(self):
        pass

    def print_available_rooms(self):
        if len(office.occupants) < office.capacity:
            offices = self.rooms['office']
            for office in offices:
                print(office.room_name)
        else:
            print("No empty offices available")
        if len(living_space.occupants) < living_space.capacity:
            living_spaces = self.rooms['living_space']
            for living_space in living_spaces:
                print(living_space.room_name)
        else:
            print("No empty living spaces available")

    def print_allocations(self, filename=None):
        all_rooms = self.rooms["office"] + self.rooms["living_space"]
        msg = ''
        if len(all_rooms) > 0:
            for room in all_rooms:
                if len(room.occupants) > 0:
                    msg += room.room_name
                    msg += "\n---------------------------\n"
                    for person in room.occupants:
                        msg += (person.first_name + " " +
                                person.last_name + ",")
            return msg
        else:
            return "No offices available"
        if filename:
            file = open(filename, 'w')
            file.write(msg)
            file.close()

    def print_unallocated(self, filename=None):
        # print people not allocated to office
        if len(Amity.office_waiting_list) == 0 and len(Amity.living_space_waiting_list) == 0:
            return "Everyone within the system has an office or livingspace"
        else:
            print("People not allocated to office \n")
            print("---------------------------")
            unallocated_office_space = '\n'.join(str(
                person.person_id) + ' ' + person.first_name + ' ' + person.last_name for person in Amity.office_waiting_list)
            return unallocated_office_space
            # print people not allocated to living space
            print("People not allocated to living space \n")
            print("---------------------------")
            unallocated_living_space = '\n'.join(str(
                person.person_id) + ' ' + person.first_name + ' ' + person.last_name for person in Amity.living_space_waiting_list)
            return unallocated_living_space
        if filename:
            file = open(filename, 'w')
            file.write(unallocated_office_space)
            file.write(unallocated_living_space)
            file.close()

    def print_all_rooms(self):
        offices = list(Amity.rooms['office'])
        if len(offices) > 0:
            for office in offices:
                print("OFFICES")
                print("---------------------------")
                print(office.room_name)
        else:
            print("There are no offices")
        living_spaces = list(self.rooms['living_space'])
        if len(living_spaces) > 0:
            for living_space in living_spaces:
                print("LIVING SPACES")
                print("---------------------------")
                print(living_space.room_name)
        else:
            print("There are no livingspaces")

    def print_room(self):
        all_rooms = self.rooms["office"] + self.rooms["living_space"]
        for room in all_rooms:
            for person in room.occupants:
                print(person.first_name, person.last_name)

    def save_state(self, dbname):
        # create database
        conn = sqlite3.connect(dbname)
        # create object to manage queries
        curs = conn.cursor()
        curs.execute("""CREATE TABLE IF NOT EXISTS allocated (aID INTEGER PRIMARY KEY UNIQUE,
                     rooms TEXT, occupants TEXT)""")
        all_rooms = self.rooms["office"] + self.rooms["living_space"]
        for room in all_rooms:
            for person in room.occupants:
                person = person.first_name
                curs.execute(
                    "INSERT INTO allocated (rooms, occupants) VALUES (?, ?)", (room.room_name, person))
        curs.execute("""CREATE TABLE IF NOT EXISTS unallocated
                     (aID INTEGER PRIMARY KEY UNIQUE,
                     office_waiting_list TEXT, living_space_waiting_list TEXT)""")
        for person in self.living_space_waiting_list:
            person = person.first_name
        for person in self.office_waiting_list:
            person = person.first_name
        curs.execute("INSERT INTO unallocated (office_waiting_list,living_space_waiting_list) VALUES (?, ?)",
                     (person, person))
        conn.commit()
        conn.close()
        return 'Data successfully exported to the Database'

    def load_state(self, dbname):
        try:
            conn = sqlite3.connect(dbname)
            curs = conn.cursor()
            curs.execute(
                "SELECT * FROM allocated WHERE aID = (SELECT MAX(aID) FROM allocated)")
            data = conn.fetchone()
            for row in allocated:
                print row[0], row[1]

            curs.close()
            conn.close()
            curs.execute(
                "SELECT * FROM unallocated WHERE aID = (SELECT MAX(aID) FROM unallocated)")
            data = conn.fetchone()
            for row in unallocated:
                print row[0], row[1]
            return 'Successfully loaded data from the Database!'
        except Error:
            return "Database not found"
