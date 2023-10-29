from utility.file_handler import read_from_file, write_to_file
from utility.io_handler import io_handler


def main() -> None:

    book = read_from_file()
    io_handler(book)
    write_to_file(book)


if __name__ == "__main__":
    main()
