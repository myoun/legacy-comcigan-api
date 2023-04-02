class SchoolNotFoundError(Exception):

    def __init__(self, name) -> None:
        self.name = name
        super().__init__(f"Cannot find school named \"{name}\".")


class MultipleSchoolExistsError(Exception):

    def __init__(self, name) -> None:
        self.name = name
        super().__init__(f"There is more than one school named \"{name}\".")


class UncaughtError(Exception):

    def __init__(self, error: Exception) -> None:
        self.error = error
        super().__init__("Uncaugt error occured.")

class InvalidGradeError(Exception):

    def __init__(self, grade: int) -> None:
        self.grade = grade
        super().__init__(f"Grade must be between 1 and 3, not {grade}.")

class InvalidClassError(Exception):

    def __init__(self, cls: int) -> None:
        self.cls = cls
        super().__init__(f"Cannot find class {cls}")

class InvalidDayError(Exception):

    def __init__(self, day: str) -> None:
        self.day = day
        super().__init__(f"Invalid day {day}.")

def errorAsResponse(error: Exception):
    return {"status":"error", "message":str(error)}