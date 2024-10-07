from enum import Enum


class STATUSES(Enum):
    proposed = 'Ожидание подтверждения'
    pending = 'Ожидание подтверждения'
    booked = 'Подтверждено'
    arrived = 'Пациент прибыл'
    fulfilled = 'Запись завершена'
    cancelled = 'Запись отменена'
    noshow = 'Пациент не пришел на прием'
    entered_in_error = 'Статус не получен'
    checked_in = 'Пациент в регистратуре'
    waitlist = 'Ожидание доступного времени'


class GENDERS(Enum):
    male = 'М',
    female = 'Ж',
    other = 'Не указан',
    unknown = 'Не указан'
