import unittest
from Models.person import Fellow, Staff
from Models.room import LivingSpace, Office
from Models.amity import Amity


class ModelsTest(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        self.amity.add_person("fellow", "Felistas", "Ngumi", "Yes")
        self.amity.add_person("staff", "Oliver", "Munala", "No")
        self.amity.create_room("office", ["tsavo"])
        self.amity.create_room("livingspace", ["topaz"])
        self.amity.reallocate_person("4464093224", "camelot")

    def test_room_exists(self):
        """Asserts tsavo already exists"""
        existing_room = self.amity.create_room("office", ["tsavo"])
        self.assertIn('tsavo already exists', existing_room)

    def test_office_created_successfully(self):
        """Asserts that an office has been successfully been created"""
        new_office = self.amity.create_room("office", ["camelot"])
        self.assertIn("Successfully created Office camelot",
                      new_office)

    def test_livingspace_created_successfully(self):
        """Asserts livingspace has been successfully been created"""
        new_living_space = self.amity.create_room("livingspace", ["php"])
        self.assertIn("Successfully created Living Space php",
                      new_living_space)

    def test_cannot_allocate_invalid_roomtype(self):
        """Asserts room type should be livingspace or office"""
        new_room = self.amity.allocate_room('dining')
        self.assertEqual('Invalid room type', new_room)

    def test_person_name_cannot_be_integer(self):
        """Asserts person cannot be integer"""
        new_person = self.amity.add_person('fellow', '123', '345')
        self.assertIn('Invalid input', new_person)

    def test_fellow_added_successfully(self):
        """Asserts fellow has been added successfully"""
        new_fellow = self.amity.add_person("fellow", "maryann", "ngumi", "Y")
        self.assertIn("FELLOW MARYANN NGUMI successfully added",
                      new_fellow)

    def test_fellow_allocated_to_office(self):
        """Asserts that fellow has been allocated a office successfully"""
        new_fellow = self.amity.add_person("fellow", "alex", "mbugua", "Y")
        self.assertIn("You have been allocated to office tsavo",
                      new_fellow,)

    def test_fellow_allocated_to_living_space(self):
        """Asserts that fellow has been allocated a living space successfully"""
        new_fellow = self.amity.add_person("fellow", "alex", "mbugua", "Y")
        self.assertIn("You have been allocated to living space topaz",
                      new_fellow,)

    def test_staff_added_successfully(self):
        """Asserts staff has been added successfully"""
        new_staff = self.amity.add_person("staff", "john", "ngumi")
        self.assertIn("STAFF JOHN NGUMI successfully added",
                      new_staff, msg='STAFF JOHN NGUMI successfully added')

    def test_staff_cannot_get_accommodation(self):
        """Asserts staff cannot get accommodation"""
        new_staff = self.amity.add_person("staff", "susan", "ngumi", "Y")
        self.assertIn("Staff cannot get accommodation",
                      new_staff, msg='Staff cannot get accommodation"')

    def test_staff_allocated_to_office(self):
        """Asserts that staff has been allocated a office successfully"""
        new_staff = self.amity.add_person("staff", "thomas", "muchiri", "N")
        self.assertIn("You have been allocated to office tsavo",
                      new_staff)

    def test_fellow_allocated_to_office_waiting_list_if_no_office(self):
        """Asserts that fellow has been aldded to office waiting list"""
        office = self.amity.rooms['office'] = []
        new_fellow = self.amity.add_person("fellow", "alex", "mbugua", "Y")
        self.assertIn("You have been added to office waiting list",
                      new_fellow)

    def test_fellow_allocated_to_living_space_waiting_list_if_no_living_space(self):
        """Asserts that fellow has been added to living space waiting list"""
        livingspace = self.amity.rooms['living_space'] = []
        new_fellow = self.amity.add_person("fellow", "alex", "mbugua", "Y")
        self.assertIn("You have been added to living space waiting list",
                      new_fellow)

    def test_staff_allocated_to_office_waiting_list_if_no_office(self):
        """Asserts that staff has been added to office waiting list"""
        office = self.amity.rooms['office'] = []
        new_staff = self.amity.add_person("staff", "ken", "olalo")
        self.assertIn("You have been added to office waiting list", new_staff)

    def test_cannot_print_id_of_non_existent_person(self):
        """Asserts that a non existent person cannot have person id"""
        person = self.amity.print_person_id("ganla", "janla")
        self.assertEqual('Person does not exist', person)

    def test_cannot_reallocate_a_non_existent_person(self):
        """Asserts cannot reallocate a person who does not exist"""
        reallocate_person = self.amity.reallocate_person('1233', 'tsavo')
        self.assertIn('1233 does not exist', reallocate_person)

    def test_cannot_reallocate_staff_to_livingspace(self):
        """Asserts that cannot reallocate staff to livingspace"""
        staff = self.amity.add_person("staff", "paul", "upendo")
        staff_id = self.amity.print_person_id("paul", "upendo").split(' ')
        reallocate_staff = self.amity.reallocate_person(staff_id[0], 'topaz')
        self.assertIn('Cannot reallocate staff to livingspace',
                      reallocate_staff)

    def test_cannot_reallocate_fellow_to_livingspace(self):
        """Assert cannot reallocate to different room type"""
        self.amity.rooms['living_space'] = []
        fellow = self.amity.add_person("fellow", "olivia", "onyango")
        new_living_space = self.amity.create_room("livingspace", ["php"])
        staff_id = self.amity.print_person_id("olivia", "onyango").split(' ')
        reallocate_fellow = self.amity.reallocate_person(staff_id[0], 'php')
        self.assertIn(
            'Cannot reallocate from one room type to another', reallocate_fellow)

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
        self.amity.create_room("office", ["narnia"])
        self.amity.add_person("fellow", "ivan", "pycharm")
        fellow_id = self.amity.print_person_id("ivan", "pycharm").split(' ')
        reallocate_fellow = self.amity.reallocate_person(fellow_id[0], 'narnia')
        self.assertIn('Cannot reallocate to the same room', reallocate_fellow)

    def test_reallocate_person_successfully(self):
        """Assert that a person has been successfully reallocated to a room"""
        self.amity.rooms['office'] = []
        self.amity.create_room("office", ["narnia"])
        self.amity.add_person("fellow", "ivan", "pycharm")
        self.amity.create_room("office", ["meru"])
        fellow_id = self.amity.print_person_id("ivan", "pycharm").split(' ')
        reallocate_fellow = self.amity.reallocate_person(fellow_id[0], 'meru')
        self.assertIn('Successfully reallocated to meru', reallocate_fellow)

    def test_cannot_allocate_office_waiting_list_if_no_office(self):
        """Assert person in office list cannot be allocated to a room if there is no office available"""
        self.amity.rooms['office'] = []
        self.amity.add_person("fellow", "ivan", "pycharm")
        allocate_office = self.amity.allocate_office_waiting_list()
        self.assertIn('No office available', allocate_office)

    def test_allocate_office_waiting_list(self):
        """Assert alloated people in office list to an office"""
        self.amity.rooms['office'] = []
        self.amity.add_person("fellow", "ivan", "pycharm")
        self.amity.create_room("office", ["toll"])
        allocate = self.amity.allocate_office_waiting_list()
        self.assertIn('You have been allocted to room toll', allocate)

    def test_cannot_allocate_people_in_living_space_waiting_list_if_no_living_space(self):
        """Assert person in living space waiting list cannot be allocated to a room if there is no living space"""
        self.amity.rooms['living_space'] = []
        self.amity.add_person("fellow", "ivan", "pycharm")
        allocate_living_space = self.amity.allocate_livingspace_waiting_list()
        self.assertIn('No livingspace available', allocate_living_space)

    def test_allocate_living_space_waiting_list(self):
        """Assert allocate people in living space waiting list successfully"""
        self.amity.rooms['living_space'] = []
        self.amity.add_person("fellow", "ivan", "pycharm")
        self.amity.create_room("livingspace", ["ruiru"])
        allocate = self.amity.allocate_livingspace_waiting_list()
        self.assertIn('You have been allocted to room ruiru', allocate)

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
        self.assertIn("There are no allocations", no_occupants)

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

    def tearDown(self):
        Amity.rooms = {'living_space': [], 'office': []}
        Amity.people = []
        Amity.office_waiting_list = []
        Amity.living_space_waiting_list = []


if __name__ == '__main__':
    unittest.main()
