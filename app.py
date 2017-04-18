#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.

Usage:
    Amity create_room (office|livingspace) <room_name>
    Amity add_person (fellow|staff) <first_name> <last_name> [<accommodation>]
    Amity reallocate_person <person_id> <room_name>
    Amity load_people
    Amity print_allocations [-o=filename]
    Amity print_unallocated [-o=filename]
    Amity print_available_rooms
    Amity print_all_rooms
    Amity print_person_id <first_name> <last_name>
    Amity print_room <room_name>
    Amity save_state [--db=sqlite_database]
    Amity load_state [--db=sqlite_database]
    Amity print_all_rooms
    Amity (-i | --interactive)
    Amity (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from Models.amity import Amity


def docopt_cmd(func):
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class Amityapp(cmd.Cmd):
    intro = 'Welcome to Amity room allocations!' \
            + ' (type help for a list of commands.)'
    prompt = 'Enter command>> '
    file = None
    amity = Amity()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room (office|livingspace) <room_name>..."""
        room_type = None
        if arg["office"]:
            room_type = "office"
        elif arg["livingspace"]:
            room_type = "livingspace"
        self.amity.create_room(room_type, arg['<room_name>'])

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person (fellow|staff) <first_name> <last_name> [<accommodation>]"""
        role = None
        if arg["fellow"]:
            role = "fellow"
        elif arg["staff"]:
            role = "staff"
        self.amity.add_person(
            role, arg['<first_name>'], arg['<last_name>'], arg['<accommodation>'])

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_id> <room_name>"""
        self.amity.reallocate_person(arg['<person_id>'], arg['<room_name>'])

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]"""
        print(self.amity.print_allocations(arg['--o']))

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""
        print(self.amity.print_unallocated(arg['--o']))

    @docopt_cmd
    def do_print_person_id(self, arg):
        """ Usage: print_person_id <first_name> <last_name> """
        self.amity.print_person_id(arg['<first_name>'], arg['<last_name>'])

    @docopt_cmd
    def do_print_all_rooms(self, arg):
        """Usage: print_all_rooms"""
        self.amity.print_all_rooms()

    @docopt_cmd
    def do_print_available_rooms(self, arg):
        """Usage: print_available_rooms"""
        self.amity.print_available_rooms()

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=sqlite_database]"""
        self.amity.save_state(args['--db'])

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state [--db=sqlite_database]"""
        self.amity.load_state()

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    Amityapp().cmdloop()
    # a = Amity()
    # a.create_room("livingspace", ["block"])
    # for x in range(1, 9):
    #     a.add_person("fellow", "shera" + str(x), "ngumi", 'Y')
    # b = a.print_unallocated()
    # print(b)


print(opt)
