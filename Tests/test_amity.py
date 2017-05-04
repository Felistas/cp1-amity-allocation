import unittest
from Models.person import Fellow, Staff
from Models.room import LivingSpace, Office
from Models.amity import Amity


class ModelsTest(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()

    def tearDown(self):
        self.amity.rooms = {'living_space': [], 'office': []}
        self.amity.people[:]
        self.amity.office_waiting_list[:]
        self.amity.living_space_waiting_list[:]

    def test_room_exists(self):
        """Asserts tsavo already exists"""
        existing_room = self.amity.create_room("office", ["tsavo"])
        existing_room = self.amity.create_room("office", ["tsavo"])
        self.assertIn('Tsavo already exists', existing_room)

    def test_office_created_successfully(self):
        """Asserts that an office has been successfully been created"""
        new_office = self.amity.create_room("office", ["camelot"])
        self.assertIn("Successfully created Office Camelot",
                      new_office)

    def test_livingspace_created_successfully(self):
        """Asserts livingspace has been successfully been created"""
        new_living_space = self.amity.create_room("livingspace", ["php"])
        self.assertIn("Successfully created Living Space Php",
                      new_living_space)

    def test_cannot_allocate_invalid_roomtype(self):
        """Asserts room type should be livingspace or office"""
        new_room = self.amity.allocate_room('dining')
        self.assertIn('Invalid room type', new_room)

    def test_person_name_cannot_be_integer(self):
        """Asserts person cannot be integer"""
        new_person = self.amity.add_person('fellow', '123', '345')
        self.assertIn('Invalid input', new_person)

    def test_fellow_added_successfully(self):
        """Asserts fellow has been added successfully"""
        new_fellow = self.amity.add_person("fellow", "maryann", "ngumi", "Y")
        self.assertIn("Fellow Maryann Ngumi successfully added", new_fellow)

    def test_fellow_allocated_to_office(self):
        """Asserts that fellow has been allocated an office successfully"""
        self.amity.rooms['office'] = []
        self.amity.create_room("office", ["tsavo"])
        new_fellow = self.amity.add_person("fellow", "alex", "mbugua", "Y")
        self.assertIn("You have been allocated to office Tsavo", new_fellow)

    def test_fellow_allocated_to_living_space(self):
        """Asserts that fellow has been allocated a living space successfully"""
        self.amity.rooms['living_space'] = []
        self.amity.rooms['office'] = []
        self.amity.people = []
        self.amity.create_room("livingspace", ["topaz"])
        #self.amity.create_room("office", ["tsavo"])
        new_fellow = self.amity.add_person("fellow", "alex", "mbugua", "Y")
        self.assertIn("You have been allocated to living space Topaz", new_fellow)

    def test_staff_added_successfully(self):
        """Asserts staff has been added successfully"""
        new_staff = self.amity.add_person("staff", "john", "ngumi")
        self.assertIn("Staff John Ngumi successfully added",
                      new_staff)

    def test_staff_cannot_get_accommodation(self):
        """Asserts staff cannot get accommodation"""
        new_staff = self.amity.add_person("staff", "susan", "ngumi", "Y")
        self.assertIn("Staff cannot get accommodation", new_staff)

    def test_staff_allocated_to_office(self):
        """Asserts that staff has been allocated an office successfully"""
        self.amity.rooms['office'] = []
        self.amity.create_room("office", ["tsavo"])
        new_staff = self.amity.add_person("staff", "thomas", "muchiri", "N")
        self.assertIn("You have been allocated to office Tsavo", new_staff)

    def test_fellow_allocated_to_office_waiting_list_if_no_office(self):
        """Asserts that fellow has been aldded to office waiting list if no office"""
        office = self.amity.rooms['office'] = []
        new_fellow = self.amity.add_person("fellow", "alex", "mbugua", "N")
        self.assertIn("You have been added to office waiting list",
                      new_fellow)

    def test_fellow_allocated_to_living_space_waiting_list_if_no_living_space(self):
        """Asserts that fellow has been added to living space waiting list if no living space"""
        office = self.amity.rooms['office'] = []
        livingspace = self.amity.rooms['living_space'] = []
        new_office = self.amity.create_room("office", ["camelot"])
        new_fellow = self.amity.add_person("fellow", "alex", "mbugua", "Y")
        self.assertIn("You have been added to living space waiting list",
                      new_fellow)

    def test_staff_allocated_to_office_waiting_list_if_no_office(self):
        """Asserts that staff has been added to office waiting list if no office"""
        office = self.amity.rooms['office'] = []
        new_staff = self.amity.add_person("staff", "ken", "olalo")
        self.assertIn("You have been added to office waiting list", new_staff)

    def test_cannot_print_id_of_non_existent_person(self):
        """Asserts that a non existent person cannot have person id"""
        self.amity.people = []
        person = self.amity.print_person_id("ganla", "janla")
        self.assertIn('Person does not exist', person)

    def test_cannot_reallocate_a_non_existent_person(self):
        """Asserts cannot reallocate a person who does not exist"""
        self.amity.people = []
        reallocate_person = self.amity.reallocate_person('1233', 'tsavo')
        self.assertIn('1233 does not exist', reallocate_person)

    def test_cannot_reallocate_person_with_no_room(self):
        """Asserts that one cannot reallocate someone who had no room before"""
        self.amity.rooms['office'] = []
        person = self.amity.add_person("staff", "felistas", "ngumi", "no")
        staff_id = self.amity.print_person_id("felistas", "ngumi").split(' ')
        reallocate_person = self.amity.reallocate_person(staff_id[0], 'tsavo')
        self.assertIn("Felistas had not been allocated a room",
                      reallocate_person)

    def test_cannot_reallocate_staff_to_livingspace(self):
        """Asserts that cannot reallocate staff to livingspace"""
        self.amity.people=[]
        self.amity.rooms['living_space'] = []
        self.amity.rooms['office'] = []
        self.amity.create_room("office", ["narnia"])
        new_living_space = self.amity.create_room("livingspace", ["topaz"])
        staff = self.amity.add_person("staff", "paul", "upendo")
        staff_id = self.amity.print_person_id("paul", "upendo").split(' ')
        reallocate_staff = self.amity.reallocate_person(staff_id[0], 'topaz')
        self.assertIn('Cannot reallocate staff to livingspace',reallocate_staff)

    def test_cannot_reallocate_fellow_to_livingspace(self):
        """Assert cannot reallocate to different room type"""
        self.amity.rooms['living_space'] = []
        self.amity.rooms['office'] = []
        self.amity.people=[]
        self.amity.create_room("office", ["narnia"])
        new_living_space = self.amity.create_room("livingspace", ["php"])
        fellow = self.amity.add_person("fellow", "olivia", "onyango")
        fellow_id = self.amity.print_person_id("olivia", "onyango").split(' ')
        print(fellow_id[0])
        print(self.amity.people[0].person_id)
        reallocate_fellow = self.amity.reallocate_person(fellow_id[0], 'php')
        self.assertIn('Cannot reallocate from one room type to another', reallocate_fellow)

    def test_cannot_reallocate_to_full_room(self):
        """Assert that one cannot be reallocated to a full room"""
        self.amity.rooms['office'] = []
        self.amity.create_room("office", ["narnia"])
        self.amity.add_person("fellow", "oliva", "munala")
        self.amity.add_person("fellow", "batian", "yokozuna")
        self.amity.add_person("fellow", "humphrey", "stick")
        self.amity.add_person("fellow", "sharon", "robley")
        self.amity.add_person("fellow", "joshua", "kamau")
        self.amity.add_person("fellow", "ivan", "pycharm")
        self.amity.create_room("office", ["nairobi"])
        self.amity.add_person("fellow", "gideon", "gandalf")
        fellow_id = self.amity.print_person_id("gideon", "gandalf").split(' ')
        reallocate_fellow = self.amity.reallocate_person(fellow_id[0], 'narnia')
        self.assertIn('Room is full', reallocate_fellow)

    def test_cannot_reallocate_to_same_room(self):
        """Assert that a person cannot be reallocated to the same room"""
        self.amity.rooms['office'] = []
        self.amity.people = []
        self.amity.create_room("office", ["narnia"])
        self.amity.add_person("staff", "ivan", "pycharm")
        fellow_id = self.amity.print_person_id("ivan", "pycharm").split(' ')
        reallocate_fellow = self.amity.reallocate_person(fellow_id[0], 'narnia')
        self.assertIn('Cannot reallocate to the same room', reallocate_fellow)

    def test_reallocate_person_successfully(self):
        """Assert that a person has been successfully reallocated to a room"""
        self.amity.rooms['office'] = []
        self.amity.people = []
        self.amity.create_room("office", ["narnia"])
        self.amity.add_person("fellow", "ivan", "pycharm")
        self.amity.create_room("office", ["meru"])
        fellow_id = self.amity.print_person_id("ivan", "pycharm").split(' ')
        reallocate_fellow = self.amity.reallocate_person(fellow_id[0], 'meru')
        self.assertIn('Successfully reallocated to Meru', reallocate_fellow)

    def test_cannot_reallocate_to_non_existent_room(self):
        """Asserts that cannot reallocate to non existent room"""
        self.amity.people = []
        self.amity.rooms['office'] = []
        self.amity.create_room("office", ["red"])
        self.amity.add_person("fellow", "ivan", "pycharm")
        fellow_id = self.amity.print_person_id("ivan", "pycharm").split(' ')
        reallocate_fellow = self.amity.reallocate_person(fellow_id[0], 'meru')
        self.assertIn('Meru does not exist', reallocate_fellow)

    def test_cannot_allocate_office_waiting_list_if_no_office(self):
        """Assert person in office waiting list cannot be allocated to a room if there is no office available"""
        self.amity.rooms['office'] = []
        self.amity.add_person("fellow", "ivan", "pycharm")
        allocate_office = self.amity.allocate_office_waiting_list()
        self.assertIn('No offices available', allocate_office)


    def test_allocate_office_waiting_list(self):
        """Assert allocated people in office list to an office"""
        self.amity.rooms['office'] = []
        self.amity.office_waiting_list = []
        self.amity.people = []
        self.amity.add_person("staff", "ivan", "pycharm")
        self.amity.create_room("office", ["toll"])
        allocate = self.amity.allocate_office_waiting_list()
        self.assertIn('Ivan Pycharm has been allocted to room Toll', allocate)

    def test_cannot_allocate_people_in_living_space_waiting_list_if_no_living_space(self):
        """Assert person in living space waiting list cannot be allocated to a room if there is no living space"""
        self.amity.rooms['living_space'] = []
        self.amity.add_person("fellow", "ivan", "pycharm")
        allocate_living_space = self.amity.allocate_livingspace_waiting_list()
        self.assertIn('No livingspace available', allocate_living_space)

    def test_allocate_livingspace_waiting_list(self):
        """Assert allocate people in living space list to a living space"""
        self.amity.rooms['living_space'] = []
        self.amity.add_person("fellow", "Felistas", "Ngumi", "yes")
        self.amity.create_room("livingspace", ["php"])
        allocate = self.amity.allocate_livingspace_waiting_list()
        self.assertIn('Felistas Ngumi has been allocted to room Php', allocate)

    def test_delete_office_successfully(self):
        """Asserts that an office can be deleted successfully"""
        self.amity.rooms['office'] = []
        self.amity.create_room("office",["tsavo"])
        deleted_room = self.amity.delete_room("tsavo")
        self.assertIn("Successfully deleted room Tsavo", deleted_room)

    def test_delete_living_space_successfully(self):
        """Asserts that living space can be deleted successfully"""
        self.amity.rooms['living_space'] = []
        self.amity.create_room("livingspace",["blue"])
        deleted_room = self.amity.delete_room("blue")
        self.assertIn("Successfully deleted room Blue", deleted_room)

    def test_cannot_delete_non_existent_room(self):
        """Asserts that one cannot delete an existent room"""
        self.amity.rooms['living_space'] = []
        self.amity.rooms['office'] = []
        deleted_room = self.amity.delete_room("huhu")
        self.assertIn("Room Huhu does not exist", deleted_room)
    def test_delete_person(self):
        """Asserts that a person has been deleted successfully"""
        self.amity.people = []
        self.amity.add_person("fellow", "Felistas", "Ngumi", "yes")
        fellow_id = self.amity.print_person_id("felistas", "ngumi").split(' ')
        delete_person = self.amity.delete_person(fellow_id[0])
        self.assertIn('Successfully deleted Felistas',delete_person)

    def test_cannot_load_people_from_non_existent_file(self):
        """Asserts that one cannot load people from a file that does not exist"""
        load_people = self.amity.load_people('haha')
        self.assertIn('File does not exist', load_people)

    def test_no_available_offices(self):
        """Assert message where there are no rooms"""
        Amity.rooms = {'living_space': [], 'office': []}
        msg = self.amity.print_available_rooms()
        self.assertIn("No offices available", msg)
        self.assertIn("No living spaces available", msg)

    def test_no_occupants(self):
        """Assert message where there are no occupants in the room"""
        self.amity.create_room("office", ["toll"])
        no_occupants = self.amity.print_allocations()
        self.assertIn("There are no allocations in the room", no_occupants)

    def test_assert_successfully_saved_to_text_file(self):
        """Assert successfully saved to text file"""
        self.amity.create_room("livingspace", ["ruiru"])
        self.amity.add_person("fellow", "ivan", "pycharm", "Y")
        room = self.amity.print_allocations("filename")
        self.assertIn("Successfully saved to filename", room)

    def test_no_unallocated_people(self):
        """Assert message that there are no unallocated people"""
        Amity.office_waiting_list = []
        Amity.living_space_waiting_list = []
        unallocated = self.amity.print_unallocated()
        self.assertIn("There are no unallocated people", unallocated)

    def test_print_unallocated_to_office(self):
        """Assert that people without offices are successfully printed"""
        Amity.office_waiting_list = []
        self.amity.add_person("fellow", "ivan", "pycharm")
        unallocated = self.amity.print_unallocated()
        self.assertIn("People not allocated to office", unallocated)

    def test_print_unallocated_to_living_space(self):
        """Assert that people without living space are successfully printed"""
        Amity.living_space_waiting_list = []
        self.amity.add_person("fellow", "ivan", "pycharm", "Y")
        unallocated = self.amity.print_unallocated()
        self.assertIn("People not allocated to living space", unallocated)

    def test_successfully_unallocated_saved_to_text_file(self):
        """Assert message successfully saved to filename"""
        self.amity.living_space_waiting_list = []
        self.amity.office_waiting_list = []
        self.amity.add_person("fellow", "ivan", "pycharm", "Y")
        room = self.amity.print_unallocated("filename")
        self.assertIn("Successfully saved to filename", room)

    def test_load_state_successfully(self):
        """Asserts that load state has been loaded successfully"""
        msg_load_state = self.amity.load_state("amity")
        self.assertIn(
            'Successfully loaded data from the Database', msg_load_state)

    def test_save_test(self):
        """Asserts that state is not saved if not provided database name"""
        msg_save_state = self.amity.save_state("")
        self.assertIn('Save state was Unsuccessfull',
                      msg_save_state)

    def test_save_test(self):
        """Asserts that state is saved successfully"""
        msg_save_state = self.amity.save_state("amity")
        self.assertIn('Data successfully exported to the Database',
                      msg_save_state)


if __name__ == '__main__':
    unittest.main()
