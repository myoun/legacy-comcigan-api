from fastapi import APIRouter
from comcigan_api.error import InvalidDayError, InvalidClassError, InvalidGradeError, SchoolNotFoundError, MultipleSchoolExistsError, UncaughtError, errorAsResponse
from comcigan_api.services.school import findSchool, getClasses
from comcigan import AsyncSchool

router = APIRouter(prefix="/schools")

FindSchoolType = AsyncSchool | SchoolNotFoundError | MultipleSchoolExistsError | UncaughtError
day_map = {0 : "mon", 1 : "tue", 2: "wed", 3: "thu", 4: "fri", "mon" : 0, "tue" : 1, "wed" : 2, "thu" : 3, "fri" : 4}

@router.get("/{name}")
async def getSchool(name: str):
    school: FindSchoolType = await findSchool(name)

    if isinstance(school, AsyncSchool):
        return {"name": school.name,"data":school._week_data}
    else:
        return errorAsResponse(school)
    
@router.get("/{name}/classes")
async def getSchoolClasses(name: str):
    school: FindSchoolType = await findSchool(name)

    if isinstance(school, AsyncSchool):
        classes = await getClasses(school)
        return {"name": school.name, "data": classes}
    else:
        return errorAsResponse(school)

@router.get("/{name}/{grade}")
async def getSchoolGrade(name: str, grade: int):
    # 학년 확인
    if not (grade >= 1 and grade <= 3):
        return errorAsResponse(InvalidGradeError(grade))
    
    school: FindSchoolType = await findSchool(name)

    if isinstance(school, AsyncSchool):
        try:
            return {"name": school.name, "grade": grade, "data": school._week_data[grade-1]}
        except IndexError as error:
            return errorAsResponse(error)
        except Exception as error:
            return errorAsResponse(UncaughtError(error))
    else:
        return errorAsResponse(school)
    
@router.get("/{name}/{grade}/{cls}")
async def getSchoolGradeClass(name: str, grade: int, cls: int):    
    school: FindSchoolType = await findSchool(name)
    if isinstance(school, AsyncSchool):
        try:
            return {"name": school.name, "grade": grade, "class": cls, "data": school._week_data[grade-1][cls-1]}
        except IndexError as error:
            return errorAsResponse(InvalidClassError(cls))
        except Exception as error:
            return errorAsResponse(UncaughtError(error))
    else:
        return errorAsResponse(school)
    
@router.get("/{name}/{grade}/{cls}/{day}")
async def getSchoolGradeClassDay(name: str, grade: int, cls: int, day: str):
    try:
        number = int(day)
    except ValueError as ve:
        try:
            number = day_map[day]
        except KeyError as ke:
            return errorAsResponse(InvalidDayError(day))
        except Exception as error:
            return errorAsResponse(UncaughtError(error))
    except Exception as error:
        return errorAsResponse(UncaughtError(error))

    school: FindSchoolType = await findSchool(name)
    if isinstance(school, AsyncSchool):
        try:
            return {"name": school.name, "grade": grade, "class": cls, "day" : day_map[number], "data": school._week_data[grade-1][cls][number]}
        except IndexError as error:
            return errorAsResponse(InvalidClassError(cls))
        except Exception as error:
            return errorAsResponse(UncaughtError(error))
    else:
        return errorAsResponse(school)

@router.get("/{name}/{grade}/{cls}/{day}/{period}")
async def getSchoolGradeClassDayPeriod(name: str, grade:int, cls: int, day:str, period: int):
    try:
        number = int(day)
    except ValueError as ve:
        try:
            number = day_map[day]
        except KeyError as ke:
            return errorAsResponse(InvalidDayError(day))
        except Exception as error:
            return errorAsResponse(UncaughtError(error))
    except Exception as error:
        return errorAsResponse(UncaughtError(error))

    school: FindSchoolType = await findSchool(name)
    if isinstance(school, AsyncSchool):
        try:
            return {"name": school.name, "grade": grade, "class": cls, "day" : day_map[number], "period" : period, "data": school._week_data[grade-1][cls][number][period-1]}
        except Exception as error:
            return errorAsResponse(UncaughtError(error))
    else:
        return errorAsResponse(school)