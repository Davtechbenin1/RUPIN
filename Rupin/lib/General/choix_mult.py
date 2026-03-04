#Coding:utf-8
"""
	Définition de liste set qui vas permettre de faire le choix
	d'une information parmie plusieurs
"""
from lib.davbuild import *

class liste_choice(scroll):
	def __init__(self,mother,info_l,list_info,
		mother_fonc = None,
		**kwargs):
		"""
			Orientation est soit V ou H

			mother_fonc accepte une paramètre obligatoire,
			celle de l'info retourné par le button
		"""
		scroll.__init__(self,mother,**kwargs)
		self.mother_fonc = mother_fonc
		self.info_l = info_l
		if not list_info:
			list_info = list()
		self.list_info = list_info
		if type(self.list_info) == dict:
			self.list_info = [i for i in self.list_info]
		self.list_info.sort()
		self.normal_height = self.size_hint[1]
		self.normal_width = self.size_hint[0]
		self.add_all()

	def Foreign_surf(self):
		self.clear_widgets()
		h = dp(25)
		H = len(self.list_info) * (h + dp(10))
		H += dp(10)
		st_w = stack(self,size_hint = (1,None),height = H,
			spacing = dp(5),padding = dp(10))
		for inf in self.list_info:
			bg_col = self.sc.aff_col3
			txt_col = self.sc.text_col1
			if inf in self.info_l:
				bg_col = self.sc.aff_col2
				txt_col = self.sc.aff_col2
			b = box(self,size_hint = (1,None),height = h,
				orientation = 'horizontal',spacing = dp(4))
			b.add_button('',size_hint = (None,None),
				height = h,width = h,radius = dp(20),
				bg_color = bg_col,info = inf,
				on_press = self.seting_info)
			b.add_button(inf,text_color = txt_col,
				bg_color = None,halign = 'left',
				info = inf,on_press = self.seting_info)
			st_w.add_surf(b)
		self.add_surf(st_w)

# Gestion des actions des buttons
	def seting_info(self,wid):
		info = wid.info
		if info in self.info_l:
			self.info_l.remove(info)
		else:
			self.info_l.append(info)
		self.add_all()
		if self.mother_fonc:
			self.mother_fonc(self.info_l)

