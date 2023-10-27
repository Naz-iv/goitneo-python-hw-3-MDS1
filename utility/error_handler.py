from models.errors import UserNotFoundError


def input_error(func: type) -> type:
    def inner(*args: tuple, **kwargs: dict):
        try:
            return func(*args, **kwargs)
        except UserNotFoundError as e:
            return e
        except ValueError as e:
            return e
        except IndexError:
            return "Name was not provided. Please enter valid name!"
    return inner
