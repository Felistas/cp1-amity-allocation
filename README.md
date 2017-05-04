# Cp1-amity-allocation
Python program to allocate rooms in Andela

**Constraints**

Amity has rooms which can be offices or living spaces. An office can accommodate a maximum of 6 people. A living space can accommodate a maximum of 4 people.

A person to be allocated could be a fellow or staff. Staff cannot be allocated living spaces. Fellows have a choice to choose a living space or not.

This system will be used to automatically allocate spaces to people at random.

The following are links as to how the app works

https://asciinema.org/a/2ljg2cndv4qyjmqyyfj76p2z1

https://asciinema.org/a/bbe2am9rxevy2ij64sdv871ai

https://asciinema.org/a/6i43f00ai9j9jp24jl7v7h4dw

https://asciinema.org/a/dkn2cozub1nkqfntlabssghfd

**Installation**

git clone `https://github.com/Felistas/cp1-amity-allocation`

`cd cp1-amity-allocation`

Activate virtual environment 

`workon venv` if you are using virtual environment wrapper 

or 
`virtualenv --python=python3 amity-venv` 

`source amity-venv/bin/activate`

Run the `pip install -r requirements.txt` to install all the dependancies needed

Launch the app

`python app.py`

Run the app with the following commands
```    Amity create_room (office|livingspace) <room_name>
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
   

