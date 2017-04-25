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
        '''
        Gets a list of all rooms
        Checks if a room exists
        Creates office
        Creates living space
        '''
        msg = ''
        room_type = room_type.title()
        for room_name in room_names:
            room_name = room_name.title()
            all_rooms = self.rooms['office'] + self.rooms['living_space']
            check_room = [
                room.room_name for room in all_rooms if room.room_name == room_name]
            if check_room:
                msg += '\n{} already exists\n'.format(room_name)
            else:
                if room_type == 'Office':
                    room = Office(room_name)
                    self.rooms['office'].append(room)
                    msg += '\nSuccessfully created Office ' + room.room_name + '\n'
                elif room_type == 'Livingspace':
                    room = LivingSpace(room_name)
                    self.rooms['living_space'].append(room)
                    msg += '\nSuccessfully created Living Space ' + room.room_name + '\n'
        return msg

    def allocate_room(self, room_type):
        '''
        Selects an office at random
        Selects a living space at random
        Checks that room type should be either livingspace or office
        '''
        room_type = room_type.title()
        if room_type == "Office":
            offices = self.rooms['office']
            if len(offices):
                return random.choice(self.rooms['office'])
        elif room_type == 'Livingspace':
            living_spaces = self.rooms['living_space']
            if len(living_spaces):
                return random.choice(self.rooms['living_space'])
        else:
            return 'Invalid room type'

    def add_person(self, role, first_name, last_name, accommodation="NO"):
        '''
        Validates that person names and roles should be strings
        Adds a staff and assign them an office
        Adds fellow and assign them living space and office
        Handle staff cannot get accommodation
        If no available offices add to office waiting list
        If no available living spaces add to living_space waiting list
        '''
        msg = ''
        if first_name.isalpha() is False and last_name.isalpha() is False and role.isalpha():
            msg += "\nInvalid input\n"
        else:
            role = role.title()
            first_name = first_name.title()
            last_name = last_name.title()
            accommodation = (accommodation.title()
                             if accommodation is not None else "NO")
            if role == 'Fellow':
                fellow = Fellow(role, first_name, last_name, accommodation)
                self.people.append(fellow)
                msg += ('\n' + fellow.role + ' ' + fellow.first_name + ' ' +
                        fellow.last_name + ' successfully added\n')
                office_selected_random = self.allocate_room("office")
                if office_selected_random:
                    if len(office_selected_random.occupants) < office_selected_random.capacity:
                        office_selected_random.occupants.append(fellow)
                        msg += '\nYou have been allocated to office ' + \
                            office_selected_random.room_name + '\n'
                    else:
                        self.office_waiting_list.append(fellow)
                        msg += '\nYou have been added to office waiting list \n'
                else:
                    self.office_waiting_list.append(fellow)
                    msg += '\nYou have been added to office waiting list \n'
                if accommodation == 'Yes' or accommodation == 'Y':
                    living_space_selected_random = self.allocate_room(
                        "livingspace")
                    if living_space_selected_random:
                        if len(living_space_selected_random.occupants) < living_space_selected_random.capacity:
                            living_space_selected_random.occupants.append(
                                fellow)
                            msg += '\nYou have been allocated to living space ' + \
                                living_space_selected_random.room_name + '\n'
                        else:
                            self.living_space_waiting_list.append(fellow)
                            msg += '\nYou have been added to living space waiting list \n'
                    else:
                        self.living_space_waiting_list.append(fellow)
                        msg += '\nYou have been added to living space waiting list \n'
            elif role == 'Staff':
                if accommodation == 'Yes' or accommodation == "Y":
                    msg += "\nStaff cannot get accommodation \n"
                staff = Staff(role, first_name, last_name,  accommodation)
                self.people.append(staff)
                msg += '\n{} {} {} successfully added\n'.format(
                    staff.role, staff.first_name, staff.last_name)
                office_selected_random = self.allocate_room("office")
                if office_selected_random:
                    if len(office_selected_random.occupants) < office_selected_random.capacity:
                        office_selected_random.occupants.append(staff)
                        msg += '\nYou have been allocated to office ' + \
                            office_selected_random.room_name + '\n'
                    else:
                        self.office_waiting_list.append(staff)
                        msg += '\nYou have been added to office waiting list \n'
                else:
                    self.office_waiting_list.append(staff)
                    msg += '\nYou have been added to office waiting list \n'
        return msg

    def print_person_id(self, first_name, last_name):
        """ Print the person id given the person first and last name"""
        msg = ''
        first_name = first_name.title()
        last_name = last_name.title()
        ids = [person for person in self.people if first_name ==
               person.first_name and last_name == person.last_name]
        if len(ids) > 0:
            for id in ids:
                msg += str(id.person_id) + ' ' + id.first_name + \
                    ' ' + id.last_name + '\n'
        else:
            msg += "Person does not exist"
        return msg

    def reallocate_person(self, person_id, room_name):
        '''
        Check if the person_id of the user is valid
        Check if the room the user chooses to be reallocated exists
        Check if there is capacity in the room provided
        Check the room type of the room provided so as to not reallocate to different room type
        Check the role of the person and assert staff cannot get accommodation
        Remove the fellow from the previous room
        Append person to the new room
        Check person should not be reallocated to the same room
        '''
        room_name = room_name.title()
        msg = ''
        person = [person for person in self.people if int(person_id) ==
                  person.person_id]
        if len(person) == 0:
            return '\n{} does not exist\n'.format(person_id)
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
            return '\n{} had not been allocated a room\n'.format(person.first_name)
        if new_room is not None:
            room_type = type(new_room)
            role = person.role.title()
            if role == 'Staff' and room_type == LivingSpace:
                return '\nCannot reallocate staff to livingspace\n'
            if not type(new_room) in [type(room) for room in previous_rooms]:
                return '\nCannot reallocate from one room type to another\n'
            if len(new_room.occupants) == new_room.capacity:
                return '\nRoom is full\n'
            if new_room in previous_rooms:
                return '\nCannot reallocate to the same room\n'
            for room in previous_rooms:
                if person in room.occupants:
                    room.occupants.remove(person)
            new_room.occupants.append(person)
            return '\nSuccessfully reallocated to {}\n'.format(new_room.room_name)
        else:
            return '\n{} does not exist\n'.format(room_name)

    def allocate_office_waiting_list(self):
        '''
        Check for available room space
        Allocate an office randomly
        Remove the person from the office waiting list
        '''
        msg = ''
        offices = self.rooms['office']
        if len(offices) > 0:
            if len(self.office_waiting_list) > 0:
                for person in self.office_waiting_list:
                    random_office = self.allocate_room("office")
                    if len(random_office.occupants) < random_office.capacity:
                        random_office.occupants.append(person)
                        self.office_waiting_list.remove(person)
                        msg += "\n{} {} has been allocted to room {}\n".format(person.first_name, person.last_name,
                                                                               random_office.room_name)
                    else:
                        msg += "\nNo offices available\n"

            else:
                msg += "\nThere are no people in the waiting list\n"
        else:
            msg += "\nNo offices available\n"
        return msg

    def allocate_livingspace_waiting_list(self):
        '''
        Check for available living space space
        Allocate an living space randomly
        Remove the person from the living space waiting list
        '''
        msg = ''
        living_spaces = self.rooms['living_space']
        if len(living_spaces) > 0:
            if len(self.living_space_waiting_list) > 0:
                for person in self.living_space_waiting_list:
                    random_living_space = self.allocate_room("livingspace")
                    if len(random_living_space.occupants) < random_living_space.capacity:
                        random_living_space.occupants.append(person)
                        self.living_space_waiting_list.remove(person)
                        msg += "\n{} {} has been allocted to room {}\n".format(person.first_name, person.last_name,
                                                                               random_living_space.room_name)
                    else:
                        msg += "\nNo livingspace available\n"
            else:
                msg += "\nThere are no people in the waiting list\n"
        else:
            msg += "\nNo livingspace available\n"
        return msg

    def load_people(self, filename):
        msg = ''
        try:
            with open(filename + '.txt') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.replace("\n", "")
                    l = line.split(' ')
                    first_name = l[0]
                    last_name = l[1]
                    role = l[2]
                    accommodation = (l[3] if len(l) > 3 else "No")
                    msg += self.add_person(role, first_name,
                                           last_name, accommodation)
        except:
            msg += 'File does not exist'
        return msg

    def print_available_rooms(self):
        '''
        Checks if all offices are full
        Prints available offices with space
        Checks if all living spaces are full
        Prints available living spaces
        '''
        msg1 = ''
        offices = self.rooms['office']
        for office in offices:
            if len(office.occupants) < office.capacity:
                msg1 += "Offices"
                msg1 += "\n--------------------------- \n"
                msg1 += office.room_name
            else:
                msg1 += "\nNo offices available\n"
        if msg1 == '':
            msg1 += "\nNo offices available\n"
        msg2 = ''
        living_spaces = self.rooms['living_space']
        for living_space in living_spaces:
            if len(living_space.occupants) < living_space.capacity:
                msg2 += "\nLiving Spaces"
                msg2 += "\n--------------------------- \n"
                msg2 += living_space.room_name
            else:
                msg2 += "\nNo living spaces available\n"
        if msg2 == '':
            msg2 += "\nNo living spaces available\n"
        return msg1 + msg2

    def print_allocations(self, filename=None):
        '''
        Checks if there are rooms
        Checks for occupants in a room
        Prints the occupants in the room
        '''
        all_rooms = self.rooms["office"] + self.rooms["living_space"]
        msg = ''
        if len(all_rooms) > 0:
            for room in all_rooms:
                if len(room.occupants) > 0:
                    msg += room.room_name
                    msg += "\n--------------------------- \n"
                    for person in room.occupants:
                        msg += (person.first_name + " " +
                                person.last_name + ",")
            if msg == '':
                return 'There are no allocations'
            if filename:
                file = open(filename, 'w')
                file.write(msg)
                file.close()
                msg += '\nSuccessfully saved to ' + filename + ' textfile'
            return msg
        else:
            return "No rooms available for allocations"

    def print_unallocated(self, filename=None):
        '''Check if there are people added in the office waiting list
        Prints all people unallocated office
        Checks if there are people in the living psace waiting list
        Prints all people unallocated living space
         '''
        msg = ''
        if len(Amity.office_waiting_list) == 0 and len(Amity.living_space_waiting_list) == 0:
            return "\nThere are no unallocated people\n"
        else:
            msg += "People not allocated to office \n"
            msg += "---------------------------\n"
            unallocated_office_space = '\n'.join(str(
                person.person_id) + ' ' + person.first_name + ' ' + person.last_name + '\n' for person in Amity.office_waiting_list)
            msg += unallocated_office_space
            msg += "\nPeople not allocated to living space \n"
            msg += "---------------------------\n"
            unallocated_living_space = '\n'.join(str(
                person.person_id) + ' ' + person.first_name + ' ' + person.last_name + '\n' for person in Amity.living_space_waiting_list)
            msg += unallocated_living_space
            if filename:
                file = open(filename, 'w')
                file.write(unallocated_office_space)
                file.write(unallocated_living_space)
                file.close()
                msg += '\n Successfully saved to ' + filename
        return msg

    def print_all_rooms(self):
        '''Checks if there are offices
        Prints of all offices
        Checks if there are any living spaces
        Prints all living spaces '''
        offices = list(Amity.rooms['office'])
        msg = ''
        if len(offices) > 0:
            for office in offices:
                msg += "OFFICES"
                msg += "\n---------------------------\n"
                msg += office.room_name
        else:
            msg += "There are no offices\n"
        living_spaces = list(self.rooms['living_space'])
        if len(living_spaces) > 0:
            for living_space in living_spaces:
                msg += "\nLIVING SPACES"
                msg += "\n---------------------------\n"
                msg += living_space.room_name
        else:
            msg += "\nThere are no livingspaces"
        return msg

    def print_room(self):
        """Prints the occupants of the room provided"""
        msg = ''
        all_rooms = self.rooms["office"] + self.rooms["living_space"]
        for room in all_rooms:
            if len(room.occupants) > 0:
                for person in room.occupants:
                    msg += str(person.first_name) + ' ' + \
                        person.last_name + '\n'
            else:
                msg += "There are no occupants in the room"
        return msg

    def save_state(self, dbname="amity.db"):
        """
        Creates table called allocated
        Saves all rooms created and occupants of the rooms to the table
        Creates table unallocated
        Saves all objects in office waiting list and living space waiting list to the table
        """
        dbname = dbname if dbname else "amity.db"
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()
        # curs.execute("""CREATE TABLE IF NOT EXISTS allocated (aID INTEGER PRIMARY KEY UNIQUE,
        #              rooms TEXT, occupants TEXT)""")
        # all_rooms = self.rooms["office"] + self.rooms["living_space"]
        # for room in all_rooms:
        #     for person in room.occupants:
        #         person = person.first_name
        #         curs.execute(
        #             "INSERT INTO allocated (rooms, occupants) VALUES (?, ?)", (room.room_name, person))
        # curs.execute("""CREATE TABLE IF NOT EXISTS unallocated
        #              (aID INTEGER PRIMARY KEY UNIQUE,
        #              office_waiting_list TEXT, living_space_waiting_list TEXT)""")
        # for person in self.living_space_waiting_list:
        #     person = person.first_name
        # for person in self.office_waiting_list:
        #     person = person.first_name
        # curs.execute("INSERT INTO unallocated (office_waiting_list,living_space_waiting_list) VALUES (?, ?)",
        #              (person, person))
        curs.execute(
            """CREATE TABLE IF NOT EXISTS people (pID INTEGER PRIMARY KEY UNIQUE, name TEXT, role TEXT, accommodation TEXT)""")
        for person in self.people:
            name = person.first_name + ' ' + person.last_name
            role = person.role
            accommodation = person.accommodation
            curs.execute("INSERT INTO people (name,role,accommodation) VALUES (?,?,?)",
                         (name, role, accommodation))
        curs.execute(
            """CREATE TABLE IF NOT EXISTS rooms (pID INTEGER PRIMARY KEY UNIQUE, name TEXT, type TEXT, occupants TEXT)""")
        office_occupants = ''
        for office in self.rooms['office']:
            office_name = office.room_name
            office_type = "office"
            for person in office.occupants:
                office_occupants += person.first_name + ' ' + person.last_name + ','
            curs.execute(
                "INSERT INTO rooms (name,type,occupants) VALUES (?,?,?)", (office_name, office_type, office_occupants))
        livingspace_occupants = ''
        for livingspace in self.rooms['living_space']:
            livingspace_name = livingspace.room_name
            livingspace_type = 'living_space'
            for person in livingspace.occupants:
                livingspace_occupants += person.first_name + ' ' + person.last_name + ','
            curs.execute(
                "INSERT INTO rooms (name,type,occupants) VALUES (?,?,?)", (livingspace_name, livingspace_type, livingspace_occupants))
        conn.commit()
        conn.close()
        return 'Data successfully exported to the Database'

    def load_state(self, dbname):
        """
        Fetches all data in allocated table in prints it on the screen
        Fetches all data in the unallocated table and prints it on the screen
        """
        try:
            msg = ''
            conn = sqlite3.connect(dbname)
            curs = conn.cursor()
            curs.execute(
                "SELECT * FROM allocated WHERE aID = (SELECT MAX(aID) FROM allocated)")
            allocated = curs.fetchone()
            for row in allocated:
                print(row)
            curs.close()
            conn.close()
            curs.execute(
                "SELECT * FROM unallocated WHERE aID = (SELECT MAX(aID) FROM unallocated)")
            data = conn.fetchone()
            for row in unallocated:
                print(row[1], row[2])
            msg += 'Successfully loaded data from the Database'
        except:
            msg += "Provide database name"
        return msg
