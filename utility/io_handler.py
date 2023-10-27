from models.models import AddressBook, Record
from utility.error_handler import input_error


def io_handler(book: AddressBook) -> None:
    print("Welcome to the assistant bot!")
    commands = {
        "add": add_contact,
        "change": change_phone,
        "phone": get_phone,
        "all": get_all_contacts,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": get_all_birthdays,
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
            print(commands[command](book, *args))
        else:
            print("Invalid command.")


@input_error
def parse_input(user_input: str) -> tuple:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(book: AddressBook, *args: tuple) -> str:
    name, phone = args
    record = Record(name.capitalize())
    if record.add_phone(phone):
        book.add_record(record)
        return "Contact added."
    return "Contact was not added."


@input_error
def change_phone(book: AddressBook, *args: tuple) -> str:
    name, old_phone, new_phone = args
    record = book.find(name.capitalize())
    if record.edit_phone(old_phone, new_phone):
        return "Contact updated."
    return "Contact was not updated."


@input_error
def get_phone(book: AddressBook, *args: tuple) -> int | str:
    name = args[0]
    record = book.find(name.capitalize())
    return " | ".join(str(phone) for phone in record.phones)


def get_all_contacts(book: AddressBook) -> str:
    return "\n".join([str(record) for record in book.values()])


@input_error
def add_birthday(book: AddressBook, *args: tuple) -> str:
    name, birthday = args
    record = book.find(name.capitalize())
    if record.add_birthday(birthday):
        return "Birthday added"
    return "Birthday wasn't added"


@input_error
def show_birthday(book: AddressBook, *args: tuple) -> str:
    name = args[0]
    record = book.find(name.capitalize())
    return record.birthday


@input_error
def get_all_birthdays(book: AddressBook) -> str:
    return book.birthdays_per_week()
