class UserNotFoundError(Exception):
    pass


class FieldError(Exception):
    pass


class InvalidPhoneError(FieldError):
    pass


class InvalidNameError(FieldError):
    pass


class InvalidBirthdayError(FieldError):
    pass


class PhoneDontExistError(FieldError):
    pass
