import pickle
from os.path import exists
from models.models import AddressBook


def read_from_file() -> AddressBook:
    filename = "AddressBook.pkl"
    if exists(filename):
        with open(filename, "rb") as file:
            return pickle.load(file)
    return AddressBook()


def write_to_file(book: AddressBook) -> None:
    filename = "AddressBook.pkl"
    with open(filename, "wb") as file:
        pickle.dump(book, file)
