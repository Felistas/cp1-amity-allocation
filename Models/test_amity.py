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

    def test_cannot_reallocate_a_non_existent_person(self):
        """Asserts cannot reallocate a person who does not exist"""
        reallocate_person = self.amity.reallocate_person('1233', 'tsavo')
        self.assertIn('1233 does not exist', reallocate_person,
                      msg='1233 does not exist')

    def test_cannot_reallocate_staff_to_livingspace(self):
        """Asserts that cannot reallocate staff to livingspace"""
        reallocate_staff = self.amity.reallocate_person('4543212', '[topaz]')
        self.assertIn('Cannot reallocate staff to livingspace',
                      reallocate_staff, msg='Cannot reallocate staff to livingspace')

    # def test_fellow_gets_an_office(self):
    #     """Asserts fellow has been allocated a room successfully"""
    #     new_fellow = self.amity.add_person("fellow", "maryann", "ngumi", "Y")
    #     self.assertIn("FELLOW MARYANN NGUMI successfully added",
    #                   new_fellow, msg='FELLOW MARYANN NGUMI successfully added')
    #

        #
    # def test_add_staff_who_wants_accommodation(self):
    #     """Assert that staff cannot get accommodation"""
    #     msg_staff = self.amity.add_person("wambui", "staff", "Y")
    #     self.assertEqual(msg_staff, "Staff cannot get accommodation")
    #
    # def test_staff_allocated_officespace(self):
    #     """Asserts that staff has been allocated office space"""
    #     msg_staff = self.amity.add_person("staff", "tsavo", "N")
    #     msg_staff = self.assertEqual(
    #         self.amity.add_person, "Staff has been allocated office")
    #
    # def test_fellow_allocated_office_and_livingspace(self):
    #     """"Asserts that fellow has been allocated livingspace and office"""
    #     msg_fellow = self.amity.add_person("shera", "tsavo", "oculus")
    #     msg_fellow = self.assertEqual(
    #         self.amity.add_person, "Fellow has been allocated office and livingspace")
    #
    # def test_reallocate_person(self):
    #     """Asserts that person has been reallocated successfully"""
    #     msg_reallocate = self.amity.reallocate_person('001', 'state')
    #     msg_reallocate = self.assertEqual(
    #         msg_reallocate, "Reallocated person successfully")
    #
    # def test_reallocate_to_ghost_room(self):
    #     """Asserts that one cannot allocate a non-existent room"""
    #     msg_reallocate = self.amity.reallocate_person('001', 'camelot')
    #     msg_reallocate = self.assertEqual(msg_reallocate, "Room does not exist")
    #
    # def test_reallocate_to_full_room(self):
    #     """Asserts that a person cannot be reallocated to a full room"""
    #     msg_reallocate = self.amity.reallocate_person('001', 'tsavo')
    #     msg_reallocate = self.assertEqual(msg_reallocate, "No space available")
    #
    # def test_cannot_reallocate_same_room(self):
    #     """Asserts that a person cannot be reallocated in the same room"""
    #     msg_reallocate = self.amity.reallocate_person("001", "tsavo")
    #     msg_reallocate = self.assertEqual(
    #         msg_reallocate, "Cannot reallocate a person in the same room")
    #
    # def test_cannot_reallocate_staff(self):
    #     """Asserts that a staff cannot be reallocated from office to livingspace"""
    #     msg_reallocate = self.amity.reallocate_person("002", "oculus")
    #     msg_reallocate = self.assertEqual(
    #         msg_reallocate, "Staff cannot be reallocated to livingspace")
    #
    # def test_print_allocated_rooms(self):
    #     """Asserts that allocated rooms are printed"""
    #     msg_allocations = self.amity.print_allocation
    #     self.assertTrue(msg_allocations, "List of allocated rooms")
    #
    # def test_print_unallocated_rooms(self):
    #     """Asserts that unallocated rooms are printed"""
    #     msg_unallocated = self.amity.print_unallocated
    #     self.assertEqual(msg_unallocated, "List of unallocated rooms")
    #
    # def test_print_all_rooms(self):
    #     """Asserts that a list of all rooms are printed"""
    #     msg_all_rooms = self.amity.print_room
    #     self.assertEqual(msg_all_rooms, "List of all rooms available")
    #

    def test_save_test(self):
        """Asserts that state is not saved if not provided database name"""
        msg_save_state = self.amity.save_state("")
        self.assertIn('Save state was Unsuccessfull',
                      msg_save_state, "Save state was Unsuccessfull")

    def test_save_test(self):
        """Asserts that state is saved successfully"""
        msg_save_state = self.amity.save_state("amity")
        self.assertIn('Data successfully exported to the Database',
                      msg_save_state, "Data successfully exported to the Database")

    # def test_load_state(self):
    #     """Assert that load state was done successfully"""
    #     msg_load_state = self.amity.load_state("amity")
    #     self.assertTrue('Successfully loaded data from the Database',
    #                     msg_load_state)
    #
    # def test_load_people(self):
    #     """Asserts that loads people is successfull"""
    #     msg_load_state = self.amity.load_state
    #     self.assertTrue(msg_load_state, "Load successfull")
    def tearDown(self):
        Amity.rooms = {'living_space': [], 'office': []}
        Amity.people = []
        Amity.office_waiting_list = []
        Amity.living_space_waiting_list = []


if __name__ == '__main__':
    unittest.main()
