#Coding:utf-8
from lib.davbuild import *

"""
	Définition de la surface de recherche avec un input
"""
class input_search_lay(box):
	def __init__(self,mother,text,info,info_list,
		mother_fonc,text_color = tuple(),but_col = tuple(),
		bg_color = tuple(),text_size = tuple(),
		search_wid_size = tuple(),**kwargs):
		kwargs['orientation'] = "horizontal"
		box.__init__(self,mother,**kwargs)
		self.info = info
		self.info_list = info_list
		self.mother_fonc = mother_fonc
		self.text = text

		if not text_color:
			text_color = self.sc.text_col1
		if not but_col:
			but_col = self.sc.aff_col3
		if not bg_color:
			bg_color = self.sc.aff_col1
		if not search_wid_size:
			search_wid_size = (1,.15)
		if not text_size:
			text_size = (.3,1)

		self.search_wid_size = search_wid_size
		self.search_text = str()
		w,h = self.text_size = text_size
		self.inf_size = 1-w,h
		self.text_color = text_color
		self.but_col = but_col
		self.bg_color = bg_color
		self.This_surf = scroll(self,size_hint = self.search_wid_size,
			)
		self.add_all()

	def Foreign_surf(self):
		self.add_part1()

	def add_part1(self):
		self.clear_widgets()
		self.add_text(self.text,text_color = self.text_color,
			size_hint = self.text_size)
		if self.info:
			b = box(self,orientation = "horizontal",
				size_hint = self.inf_size,spacing = dp(10))
			b.add_button('',size_hint = (None,None),bg_opact = 0,
				width = dp(20),height = dp(20),radius = dp(10),
				info = self.info,on_press = self.modif_info,
				bg_color = self.text_color,pos_hint = (0,.2))
			b.add_button(self.info,info = self.info,
				on_press = self.modif_info,bg_color = None,
				text_color = self.text_color,bg_opact = 0,
				halign = 'left')
			self.add_surf(b)
		else:
			self.add_input("Search",bg_color = self.but_col,
			text_color = self.text_color,on_text = self.modif_search,
			size_hint = self.inf_size,default_text = self.search_text,
			placeholder = "Recherche")
			self.add_part2()

	def add_part2(self):
		self.This_surf.clear_widgets()
		h = dp(20)
		liste = [i for i in self.info_list if self.search_text.lower() in i.lower()]
		H = len(liste) * (h+dp(10))
		st_w = stack(self,size_hint = (1,None),height = H,
			spacing = dp(10),padding = dp(5))
		for info in liste:
			b = box(self,orientation = 'horizontal',
				size_hint = (1,None),height = h,spacing = dp(10))
			b.add_button('',size_hint = (None,None),
				height = dp(20),width = dp(20),
				bg_color = self.but_col,on_press = self.modif_info,
				info = info,bg_opact = 0)
			b.add_button(info,bg_color = None,bg_opact = 0,
				text_color = self.text_color,on_press = self.modif_info,
				info = info,
				halign = 'left')
			st_w.add_surf(b)
		self.This_surf.add_surf(st_w)

# Méthodes de gestion des actions au niveau des buttons
	def modif_info(self,wid):
		if self.info:
			self.info = str()
			self.mother.add_surf(self.This_surf)
		else:
			self.info = wid.info
			#try:
			self.mother.remove_widget(self.This_surf)
			
		self.mother_fonc(wid)
		self.add_part1()

	def modif_search(self,wid,val):
		self.search_text = val
		self.add_part2()

from .liste_deroulante import liste_deroulante
class input_search_lay_new(stack):
	def __init__(self,mother,info,info_list,
		mother_fonc,text_color = tuple(),
		but_col = tuple(),inp_size = (1,.15),
		mult = 6,sub_mod = 1,
		bg_color = tuple(),text_size = tuple(),
		search_wid_size = tuple(),**kwargs):
		kwargs['spacing'] = dp(10)
		stack.__init__(self,mother,**kwargs)
		self.info = info
		self.sub_mod = sub_mod
		self.info_list = info_list
		self.mother_fonc = mother_fonc
		self.mult = mult

		if not text_color:
			text_color = self.sc.text_col1
		if not but_col:
			but_col = self.sc.aff_col3
		if not bg_color:
			bg_color = self.sc.aff_col1
		if not search_wid_size:
			search_wid_size = (1,.1)
		if not text_size:
			text_size = (1,1)

		w,h = search_wid_size
		self.inp_size = inp_size

		self.search_wid_size = search_wid_size
		self.search_text = str()
		w,h = self.text_size = text_size
		self.inf_size = 1-w,h
		self.text_color = text_color
		self.but_col = but_col
		self.bg_color = bg_color
		self.add_all()

	def Foreign_surf(self):
		self.clear_widgets()
		if not self.info:
			self.add_input("Search",bg_color = self.sc.aff_col3,
				text_color = self.sc.text_col1,
				on_text = self.add_search_txt,
				size_hint = self.inp_size,
				placeholder = 'Recherche',
				width = dp(350),
				default_text = self.search_text)
		liste = [i for i in self.info_list 
			if self.search_text.lower() in i.lower()]
		self.liste_obj = liste_deroulante(self,self.info,liste,
			size_hint = self.search_wid_size,
			orientation = 'V',mult = self.mult,
			mother_fonc = self.up_infos,
			sub_mod = self.sub_mod)
		self.add_surf(self.liste_obj)

	def add_second(self):
		liste = [i for i in self.info_list 
			if self.search_text.lower() in i.lower()]
		self.liste_obj.list_info = liste
		self.liste_obj.add_all()

# Méthode de gestion des actions
	def up_infos(self,info):
		if self.info:
			self.info = str()
		else:
			self.info = info
		self.mother_fonc(info)
		self.add_all()

	def add_search_txt(self,wid,val):
		self.search_text = val
		self.add_second()

class input_search_new(input_search_lay_new):
	def __init__(self,mother,info,info_list,
		mother_fonc,size_hint = (1,.05),mult = 6,
		sub_mod = 1,**kwargs):
		kwargs['spacing'] = dp(10)
		w,h = size_hint
		kwargs["size_hint"] = size_hint
		padd = 1-w,h
		stack.__init__(self,mother,**kwargs)
		self.SH = size_hint
		self.info = info
		self.sub_mod = sub_mod
		self.info_list = info_list
		self.mother_fonc = mother_fonc
		self.mult = mult
		self.liste_obj = liste_deroulante(self,self.info,
			self.info_list,
			size_hint = size_hint,
			orientation = 'V',mult = self.mult,
			mother_fonc = self.up_infos,
			sub_mod = self.sub_mod)
		self.mother.add_surf(self)
		self.mother.add_padd(padd)
		self.mother.add_surf(self.liste_obj)
		self.search_text = str()
		self.add_all()

	def Foreign_surf(self):
		self.clear_widgets()
		if not self.info:
			self.size_hint = self.SH[0],self.SH[1]
			self.add_input("Search",bg_color = self.sc.aff_col3,
				text_color = self.sc.text_col1,
				on_text = self.add_search_txt,
				placeholder = 'Recherche',
				width = dp(350),
				default_text = self.search_text)
		else:
			#self.size_hint = self.SH[0],.0002
			self.add_input("Search",bg_color = self.sc.aff_col3,
				text_color = self.sc.text_col1,
				on_text = self.add_search_txt,
				placeholder = 'Recherche',
				width = dp(350),
				default_text = self.search_text)

	def up_infos(self,info):
		if self.info:
			self.info = str()
		else:
			self.info = info
			self.search_text = info
		#self.add_all()
		self.mother_fonc(info)


