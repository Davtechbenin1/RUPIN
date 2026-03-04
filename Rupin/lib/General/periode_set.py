#Coding:utf-8
'''
	Objet de gestion de la date
'''
from lib.davbuild import *

try:
	from .date_handler import calcule_date
	from .liste_set import *
except ImportError:
	from date_handler import calcule_date
	from liste_set import *

def Get_year_month(year,month):
	Cal = calendar.Calendar()
	liste = list(Cal.itermonthdates(year,month))
	line_dict = dict()
	a = 1
	for i in range(0,len(liste),7):
		line = liste[i:i+7]
		line_dict[a] = line
		a += 1
	return line_dict

	
class Periode_set(box):
	def __init__(self,mother,
		input_color = None,info = "Période : ",
		info_w = .2,space = dp(5),
		sep_w = .08,modal_size = (1,.5),
		modal_pos = (0,.45),
		date_key = '',
		exc_fonc = None,one_part = False,
		date_dict = dict(),readonly = False,**kwargs):
		kwargs['orientation'] = 'horizontal'
		kwargs['spacing'] = space
		box.__init__(self,mother,**kwargs)
		self.exc_fonc = exc_fonc

		self.drop_down = modal_list(auto_width = False,width = dp(350),
			bg_color = self.sc.aff_col1)
		if date_dict:
			self.date_dict = date_dict
		else:
			self.date_dict = {
				"day1":self.mother.day1,
				"day2":self.mother.day2
			}
		self.modal_size = modal_size
		self.modal_pos = modal_pos

		if not date_key:
			date_key = 'day1'
		self.readonly = readonly
		self.date_key = date_key

		self.info = info
		self.info_w = info_w
		self.sep_w = sep_w
		self.but_w = (1-(self.info_w - self.sep_w))/2
		self.one_part = one_part
		self.input_color = self.sc.aff_col3
		self.but_srf_dic = {}
		if input_color:
			self.input_color = input_color
		self.set_days()

	def set_days(self):
		self.add_text(self.info,text_color = self.sc.text_col1,
			size_hint = (self.info_w,1))
		if self.one_part:
			self.but_srf_dic[self.date_key] = self.add_button(self.date_dict[self.date_key],
				text_color = self.sc.text_col1,bg_color = self.input_color,
				on_release = self.set_days_info,bold = True,
				info = self.date_key,size_hint = (self.but_w,1))
		else:
			self.but_srf_dic["day1"] = self.add_button(self.date_dict['day1'],
				text_color = self.sc.text_col1,bg_color = self.input_color,
				on_release = self.set_days_info,bold = True,
				info = "day1",size_hint = (self.but_w,1))
			self.add_text('--',text_color = self.sc.sep,halign = 'center',
				size_hint = (self.sep_w,1))
			self.but_srf_dic["day2"] = self.add_button(self.date_dict['day2'],
				text_color = self.sc.text_col1,	bg_color = self.input_color,
				on_release = self.set_days_info,bold = True,
				info = "day2",size_hint = (self.but_w,1))

# Gestion des actions des bouttons
	def set_days_info(self,wid):
		if not self.one_part:
			self.key = wid.info
			butt = self.but_srf_dic.get(self.key)
		else:
			self.key = self.date_key
			butt = self.but_srf_dic.get(wid.info)
		srf = my_calendar(self,bg_color = self.sc.aff_col1,
			size_hint = (1,1),radius = dp(10))

		b = box(self,size_hint = (1,None),height = dp(300),
			padding = dp(1),radius = dp(10),bg_color = self.sc.black)

		srf.add_all()

		b.add_surf(srf)

		self.drop_down.clear_widgets()
		self.drop_down.add_widget(b)
		
		self.drop_down.open(butt)
		"""
		self.sc.add_modal_surf(srf,size_hint = self.modal_size,
			titre = 'Calendrier',pos_hint = {"x":self.modal_pos[0],
			"y":self.modal_pos[1]})
		"""

