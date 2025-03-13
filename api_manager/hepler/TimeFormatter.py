import time

from datetime import datetime


class TimeConverter:
    @staticmethod
    def sec_to_date(sec: int, shift:int=None) -> datetime:
        mk_time_format = time.mktime(time.gmtime(sec)) if not shift else time.mktime(time.gmtime(sec + shift))   # shift depends on the crypto platform
        datetime_format = datetime.fromtimestamp(mk_time_format)

        return datetime_format

    @staticmethod
    def date_to_sec(date: str, shift:int=None) -> int:
        date_format = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        to_sec = time.mktime(date_format.timetuple())
        result = int(to_sec) if not shift else int(to_sec) + shift

        return result

    @staticmethod
    def get_now_in_sec():
        return round(time.time())

    @staticmethod
    def get_now():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
