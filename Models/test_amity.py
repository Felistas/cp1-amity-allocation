import unittest
from person import Person,Fellow,Staff
from room import Room,LivingSpace,Office
from amity import Amity

class ModelsTest(unittest.TestCase):
    def setUp(self):
            self.amity = Amity()
            self.person = Person("felistas","ngumi")
            self.fellow = Fellow("shera","ann")
            self.staff = Staff("john","ngumi")
            self.room = Room("lion")
            self.office = Office("tsavo")
            self.livingspace = LivingSpace("oculus")
    def test_fellow_inherits_person(self):
        """ Checks if class Fellow inherits class Person"""
        self.assertTrue(issubclass(Fellow,Person))

    def test_staff_inherits_Person(self):
        """Checks if class Staff Inherits class Person"""
        self.assertTrue(issubclass(Staff,Person))

    def test_livingspace_inherits_room(self):
        """ Checks if class LivingSpace inherits class Room"""
        self.assertTrue(issubclass(LivingSpace,Room))

    def test_office_inherits_room(self):
        """Checks if class Office Inherits class Room"""
        self.assertTrue(issubclass(Office,Room))

    def test_room_exists(self):
        """Asserts tsavo exists in rooms"""
        self.assertEqual("tsavo",self.office.room_name,msg='The room already exists')

    def test_office_created_successfully(self):
        """Asserts that an office has been successfully been created"""
        msg_room = self.amity.create_room("state","office")
        self.assertEqual(msg_room,"Created room successfully")

    def test_livingspace_created_successfully(self):
        """Asserts that livingspace has been successfully been created"""
        msg_room = self.amity.create_room("tsavo","livingspace")
        self.assertEqual(msg_room,"Created room successfully")

    def test_fellow_added_successfully(self):
        """Asserts that the fellow has been added successfully"""
        msg_fellow = self.amity.add_person("shera","fellow","Y")
        self.assertEqual(msg_fellow,"Added person successfully")

    def test_staff_added_successfully(self):
        """Asserts that the staff has been added successfully in the system"""
        msg_staff = self.amity.add_person("wambui","staff","N")
        self.assertEqual(msg_staff,"Added person successfully")

    def test_add_staff_who_wants_accommodation(self):
        """Assert that staff cannot get accommodation"""
        msg_staff = self.amity.add_person("wambui","staff","Y")
        self.assertEqual(msg_staff,"Staff cannot get accommodation")

    def test_staff_allocated_officespace(self):
        """Asserts that staff has been allocated office space"""
        msg_staff = self.amity.add_person("staff","tsavo","N")
        msg_staff = self.assertEqual(self.amity.add_person,"Staff has been allocated office")

    def test_fellow_allocated_office_and_livingspace(self):
        """"Asserts that fellow has been allocated livingspace and office"""
        msg_fellow = self.amity.add_person("shera","tsavo","oculus")
        msg_fellow = self.assertEqual(self.amity.add_person,"Fellow has been allocated office and livingspace")

    def test_reallocate_person(self):
        """Asserts that person has been reallocated successfully"""
        msg_reallocate = self.amity.reallocate_person('shera','state')
        msg_reallocate = self.assertEqual(msg_reallocate,"Reallocated person successfully")

    def test_reallocate_to_ghost_room(self):
        """Asserts that one cannot allocate a non-existent room"""
        msg_reallocate = self.amity.reallocate_person('shera','camelot')
        msg_reallocate = self.assertEqual(msg_reallocate,"Room does not exist")

    def test_reallocate_to_full_room(self):
        """Asserts that a person cannot be reallocated to a full room"""
        msg_reallocate = self.amity.reallocate_person('shera','tsavo')
        msg_reallocate = self.assertEqual(msg_reallocate,"No space available")

    def test_cannot_reallocate_same_room(self):
        """Asserts that a person cannot be reallocated in the same room"""
        msg_reallocate = self.amity.reallocate_person("shera","tsavo")
        msg_reallocate = self.assertEqual(msg_reallocate,"Cannot reallocate a person in the same room")

    def test_cannot_reallocate_staff(self):
        """Asserts that a staff cannot be reallocated from office to livingspace"""
        msg_reallocate = self.amity.reallocate_person("john","oculus")
        msg_reallocate = self.assertEqual(msg_reallocate,"Staff cannot be reallocated to livingspace")

    def test_print_allocated_rooms(self):
        """Asserts that allocated rooms are printed"""
        msg_allocations = self.amity.allocations
        self.assertTrue(msg_allocations,"List of allocated rooms")

    def test_print_unallocated_rooms(self):
        """Asserts that unallocated rooms are printed"""
        msg_unallocated = self.amity.print_unallocated
        self.assertEqual(msg_unallocated,"List of unallocated rooms")

    def test_print_all_rooms(self):
        """Asserts that a list of all rooms are printed"""
        msg_all_rooms = self.amity.print_room
        self.assertEqual(msg_all_rooms,"List of all rooms available")

    def test_save_test(self):
        """Asserts that state is saved"""
        msg_save_state = self.amity.save_state
        self.assertTrue(msg_save_state,"State saved successfully")

    def test_load_people(self):
        """Asserts that loads people is successfull"""
        msg_load_state = self.amity.load_state
        self.assertTrue(msg_load_state,"Load successfull")




if __name__ == '__main__':
    unittest.main()
