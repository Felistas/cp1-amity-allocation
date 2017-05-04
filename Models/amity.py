import random
import sqlite3
from termcolor import colored
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
                msg += colored('\n{} already exists\n'.format(room_name),'yellow')
            else:
                if room_type == 'Office':
                    room = Office(room_name)
                    self.rooms['office'].append(room)

                    msg += colored('\nSuccessfully created Office ' + room.room_name + '\n','green')

                elif room_type == 'Livingspace':
                    room = LivingSpace(room_name)
                    self.rooms['living_space'].append(room)
                    msg += colored('\nSuccessfully created Living Space ' + room.room_name + '\n', 'green')
        return msg

    def allocate_room(self, room_type):
        '''
        Selects an office at random
        Selects a living space at random
        Checks that room type should be either livingspace or office
        '''
        msg = ''
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
            msg += colored('Invalid room type','red')
        return msg

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
            msg += colored("\nInvalid input\n","red")
        else:
            role = role.title()
            first_name = first_name.title()
            last_name = last_name.title()
            accommodation = (accommodation.title()
                             if accommodation is not None else "NO")
            if role == 'Fellow':
                fellow = Fellow(role, first_name, last_name, accommodation)
                self.people.append(fellow)
                msg += colored(('\n' + fellow.role + ' ' + fellow.first_name + ' ' +
                        fellow.last_name + ' successfully added\n'),'green')
                office_selected_random = self.allocate_room("office")
                if office_selected_random:
                    if len(office_selected_random.occupants) < office_selected_random.capacity:
                        office_selected_random.occupants.append(fellow)
                        msg += colored('\nYou have been allocated to office ' + \
                            office_selected_random.room_name + '\n','green')
                    else:
                        self.office_waiting_list.append(fellow)
                        msg += colored('\nYou have been added to office waiting list \n','yellow')
                else:
                    self.office_waiting_list.append(fellow)
                    msg += colored('\nYou have been added to office waiting list \n','yellow')
                if accommodation == 'Yes' or accommodation == 'Y':
                    living_space_selected_random = self.allocate_room(
                        "livingspace")
                    if living_space_selected_random:
                        if len(living_space_selected_random.occupants) < living_space_selected_random.capacity:
                            living_space_selected_random.occupants.append(
                                fellow)
                            msg += colored('\nYou have been allocated to living space ' + \
                                living_space_selected_random.room_name + '\n','green')
                        else:
                            self.living_space_waiting_list.append(fellow)
                            msg += colored('\nYou have been added to living space waiting list \n','yellow')
                    else:
                        self.living_space_waiting_list.append(fellow)
                        msg += colored('\nYou have been added to living space waiting list \n','yellow')
            elif role == 'Staff':
                if accommodation == 'Yes' or accommodation == "Y":
                    msg += colored("\nStaff cannot get accommodation \n","red")
                staff = Staff(role, first_name, last_name,  accommodation)
                self.people.append(staff)
                msg += colored('\n{} {} {} successfully added\n'.format(
                    staff.role, staff.first_name, staff.last_name),'green')
                office_selected_random = self.allocate_room("office")
                if office_selected_random:
                    if len(office_selected_random.occupants) < office_selected_random.capacity:
                        office_selected_random.occupants.append(staff)
                        msg += colored('\nYou have been allocated to office ' + \
                            office_selected_random.room_name + '\n','green')
                    else:
                        self.office_waiting_list.append(staff)
                        msg += colored('\nYou have been added to office waiting list \n','yellow')
                else:
                    self.office_waiting_list.append(staff)
                    msg += colored('\nYou have been added to office waiting list \n','yellow')
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
                msg += (str(id.person_id) + ' ' + id.first_name + \
                    ' ' + id.last_name + '\n')
        else:
            msg += colored("Person does not exist",'yellow')
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
            return colored('\n{} does not exist\n'.format(person_id),'yellow')
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
            return colored('\n{} had not been allocated a room\n'.format(person.first_name),'yellow')
        if new_room is not None:
            room_type = type(new_room)
            role = person.role.title()
            if role == 'Staff' and room_type == LivingSpace:
                return colored('\nCannot reallocate staff to livingspace\n','yellow')
            if not type(new_room) in [type(room) for room in previous_rooms]:
                return colored('\nCannot reallocate from one room type to another\n','yellow')
            if len(new_room.occupants) == new_room.capacity:
                return colored('\nRoom is full\n','yellow')
            if new_room in previous_rooms:
                return colored('\nCannot reallocate to the same room\n','yellow')
            for room in previous_rooms:
                if person in room.occupants:
                    room.occupants.remove(person)
            new_room.occupants.append(person)
            return colored('\nSuccessfully reallocated to {}\n'.format(new_room.room_name),'green')
        else:
            return colored('\n{} does not exist\n'.format(room_name),'red')

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
                        msg += colored("\n{} {} has been allocted to room {}\n".format(person.first_name, person.last_name,
                                                                               random_office.room_name),'green')
                    else:
                        msg += colored("\nNo offices available\n",'yellow')

            else:
                msg += colored("\nThere are no people in the waiting list\n",'yellow')
        else:
            msg += colored("\nNo offices available\n",'yellow')
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
                        msg += colored("\n{} {} has been allocted to room {}\n".format(person.first_name, person.last_name,
                                                                               random_living_space.room_name),'green')
                    else:
                        msg += colored("\nNo livingspace available\n",'yellow')
            else:
                msg += colored("\nThere are no people in the waiting list\n",'yellow')
        else:
            msg += colored("\nNo livingspace available\n",'yellow')
        return msg

    def delete_room(self, room_name):
        all_rooms = self.rooms['office'] + self.rooms['living_space']
        msg = ''
        room_name = room_name.title()
        for room in all_rooms:
            if room_name == room.room_name:
                offices = self.rooms['office']
                if room in offices:
                    for occupant in room.occupants:
                        self.office_waiting_list.append(occupant)
                    self.rooms['office'].remove(room)
                    msg += colored('Successfully deleted room {}'.format(
                        room.room_name),'green')
                livingspaces = self.rooms['living_space']
                if room in livingspaces:
                    for occupant in room.occupants:
                        self.living_space_waiting_list.append(occupant)
                    self.rooms['living_space'].remove(room)
                    msg += colored('Successfully deleted room {}'.format(
                        room.room_name),'green')
        if msg == '':
            msg += colored('Room {} does not exist'.format(room_name),'yellow')
        return msg

    def list_all_people(self):
        """Lists all people in the system"""
        msg = ''
        msg += "People\n"
        msg += "-----------------------------------------\n"
        for person in self.people:
            msg += colored(str(person.person_id) + ' ' + \
                person.first_name + ' ' + person.last_name + '\n','green')
        return msg

    def delete_person(self, person_id):
        """
        Check if the person exists in the system
        Deletes a person in the room he/she was in
        """
        msg = ''
        person = [person for person in self.people if int(person_id) == person.person_id]
        if len(person) > 0:
            all_rooms = self.rooms['office'] + self.rooms['living_space']
            if person[0] in self.office_waiting_list:
                self.office_waiting_list.remove(person[0])
            if person[0] in self.living_space_waiting_list:
                self.living_space_waiting_list.remove(person[0])
            if len(all_rooms)>0:
                for room in all_rooms:
                    if person[0] in room.occupants:
                        room.occupants.remove(person[0])
            self.people.remove(person[0])
            msg += colored('Successfully deleted {}'.format(person[0].first_name),'green')
        else:
            msg += colored('Person does not exist','yellow')
        return msg

    def load_people(self, filename):
        '''Adds people in the system from a text file
        Allocates rooms to people in the text file
        '''
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
                    msg += colored(self.add_person(role, first_name,
                                           last_name, accommodation),"green")
        except:
            msg += colored('File does not exist','red')
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
                msg1 += colored("Offices",'green')
                msg1 += colored("\n--------------------------- \n",'green')
                msg1 += colored(office.room_name,'green')
            else:
                msg1 += colored("\nNo offices available\n",'yellow')
        if msg1 == '':
            msg1 += colored("\nNo offices available\n",'yellow')
        msg2 = ''
        living_spaces = self.rooms['living_space']
        for living_space in living_spaces:
            if len(living_space.occupants) < living_space.capacity:
                msg2 += colored("\nLiving Spaces",'green')
                msg2 += colored("\n--------------------------- \n",'green')
                msg2 += colored(living_space.room_name,'green')
            else:
                msg2 += colored("\nNo living spaces available\n",'yellow')
        if msg2 == '':
            msg2 += colored("\nNo living spaces available\n",'yellow')
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
                    msg += colored(room.room_name,'green')
                    msg += colored("\n--------------------------- \n",'green')
                    for person in room.occupants:
                        msg += colored((person.first_name + " " +
                                person.last_name + ","),'green')
                    msg += '\n\n'
            if msg == '':
                return colored('There are no allocations in the room','yellow')
            if filename:
                file = open(filename, 'w')
                file.write(msg)
                file.close()
                msg += colored('\nSuccessfully saved to ' + filename + ' textfile','green')
            return msg
        else:
            return colored("No rooms available for allocations",'yellow')

    def print_unallocated(self, filename=None):
        '''Check if there are people added in the office waiting list
        Prints all people unallocated office
        Checks if there are people in the living psace waiting list
        Prints all people unallocated living space
         '''
        msg = ''
        if len(Amity.office_waiting_list) == 0 and len(Amity.living_space_waiting_list) == 0:
            return colored("\nThere are no unallocated people\n",'yellow')
        else:
            msg += colored("People not allocated to office \n",'green')
            msg += colored("---------------------------\n",'green')
            unallocated_office_space = '\n'.join(str(
                person.person_id) + ' ' + person.first_name + ' ' + person.last_name + '\n' for person in Amity.office_waiting_list)
            msg += colored(unallocated_office_space,'green')
            msg += colored("\nPeople not allocated to living space \n",'green')
            msg += colored("---------------------------\n",'green')
            unallocated_living_space = '\n'.join(str(
                person.person_id) + ' ' + person.first_name + ' ' + person.last_name + '\n' for person in Amity.living_space_waiting_list)
            msg += colored(unallocated_living_space,'green')
            if filename:
                file = open(filename, 'w')
                file.write(unallocated_office_space)
                file.write(unallocated_living_space)
                file.close()
                msg += colored('\n Successfully saved to ' + filename,'green')
        return msg

    def print_all_rooms(self):
        '''Checks if there are offices
        Prints of all offices
        Checks if there are any living spaces
        Prints all living spaces '''
        offices = list(Amity.rooms['office'])
        msg = ''
        if len(offices) > 0:
            msg += colored("OFFICES",'green')
            msg += colored("\n---------------------------\n",'green')
            for office in offices:
                msg += colored(office.room_name + '\n','green')
        else:
            msg += colored("There are no offices\n",'yellow')
        living_spaces = list(self.rooms['living_space'])
        if len(living_spaces) > 0:
            msg += colored("\nLIVING SPACES",'green')
            msg += colored("\n---------------------------\n",'green')
            for living_space in living_spaces:
                msg += colored(living_space.room_name + '\n','green')
        else:
            msg += colored("\nThere are no livingspaces",'yellow')
        return msg

    def print_room(self, room_name):
        """Prints the occupants of the room provided"""
        msg = ''
        all_rooms = self.rooms["office"] + self.rooms["living_space"]
        for room in all_rooms:
            if room_name == room.room_name:
                if len(room.occupants) > 0:
                    for person in room.occupants:
                        msg += colored(str(person.first_name) + ' ' + \
                            person.last_name + '\n','green')
                else:
                    msg += colored("There are no occupants in the room",'yellow')
            else:
                msg += colored("{} does not exist".format(room.room_name),'yellow')
        return msg

    def save_state(self, dbname="amity.db"):
        """
        Creates table called unallocated and saves the ids of unallocated people in office and livingspace waiting list
        Creates a table called rooms that saves all rooms created and occupants id of the rooms
        Creates table people which stores the ids of the people added to the system
        """
        dbname = dbname if dbname else "amity.db"
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()
        curs.execute("""DROP TABLE IF EXISTS unallocated""")
        curs.execute("""CREATE TABLE unallocated
                     (aID INTEGER PRIMARY KEY UNIQUE,
                     office_waiting_list INTEGER, living_space_waiting_list INTEGER)""")
        person = ''
        for person in self.office_waiting_list:
            person = person.person_id
            curs.execute("INSERT INTO unallocated (office_waiting_list,living_space_waiting_list) VALUES (?,?)",
                         (person, 0))
        for person in self.living_space_waiting_list:
            person = person.person_id
            curs.execute("INSERT INTO unallocated (office_waiting_list,living_space_waiting_list) VALUES (?,?)",
                         (0, person))
        curs.execute("""DROP TABLE IF EXISTS people""")
        curs.execute(
            """CREATE TABLE people (person_id INTEGER PRIMARY KEY UNIQUE,name TEXT, role TEXT, accommodation TEXT)""")
        for person in self.people:
            person_id = person.person_id
            name = person.first_name + ' ' + person.last_name
            role = person.role
            accommodation = person.accommodation
            curs.execute("INSERT INTO people (person_id,name,role,accommodation) VALUES (?,?,?,?)",
                         (person_id, name, role, accommodation))
        curs.execute("""DROP TABLE IF EXISTS rooms""")
        curs.execute(
            """CREATE TABLE rooms (pID INTEGER PRIMARY KEY UNIQUE, name TEXT, type TEXT, occupants TEXT)""")
        office_occupants = ''
        for office in self.rooms['office']:
            office_occupants = ''
            office_name = office.room_name
            office_type = "office"
            for person in office.occupants:
                office_occupants += str(person.person_id) + ' '
            curs.execute(
                "INSERT INTO rooms (name,type,occupants) VALUES (?,?,?)", (office_name, office_type, office_occupants))
        for livingspace in self.rooms['living_space']:
            livingspace_occupants = ''
            livingspace_name = livingspace.room_name
            livingspace_type = 'living_space'
            for person in livingspace.occupants:
                livingspace_occupants += str(person.person_id) + ' '
            curs.execute(
                "INSERT INTO rooms (name,type,occupants) VALUES (?,?,?)", (livingspace_name, livingspace_type, livingspace_occupants))
        conn.commit()
        conn.close()
        return colored('Data successfully exported to the Database','green')

    def load_state(self, dbname="amity.db"):
        """
        Fetches all data in unallocated table
        Fetches all data in the people table
        Fetches all data in the rooms table
        """
        dbname = dbname if dbname else "amity.db"
        msg = ''
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()
        curs.execute("SELECT * FROM people")
        people = curs.fetchall()
        self.people = []
        for person in people:
            if person[2] == 'Staff':
                staff = Staff(person[2], person[1].split(
                    ' ')[0], person[1].split(' ')[1], person[3])
                staff.id = person[0]
                self.people.append(staff)
            else:
                fellow = Fellow(person[2], person[1].split(
                    ' ')[0], person[1].split(' ')[1], person[3])
                fellow.id = person[0]
                self.people.append(fellow)

        curs.execute("SELECT * FROM rooms")
        rooms = curs.fetchall()
        for room in rooms:
            if room[2] == 'living_space':
                livingspace = LivingSpace(room[1])
                livingspace_occupants = []
                for occupant in room[3][:-1].split(' '):
                    for person in self.people:
                        if person.id == str(occupant):
                            livingspace_occupants.append(person)
                livingspace.occupants = livingspace_occupants
                self.rooms['living_space'].append(livingspace)
            if room[2] == 'office':
                office = Office(room[1])
                office_occupants = []
                for occupant in room[3][:-1].split(' '):
                    for person in self.people:
                        if person.id == str(occupant):
                            office_occupants.append(person)
                office.occupants = office_occupants
                self.rooms['office'].append(office)
        curs.execute("SELECT * FROM unallocated")
        data = curs.fetchall()
        for ids in data:
            person = None
            for persons in self.people:
                person = None
                if ids[1] == persons.id or ids[2] == persons.id:
                    person = persons
                    if ids[1] > 0 and person is not None:
                        self.office_waiting_list.append(person)
                    if ids[2] > 0 and person is not None:
                        self.living_space_waiting_list.append(person)
                    break
                    conn.close()
        msg += colored('Successfully loaded data from the Database','green')
        return msg
