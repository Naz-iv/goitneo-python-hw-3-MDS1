from utility.file_handler import read_from_file, write_to_file
from utility.cli_bot import cli_bot


def main() -> None:

    book = read_from_file()
    cli_bot(book)
    write_to_file(book)


if __name__ == "__main__":
    main()
