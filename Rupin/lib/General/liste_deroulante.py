#Coding:utf-8
"""
	Définition de liste déroulante
	ici, on part du principe
	dict = {
		keys:[inf1,inf2,...,infn]
	}
"""
from lib.davbuild import *

class liste_deroulante(box):
	def __init__(self,mother,info,list_info,
		orientation = "V",but_col1 = tuple(),
		txt_col1 = tuple(),but_col2 = tuple(),
		txt_col2 = tuple(),mother_fonc = None,
		taille_scroll_h = dp(35),taille_scroll_w = dp(110),
		mult = 1,readonly = False,sub_mod = 1,**kwargs):
		"""
			Orientation est soit V ou H

			mother_fonc accepte une paramètre obligatoire,
			celle de l'info retourné par le button
		"""
		kwargs['orientation'] = 'horizontal'
		kwargs['spacing'] = dp(5)
		box.__init__(self,mother,**kwargs)
		self.readonly = readonly
		
		if not but_col1:
			but_col1 = self.sc.aff_col3
		if not but_col2:
			but_col2 = self.sc.aff_col2
		if not txt_col1:
			txt_col1 = self.sc.green
		if not txt_col2:
			txt_col2 = self.sc.text_col3
		self.taille_scroll_h = taille_scroll_h
		self.taille_scroll_w = taille_scroll_w
		self.sub_mod = sub_mod

		self.but_col1 = but_col1
		self.but_col2 = but_col2
		self.txt_col1 = txt_col1
		self.txt_col2 = txt_col2
		self.mother_fonc = mother_fonc
		self.mult = mult

		
		self.orient = orientation
		self.info = info
		if not list_info:
			list_info = list()
		self.list_info = self.normal_list(list_info)
		self.normal_height = self.size_hint[1]
		self.normal_width = self.size_hint[0]
		self.inf_but_srfs = dict()
		
		self.add_all()

	def normal_list(self,liste):
		liste = [i for i in liste if i]
		if len(liste) > 20:
			liste = liste[:20]
		return liste

	def Foreign_surf(self,*args):
		self.inf_but_srfs = dict()
		self.clear_widgets()
		
		sc_surf = scroll(self,)
		self.size_hint = self.size_hint[0],self.normal_height*self.mult
		h = self.taille_scroll_h
		H = len(self.list_info)*(h+dp(5))
		st_w = grid(self,cols = 2 * self.sub_mod,spacing = dp(3),
			size_hint = (1,None),height = H)
		for info in self.normal_list(self.list_info):
			this_w = len(info)*dp(10)
			if this_w < 50:
				this_w = 50

			th_srf = st_w.add_icon_but(icon = "radiobox-marked",
				size_hint = (None,None),size = (dp(35),h),
				text_color = self.sc.sep,on_press = self.seting_info)
		
			st_w.add_button(info.lower(),info = info,bg_opact = 0,
				bg_color = None,text_color = self.txt_col1,
				size_hint = (1,None),height = h,
				on_press = self.seting_info,
				halign = 'left',padding_left = dp(5))
			self.inf_but_srfs[info] = th_srf
		
		sc_surf.add_surf(st_w)
		self.add_surf(sc_surf)
		self.up_th_but_srf_but()

	def up_th_but_srf_but(self):
		if self.info:
			for srf in self.inf_but_srfs.values():
				srf.color = self.sc.sep
			srf = self.inf_but_srfs.get(self.info)
			if srf:
				srf.color = self.sc.text_col3

# Gestion des actions des buttons
	def seting_info(self,wid):
		if not self.readonly:
			self.info = wid.info
			self
			#self.add_all()
			self.up_th_but_srf_but()
			Clock.schedule_once(self.set_th_inf)

	def set_th_inf(self,*args):
		if self.mother_fonc:
			self.mother_fonc(self.info)
