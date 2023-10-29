from models.models import AddressBook
from utility.cli_bot_commands import (
    add_birthday,
    add_contact,
    change_phone,
    get_all_birthdays,
    get_all_contacts,
    get_phone,
    parse_input,
    show_birthday,
)


def cli_bot(book: AddressBook) -> None:
    print("Welcome to the assistant bot!")
    commands = {
        "add": add_contact,
        "change": change_phone,
        "phone": get_phone,
        "all": get_all_contacts,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": get_all_birthdays
    }

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command in commands:
            try:
                print(commands[command](book, *args))
            except Exception as e:
                print(e)
        else:
            print("Invalid command.")
