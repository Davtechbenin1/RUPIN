#Coding:utf-8
from datetime import datetime
import calendar
now = datetime.now
import sys
# This object is just for handling the date and hour

def get_year_weeks():
	"""
		Cette fonction permet d'obtenir les semaines de l'années en cours
		sous forme de dictionnaire. 
		la clé est le numéro de la semaine et la valeur représente le 
		premier jour de la semaine et le dernier jour.
	"""
	liste = list()
	for month in range(1,13):
		for i in calendar.Calendar().itermonthdates(now().year,month):
			tup = (i.day,i.month,i.year)
			if tup not in liste:
				liste.append(tup)
	L_arrange = liste
	dic = dict()
	a = 0
	L = list()
	u = 1
	for tup in L_arrange:
		if a == 7:
			dic[u] = L
			u += 1
			a = 0
			L = list()
		L.append(tup)
		a+=1
	dic[u] = L
	F_dic = dict()
	for i in dic:
		tup = dic[i]
		ind1 = tup[0][0]
		ind2 = tup[-1][0]
		ind = f'{ind1}-{ind2}/{tup[0][1]}-{tup[-1][1]}/{tup[0][-1]}-{tup[-1][-1]}'
		F_dic[i] = ind
	return F_dic

def get_curent_week():
	dic = get_year_weeks()

	day = now().day
	month = now().month
	year = now().year
	for key in dic:
		ind = dic[key]
		days,months,years = ind.split('/')
		d1,d2 = days.split('-')
		m1,m2 = months.split('-')
		y1,y2 = years.split('-')
		if year in (int(y1),int(y2)):
			if month in (int(m1),int(m2)):
				#print(d1,day,d2)
				if int(d1) <= day <= int(d2):
					#print(key)
					#sys.exit()
					return key
				
			elif month+1 in (int(m1),int(m2)):
				return key

def Correct_date(d,m,y):
	d,m,y = int(d),int(m),int(y)
	if d == 0:
		m -= 1
		if m == 0:
			y -= 1
			m = 12
		for date in calendar.Calendar().itermonthdates(y,m):
			if date.month == m:
				d = date.day
		return (d,m,y)
	elif d < 0:
		m -= 1
		if m == 0:
			y -= 1
			m = 12
		for date in calendar.Calendar().itermonthdates(y,m):
			if date.month == m:
				d_ = date.day
		d_+=d
		if d_ < 0:
			return Correct_date(d_,m,y)
		else:
			return(d_,m,y)
	else:
		for date in calendar.Calendar().itermonthdates(y,m):
			if date.month == m:
				d_ = date.day
		if d_ < d:
			m += 1
			if m > 12:
				y += 1
				m = 1
			d -= d_
			for date in calendar.Calendar().itermonthdates(y,m):
				if date.month == m:
					d_ = date.day
			if d_ < d:
				return Correct_date(d,m,y)
			else:
				return (d,m,y)
		else:
			return (d,m,y)

def date_gt(date1,date2):
	date1 = Correct_date(*date1.split('/'))
	date2 = Correct_date(*date2.split('/'))
	d1,m1,y1 = date1.split('/')
	d1,m1,y1 = int(d1),int(m1),int(y1)

	d2,m2,y2 = date2.split('/')
	d2,m2,y2 = int(d2),int(m2),int(y2)

	if y1 > y2:
		return True
	elif y1 == y2:
		if m1 > m2:
			return True
		elif m1 == m2:
			if d1 > d2:
				return True
			elif d1 == d2:
				return 0
			else:
				return False
		else:
			return False
	else:
		return False

def Correct_month(m,y):
	if m < 0:
		y -= 1
		m += 12
		if m < 0:
			return Correct_month(m,y)
		else:
			return (m,y)
	elif m > 12:
		y += 1
		m -= 12
		if m > 12:
			return Correct_month(m,y)
		else:
			return (m,y)
	else:
		return (m,y)

