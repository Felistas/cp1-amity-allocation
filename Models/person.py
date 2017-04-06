class Person(object):
    def __init__(self, first_name, last_name):
        self.person_id = id(self)
        self.first_name = first_name
        self.last_name = last_name

class Fellow(Person):
    role = "fellow"
    wants_accomodation = "N"
    def __init__(self, first_name, last_name):
        super(Fellow, self).__init__(first_name, last_name)

class Staff(Person):
    role = "staff"
    def __init__(self, first_name, last_name):
        super(Staff, self).__init__(first_name, last_name)