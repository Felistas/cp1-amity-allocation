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
        self.assertIn("Office camelot successfully created",
                      new_office)

    def test_livingspace_created_successfully(self):
        """Asserts livingspace has been successfully been created"""
        new_living_space = self.amity.create_room("livingspace", ["php"])
        self.assertIn("Living Space php successfully created",
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
