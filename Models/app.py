#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.

Usage:
    Amity create_room <room_name> <room_type>
    Amity add_person <person_name> <FELLOW|STAFF> [wants_accommodation]
    Amity reallocate_person <person_identifier> <new_room_name>
    Amity load_people
    Amity print_allocations [-o=filename]
    Amity print_unallocated [-o=filename]
    Amity print_room <room_name>
    Amity save_state [--db=sqlite_database]
    Amity load_state <sqlite_database>
    Amity (-i | --interactive)
    Amity (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from amity import Amity


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


class Amityapp (cmd.Cmd):
    intro = 'Welcome to Amity room allocations!' \
        + ' (type help for a list of commands.)'
    prompt = 'Enter command>> '
    file = None
    amity = Amity()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>..."""
        self.amity.create_room(arg['<room_type>'],arg['<room_name>'])

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <person_name> <FELLOW|STAFF> [wants_accommodation]"""

        print(arg)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    Amityapp().cmdloop()

print(opt)
