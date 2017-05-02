#!/usr/bin/env python
"""
This is a room allocation system using CLI.

Usage:
    Amity create_room (office|livingspace) <room_name>
    Amity add_person (fellow|staff) <first_name> <last_name> [<accommodation>]
    Amity reallocate_person <person_id> <room_name>
    Amity load_people <filename>
    Amity list_all_people
    Amity print_allocations [-o=filename]
    Amity print_unallocated [-o=filename]
    Amity print_available_rooms
    Amity delete_room <room_name>
    Amity delete_person <person_id>
    Amity print_all_rooms
    Amity allocate_office_waiting_list
    Amity allocate_livingspace_waiting_list
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
import os
from colorama import init
from termcolor import cprint, colored
from pyfiglet import Figlet
from docopt import docopt, DocoptExit
from Models.amity import Amity

init()


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
    font = Figlet(font='isometric3')
    introduction = font.renderText('AMITY')
    os.system('cls')
    cprint(introduction, "blue", attrs=['blink'])
    intro = colored('Welcome to Amity room allocations!'
                    + ' (type help for a list of commands.)', "blue")
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
        cprint(self.amity.create_room(room_type, arg['<room_name>']), "blue")

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person (fellow|staff) <first_name> <last_name> [<accommodation>]"""
        role = None
        if arg["fellow"]:
            role = "fellow"
        elif arg["staff"]:
            role = "staff"
        cprint(self.amity.add_person(
            role, arg['<first_name>'], arg['<last_name>'], arg['<accommodation>']), "blue")

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_id> <room_name>"""
        cprint(self.amity.reallocate_person(
            arg['<person_id>'], arg['<room_name>']), "blue")

    @docopt_cmd
    def do_list_all_people(self, arg):
        """Usage: list_all_people"""
        print(self.amity.list_all_people())

    @docopt_cmd
    def do_delete_room(self, arg):
        """Usage: delete_room <room_name>"""
        cprint(self.amity.delete_room(arg['<room_name>']), "blue")

    @docopt_cmd
    def do_delete_person(self, arg):
        """Usage: delete_person <person_id>"""
        cprint(self.amity.delete_person(arg['<person_id>']), "blue")


    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <filename>"""
        filename = arg['<filename>']
        cprint(self.amity.load_people(filename), "blue")

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]"""
        filename = arg['--o']
        cprint(self.amity.print_allocations(arg['--o']), "blue")

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""
        filename = arg['--o']
        cprint(self.amity.print_unallocated(arg['--o']), "blue")

    @docopt_cmd
    def do_print_person_id(self, arg):
        """ Usage: print_person_id <first_name> <last_name> """
        cprint(self.amity.print_person_id(
            arg['<first_name>'], arg['<last_name>']), "blue")

    @docopt_cmd
    def do_allocate_office_waiting_list(self, arg):
        """Usage: allocate_office_waiting_list"""
        cprint(self.amity.allocate_office_waiting_list(), "blue")

    @docopt_cmd
    def do_allocate_livingspace_waiting_list(self, arg):
        """Usage: allocate_office_waiting_list"""
        cprint(self.amity.allocate_livingspace_waiting_list(), "blue")

    @docopt_cmd
    def do_print_all_rooms(self, arg):
        """Usage: print_all_rooms"""
        cprint(self.amity.print_all_rooms(), "blue")

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_all_rooms <room_name>"""
        room_name = arg['<room_name>']
        cprint(self.amity.print_room(room_name), "blue")

    @docopt_cmd
    def do_print_available_rooms(self, arg):
        """Usage: print_available_rooms"""
        cprint(self.amity.print_available_rooms(), "blue")

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=sqlite_database]"""
        db_name = args['--db']
        cprint(self.amity.save_state(args['--db']), "blue")

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state [--db=sqlite_database]"""
        db_name = args['--db']
        cprint(self.amity.load_state(args['--db']), "blue")

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        cprint('Good Bye!', "blue")
        exit()


if __name__ == '__main__':
    # opt = docopt(__doc__, sys.argv[1:])
    opt = (__doc__)
    cprint(opt, 'blue')
    Amityapp().cmdloop()

# if opt['--interactive']:
