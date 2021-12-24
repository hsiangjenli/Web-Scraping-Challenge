import datetime
from dateutil.relativedelta import relativedelta

class TDate:

    class str:
        def toDate(string):
            return datetime.datetime.strptime(string, '%Y-%m-%d')
        def withNospace(string):
            return TDate.date.toStringNospace(TDate.str.toDate(string))
	
    class plus:
        def days(date, delta = 1):
            return date + datetime.timedelta(days = delta)
        def months(date, delta = 1):
            return date + relativedelta(months = delta)

    class date:
        def toStringwithSlash(date):
            return f'{date.year}/{date.month}/{date.day}'

        def toStringNospace(date):
            return date.strftime('%Y%m%d')
        def toStringwithDash(date):
            return date.strftime('%Y-%m-%d')