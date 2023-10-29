import pickle
from os.path import exists
from models.models import AddressBook


FILENAME = "AddressBook.pkl"


def read_from_file() -> AddressBook:
    if exists(FILENAME):
        with open(FILENAME, "rb") as file:
            return pickle.load(file)
    return AddressBook()


def write_to_file(book: AddressBook) -> None:
    with open(FILENAME, "wb") as file:
        pickle.dump(book, file)
