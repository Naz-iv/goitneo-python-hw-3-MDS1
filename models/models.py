from collections import UserDict, defaultdict
from re import compile, search
from models.errors import UserNotFoundError

from utility.birthdays_per_week_handler import (
    celebration_validator,
    birthdays_reminder_output
)


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: str) -> bool:
        return self.value == other

    def __hash__(self) -> int:
        return super().__hash__()

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__ = state


class Name(Field):
    def __init__(self, value: str) -> None:
        if not value:
            raise ValueError("Name can't be empty")
        super().__init__(value)

    def __rep__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


class Phone(Field):
    def __init__(self, value: str) -> None:
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number should have 10 digits.")
        super().__init__(value)

    def __str__(self) -> str:
        return self.value


class Birthday(Field):
    def __init__(self, value: str) -> None:
        pattern = compile(r'^\d{1,2}\.\d{1,2}\.\d{4}')
        if not search(pattern, value):
            raise ValueError("Birthday shoild be in DD.MM.YYYY format!")
        super().__init__(value)


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.birthday = None
        self.phones = []

    def add_phone(self, phone: str) -> bool:
        try:
            phone = Phone(phone)
            self.phones.append(phone)
            return True
        except ValueError as e:
            print(e)
            return False

    def add_birthday(self, birthday: str) -> bool:
        try:
            self.birthday = Birthday(birthday)
            return True
        except ValueError as e:
            print(e)
            return False

    def remove_phone(self, phone: str) -> bool:
        if phone in self.phones:
            self.phones.remove(phone)
            return True
        print("Phone number is not in contact book.")
        return False

    def edit_phone(self, old_phone: str, new_phone: str) -> bool:
        if old_phone in self.phones:
            self.phones[self.phones.index(old_phone)] = Phone(new_phone)
            return True
        else:
            print("Old phone number is not in contact book.")
            return False

    def find_phone(self, phone: str) -> str | None:
        if phone in self.phones:
            return self.phones[self.phones.index(phone)].value
        return None

    def __str__(self):
        return (f"Contact name: {self.name}, Phones: "
                f"{'; '.join(phone.value for phone in self.phones)}")

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__ = state


class AddressBook(UserDict):

    def add_record(self, record: Record) -> None:
        self.data[record.name] = record

    def find(self, name: str) -> Record | None:
        for key in self.data.keys():
            if key.value == name:
                return self.data[key]
        raise UserNotFoundError(
            f"Contact with name {name} not in Addres Book"
        )

    def delete(self, name: str) -> None:
        for key in self.data.keys():
            if key.value == name:
                self.data.pop(key)
                return
        raise UserNotFoundError(
            f"Contact with name {name} not in Addres Book"
        )

    def birthdays_per_week(self) -> list:
        birthdays_this_week = defaultdict(list)

        for record in self.data.values():
            if record.birthday:
                validate = celebration_validator((
                    record.name,
                    record.birthday.value
                ))
                if validate:
                    day, name = validate
                    birthdays_this_week[day] += [str(name)]
        birthdays_this_week = birthdays_reminder_output(birthdays_this_week)

        if birthdays_this_week:
            return "\n".join(birthdays_this_week)
        return "No birthdays this week"

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__ = state
