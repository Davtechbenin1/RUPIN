#Coding:utf-8
"""
	Module pour la définition d'une surface pour la
	définition de la date.
"""

try:
	from .davbuild import *
except ImportError:
	from davbuild import *

from color import *

class date_surf(float_l):
	def __init__(self,mother,
		y = int(),m = int(),d = int(),
		title_text_color = GRIS_,
		text_color = TEXT_COL1,**kwargs):
		float_l.__init__(self,mother,**kwargs)
		self.Year = now().year

		self.This_month = now().month
		self.To_day = now().day
		self.This_day = now().day

		if y:
			self.Year = y
		if m:
			self.This_month = m
		if d:
			self.This_day = d

		self.title_text_color = title_text_color
		self.text_color = text_color

		self.Calend_ret = ('m+1','m-1','y+1','y-1')

		self.month_dic = {
			1:"Janvier",
			2:"Février",
			3:"Mars",
			4:"Avril",
			5:"Mai",
			6:"Juin",
			7:"Juiellet",
			8:"Août",
			9:"Septembre",
			10:"Octobre",
			11:"Novembre",
			12:"Décembre",
		}
		self.add_all()

	def Foreign_surf(self):
		self.size_pos()
		self.add_annee()
		self.add_mois()
		self.add_day()

	def size_pos(self):
		self.gene_height = 1/8
		self.Anne_size = 1,self.gene_height
		self.Mois_size = 1,self.gene_height
		self.Grid_size = 1,self.gene_height*6

	def add_annee(self):
		b = box(self,size_hint = self.Anne_size,
			pos_hint = (0,1-self.gene_height),
			orientation = 'horizontal',
			padding = dp(5))
		b.add_button("<",on_press = self.Ret_handler,
			text_color = self.text_color,
			font_size = '20sp',size_hint = (.1,1),
			info = 'y-1',halign = 'center',
			bg_color = self.bg_color,shadow = 10)
		b.add_text(self.Year,size_hint = (.8,1),
			halign = 'center',font_size = "13sp",
			text_color = self.title_text_color,
			)
		b.add_button(">",on_press = self.Ret_handler,
			text_color = self.text_color,
			font_size = '20sp',size_hint = (.1,1),
			info = 'y+1',halign = 'center',
			bg_color = self.bg_color,shadow = 10)
		self.add_surf(b)

	def add_mois(self):

		b = box(self,size_hint = self.Mois_size,
			pos_hint = (0,1-self.gene_height*2),
			orientation = 'horizontal',
			padding = dp(5))
		txt = ""
		info = ""
		shad = 0
		if self.This_month >1:
			txt = "<"
			info = 'm-1'
			shad = 10
		b.add_button(txt,on_press = self.Ret_handler,text_color = self.text_color,
			font_size = '20sp',size_hint = (.1,1),
			info = info,halign = 'center',
			bg_color = self.bg_color,shadow = shad)
		M = self.month_dic[self.This_month] + f' {self.Year}'
		b.add_text(M,size_hint = (.8,1),
			halign = 'center',font_size = "13sp",
			text_color = self.title_text_color,
			)
		txt = ""
		info = ""
		shad = 0
		if self.This_month < 12:
			txt = ">"
			info = 'm+1'
			shad = 10
	
		b.add_button(txt,on_press = self.Ret_handler,text_color = self.text_color,
			font_size = '20sp',size_hint = (.1,1),
			info = info,halign = 'center',
			bg_color = self.bg_color,shadow = shad)
		self.add_surf(b)

	def add_day(self):
		line_dict = Calen().Get_year_month(self.Year,
			self.This_month)
		day_l = 'Lun','Mard','Mer','Jeu','Ven','Sam','Dim'
		day_surf = grid(self,cols = len(day_l),
			size_hint = self.Grid_size,pos_hint = (0,0))
		for d in day_l:
			day_surf.add_text(d,text_color = self.title_text_color,
				halign = 'center',font_size = '13sp')
		for k,line in line_dict.items():
			for date in line:
				day = date.day
				month = date.month
				year = date.year
				info = f"{day}**{month}**{year}"
				txt_col = self.text_color
				bg_color = self.bg_color
				if month == self.This_month:
					if line.index(date)>=5:
						txt_col = self.title_text_color
					if day == self.To_day and month == now().month and year == now().year:
						txt_col = TEXT_COL3
						bg_color = GREEN
					if day == self.This_day:
						txt_col = TEXT_COL4
					
					day_surf.add_button(str,on_press = self.Ret_handler(day),text_color = txt_col,
						font_size = "15sp",bg_color = bg_color,
						halign = 'center',info = info,
						radius = 20)
				else:
					day_surf.add_text(" ",text_color = txt_col,
						font_size = "15sp",bg_color = bg_color,
						halign = 'center')

		self.add_surf(day_surf)

	@classmethod
	def Set_Year(cls,year):
		month = range(1,13)
		Date_liste = list()
		for M in month:
			Date_liste.append(Calen().Get_year_month(year,M))
		return Date_liste

	def Ret_handler(self,wid):
		ret = wid.info
		if ret:
			if ret == 'y+1':
				self.Year += 1
				self.This_month = 1
				self.add_all()
			elif ret == 'y-1':
				self.Year -= 1
				self.This_month = 12
				self.add_all()
			elif ret == 'm+1':
				self.This_month += 1
				self.add_all()
			elif ret == 'm-1':
				self.This_month -= 1
				self.add_all()
			elif '**' in ret:
				day,month,year = ret.split('**')
				self.This_day = int(day)
				self.This_month = int(month)
				self.Year = int(year)
				self.add_all()
				liste = [self.This_day,self.This_month,
				elf.Year]
				self.mother.date_handler(*liste)







