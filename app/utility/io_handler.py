from models.errors import (
    InvalidBirthdayError,
    InvalidNameError,
    InvalidPhoneError,
    PhoneDontExistError,
    UserNotFoundError
)
from models.models import AddressBook, Record


def io_handler(book: AddressBook) -> None:
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


def parse_input(user_input: str) -> tuple:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def add_contact(book: AddressBook, *args: tuple) -> str:
    try:
        name, phone = args
    except ValueError:
        return "Invalid command format. Add command format: add [name] [phone]"

    try:
        record = Record(name.capitalize())
        record.add_phone(phone)
    except InvalidNameError as e:
        return f"Contact wasn't added. {e}"
    except InvalidPhoneError as e:
        return f"Contact wasn't added. {e}"

    book.add_record(record)
    return "Contact added."


def change_phone(book: AddressBook, *args: tuple) -> str:
    try:
        name, old_phone, new_phone = args
    except ValueError:
        return ("Invalid command format. Change command format:"
                " change [name] [old phone] [new phone]")

    try:
        book.edit_phone(name, old_phone, new_phone)
        return "Contact updated."
    except UserNotFoundError as e:
        return f"Contact wasn't updated. {e}"
    except PhoneDontExistError as e:
        return e
    except InvalidPhoneError as e:
        return f"New phone number is invalid. {e}"


def get_phone(book: AddressBook, *args: tuple) -> int | str:
    try:
        name = args[0]
    except IndexError:
        return "Invalid command format. Correct command format: phone [name]"

    try:
        record = book.find(name.capitalize())
        return " | ".join(str(phone) for phone in record.phones)
    except UserNotFoundError as e:
        return e


def get_all_contacts(book: AddressBook) -> str:
    return "\n".join([str(record) for record in book.values()])


def add_birthday(book: AddressBook, *args: tuple) -> str:
    try:
        name, birthday = args
    except ValueError:
        return ("Invalid command format. Add birthday command "
                "format: add-birthday [name] [birthday]")

    try:
        record = book.find(name.capitalize())
        record.add_birthday(birthday)
        return "Birthday added"
    except InvalidBirthdayError as e:
        return f"Birthday wasn't added. {e}"


def show_birthday(book: AddressBook, *args: tuple) -> str:
    try:
        name = args[0]
    except IndexError:
        return ("Invalid command format. Show birthday command "
                "format: show-birthday [name]")

    try:
        record = book.find(name.capitalize())
        if record.birthday:
            return record.birthday
        return f"{record.name}'s birthday is not in address book!"
    except UserNotFoundError as e:
        return e


def get_all_birthdays(book: AddressBook) -> str:
    bd_this_week = book.birthdays_per_week()
    if bd_this_week:
        return "\n".join(bd_this_week)
    return "No birthdays this week"
