import datetime
from dateutil.relativedelta import relativedelta

class TDate:

	class str:
		def to_date(string):
			return datetime.datetime.strptime(string, '%Y-%m-%d')
        def to_string_nospace(string):
            return TDate.date.to_string_nospace(TDate.str.to_date(string))
	
	class plus:
		def days(date, delta = 1):
			return date + datetime.timedelta(days = delta)
		def months(date, delta = 1):
			return date + relativedelta(months = delta)

	class date:
		def to_string_slash(date):
			return f'{date.year}/{date.month}/{date.day}'

		def to_string_nospace(date):
			return date.strftime('%Y%m%d')




'''
	def str_to_date(string):
		return datetime.datetime.strptime(string, '%Y-%m-%d')

	def date_plus(date, delta = 1):
		return date + datetime.timedelta(days = delta)
	def date_plus_m(date, delta = 1):
		return date + relativedelta(months = delta)

	def date_to_string(date):
		return f'{date.year}/{date.month}/{date.day}'

	def date_no_space(date):
		return date.strftime('%Y%m%d')
'''