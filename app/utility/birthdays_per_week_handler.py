from datetime import datetime


SYSTEM_DATE = datetime.today().date()


def days_of_the_week_orderd_from_current() -> list:

    days_of_week = ["Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday"]

    current_day_index = SYSTEM_DATE.weekday()

    return [days_of_week[(current_day_index + i) % 7] for i in range(7)]


def birthdays_reminder_output(birthdays_data: dict, ) -> list:

    days_ordered = days_of_the_week_orderd_from_current()
    bd_odered = []
    for day in days_ordered:
        celebrating = birthdays_data.get(day)
        if celebrating:
            bd_odered.append(f"{day}: {', '.join(celebrating)}")
    return bd_odered


def celebration_validator(record: tuple) -> tuple | None:
    name, birthday = record
    birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
    birthday_this_year = birthday.replace(year=SYSTEM_DATE.year)
    delta_days = (birthday_this_year - SYSTEM_DATE).days

    if birthday_this_year < SYSTEM_DATE:
        birthday_this_year = birthday.replace(year=SYSTEM_DATE.year + 1)

    if abs(delta_days) > 7:
        return None

    day_of_the_week = datetime.strftime(birthday_this_year, "%A")

    if day_of_the_week == "Saturday":
        if delta_days + 2 < 7:
            return "Monday", name
        return None

    if day_of_the_week == "Sunday":
        if delta_days + 1 < 7:
            return "Monday", name
        return None
    return day_of_the_week, name