class my_calendar(box):
	def initialisation(self):
		self.key = self.mother.key
		self.date_dict = self.mother.date_dict
		self.key_date = self.mother.date_dict.get(self.key)
		d,m,y = self.key_date.split('-')
		self.year = int(y)
		self.month = int(m)
		self.day = int(d)
		self.this_year = datetime.now().year

		self.mounth_dic = {
			1:"Janvier",
			2:"Février",
			3:"Mars",
			4:"Avril",
			5:"Mai",
			6:"Juin",
			7:"Juillet",
			8:"Août",
			9:"Septembre",
			10:"Octobre",
			11:"Novembre",
			12:"Décembre",
		}
		self.size_pos()

	def Foreign_surf(self):
		self.add_year_and_mounth()
		self.add_days_obj()

	def size_pos(self):
		self.year_and_mounth = box(self,size_hint = (1,None),
			height = dp(30),orientation = 'horizontal',
			padding = [dp(10),0,dp(10),0])

		self.days_obj = box(self,padding = dp(10),
			spacing = dp(10))

		self.add_surf(self.year_and_mounth)
		self.add_surf(self.days_obj)

	def add_year_and_mounth(self):
		self.year_and_mounth.clear_widgets()

		mont = self.mounth_dic.get(self.month)
		self.year_and_mounth.add_surf(liste_set(self,str(mont),
			self.mounth_dic.values(),mother_fonc = self.set_month,
			add_null_text = False))

		self.year_and_mounth.add_surf(liste_set(self,str(self.year),
			sorted((range(2000,self.this_year+1)),reverse = True),
			mother_fonc = self.set_year,add_null_text = False))

	def add_days_obj(self):
		self.days_obj.clear_widgets()
		line1 = ["Lun","Mar",'Mer','Jeu','Ven','Sam','Dim']
		b = box(self,orientation = 'horizontal',spacing = dp(10))
		for i in line1:
			txt_col = self.sc.black
			if i in ('Sam','Dim'):
				txt_col = self.sc.green
			b.add_text(i,text_color = txt_col,halign = 'center',
				)
		self.days_obj.add_surf(b)
		self.days_obj.add_text('',size_hint = (1,None),
			height = dp(1),bg_color = self.sc.sep)

		th_dic = Get_year_month(self.year,self.month)
		begin = False
		for line in th_dic.values():
			b = box(self,orientation = 'horizontal',spacing = dp(10))
			a = 0
			for date in line:
				a += 1
				txt_col = self.sc.black
				bg_col = self.sc.aff_col3
				if a > 5:
					txt_col = self.sc.green
				day = date.day
				if f"{day}-{self.month}-{self.year}" == self.sc.get_today():
					txt_col = self.sc.orange
				if f"{day}-{self.month}-{self.year}" == self.mother.date_dict.get(self.key):
					bg_col = self.sc.sep

				if begin == False:
					if day == 1:
						begin = True
					else:
						day = str()
				elif begin:
					if day in range(20,32):
						begin = None
				elif begin == None:
					if day < 20:
						day = str()

				if day:
					b.add_button(str(day),text_color = txt_col,
						radius = dp(20),bg_color = bg_col,
						on_press = self.set_day)
				else:
					b.add_text(day)
			self.days_obj.add_surf(b)

# Gestion des actions des buttons
	def set_year(self,info):
		self.year = int(info)
		self.add_days_obj()

	def set_month(self,info):
		key = [key for key,val in self.mounth_dic.items() 
			if val.lower() == info.lower()]
		if key:
			self.month = key[0]
		self.add_days_obj()

	def set_day(self,wid):
		day = f"{self.redo_str(wid.info)}-{self.redo_str(self.month)}-{self.year}"
		self.mother.date_dict[self.key] = day
		if self.key == 'day1':
			self.mother.mother.day1 = day
		elif self.key == 'day2':
			self.mother.mother.day2 = day
		srf = self.mother.but_srf_dic[self.key]
		srf.text = day
		if self.mother.exc_fonc:
			self.mother.exc_fonc()
		self.mother.drop_down.dismiss()

	def redo_str(self,val):
		if len(str(val)) == 1:
			return "0"+str(val)
		else:
			return str(val)

