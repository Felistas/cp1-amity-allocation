class Person(object):
    """Creates the super class Person that defines the common attributes for the other classes"""

    def __init__(self, role, first_name, last_name, accommodation):
        self.person_id = id(self)
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.accommodation = accommodation


class Fellow(Person):
    """Creates class Fellow that overides the Person class"""

    def __init__(self, role, first_name, last_name, accommodation):
        super(Fellow, self).__init__(role, first_name, last_name, accommodation)


class Staff(Person):
    """Creates class Staff that overides the Person class"""

    def __init__(self, role, first_name, last_name, accommodation):
        super(Staff, self).__init__(role, first_name, last_name, accommodation)
