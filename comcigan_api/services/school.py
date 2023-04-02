from comcigan import AsyncSchool
from comcigan_api.error import SchoolNotFoundError, MultipleSchoolExistsError, UncaughtError
from async_lru import alru_cache

@alru_cache(maxsize=100, ttl=60*60)
async def findSchool(name: str) -> AsyncSchool | SchoolNotFoundError | MultipleSchoolExistsError | UncaughtError:
    try:
        return await AsyncSchool.init(name)
    except Exception as error:
        if isinstance(error, ValueError):
            return MultipleSchoolExistsError(name)
        elif isinstance(error, NameError):
            return SchoolNotFoundError(name)
        else:
            return UncaughtError(error)
        
async def getClasses(school: AsyncSchool):
    grade_len = len(school._week_data)
    result = {}
    for grade in range(1, grade_len+1):
        result[grade] = [f'{grade}-{i}' for i in range(1, len(school._week_data[grade-1]))]
    return result