class Calen:
	def __init__(self):
		self.Cal = calendar.Calendar()

	#@classmethod
	def Get_year_month(self,year,month):
		liste = list(self.Cal.itermonthdates(year,month))
		line_dict = dict()
		a = 1
		for i in range(0,len(liste),7):
			line = liste[i:i+7]
			#line = [dat.day for dat in line]
			line_dict[a] = line
			a += 1
		return line_dict
# This functions are used in the defining of a full time programs 
	@classmethod
	def date_format(cls,day,month,year):
		forma = f"{day}/{month}/{year}"
		if not day:
			forma = f"{month}/{year}"
		if not month:
			forma = f"{year}"
		return forma

	@classmethod
	def this_day(cls):
		d,m,y = now().day, now().month, now().year
		f = Calendar.date_format(d,m,y)
		return f

	@classmethod
	def to_day(cls):
		return now().day

	@classmethod
	def next_day(cls):
		d,m,y = now().day, now().month, now().year
		f = Calendar.date_format(d+1,m,y)
		return f

	@classmethod
	def three_day(cls):
		d,m,y = now().day, now().month, now().year
		f = Calendar.date_format(d+2,m,y)
		return f

	@classmethod
	def this_month(cls):
		d,m,y = '', now().month, now().year
		f = Calendar.date_format(d,m,y)
		return f

	@classmethod
	def next_month(cls):
		d,m,y = '', now().month, now().year
		f = Calendar.date_format(d,m+1,y)
		return f

	@classmethod
	def three_month(cls):
		d,m,y = '', now().month, now().year
		f = Calendar.date_format(d,m+2,y)
		return f
	
	@classmethod
	def this_year(cls):
		d,m,y = '', '', now().year
		f = Calendar.date_format(d,m,y)
		return f

	@classmethod
	def next_year(cls):
		d,m,y = '', '', now().year
		f = Calendar.date_format(d,m,y+1)
		return f

	@classmethod
	def three_year(cls):
		d,m,y = '', '', now().year
		f = Calendar.date_format(d,m,y+2)
		return f
	
# To define notifications method
	def date(self,d,m,y):
		liste = list(self.Cal.itermonthdays2(y,m))
		day_list = ('Lun.','Mard.','Mer.','Jeu.','Ven.','Sam.','Dim.')
		month_list = ('Jan.','Fev.','Mar.','Avr.','Mai','Juin.','Juie.',
			'Août','Sep.','Oct.','Nov.','Dec.')
		day_dic = {i:j for i,j in zip(self.Cal.iterweekdays(),day_list)}
		# this dic associate the number and the string of the day.
		for tup in liste:
			if d == tup[0]:
				to_day = tup[1]
		h = now().hour
		mi = now().minute
		s = now().second

		if h < 10:
			h = f'0{h}'
		if mi < 10:
			mi = f'0{mi}'
		if s < 10:
			s = f'0{s}'
		if d < 10:
			d = f'0{d}'
		if m < 10:
			m = f'0{m}'

		if int(d) == 1:
			d = '1er'

		to_day = f"{day_dic[to_day]} {d} {month_list[int(m)-1]} {y}"
		return to_day

	def date_m(self,m,y):
		d = now().day
		liste = list(self.Cal.itermonthdays2(y,m))
		day_list = ('Lun.','Mard.','Mer.','Jeu.','Ven.','Sam.','Dim.')
		month_list = ('Jan.','Fev.','Mar.','Avr.','Mai','Juin.','Juie.',
			'Août','Sep.','Oct.','Nov.','Dec.')
		day_dic = {i:j for i,j in zip(self.Cal.iterweekdays(),day_list)}
		# this dic associate the number and the string of the day.
		for tup in liste:
			if d == tup[0]:
				to_day = tup[1]
		h = now().hour
		mi = now().minute
		s = now().second

		if h < 10:
			h = f'0{h}'
		if mi < 10:
			mi = f'0{mi}'
		if s < 10:
			s = f'0{s}'
		if d < 10:
			d = f'0{d}'
		if m < 10:
			m = f'0{m}'

		to_day = f"{month_list[int(m)-1]} {y}"
		return to_day
