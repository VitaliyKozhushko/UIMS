from enum import Enum


class STATUSES(Enum):
    PROPOSED = 'Ожидание подтверждения'
    PENDING = 'В работе'
    BOOKED = 'Подтверждено'
    ARRIVED = 'Пациент прибыл'
    FULFILLED = 'Запись завершена'
    CANCELLED = 'Запись отменена'
    NOSHOW = 'Пациент не пришел на прием'
    ENTERED_IN_ERROR = 'Статус не получен'
    CHECKED_IN = 'Пациент в регистратуре'
    WAITLIST = 'Ожидание доступного времени'


class GENDERS(Enum):
    MALE = 'М'
    FEMALE = 'Ж'
    OTHER = 'Не указан'
    UNKNOWN = 'Не известен'
