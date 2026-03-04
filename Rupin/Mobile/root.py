#Coding:utf-8
"""
	L'écran principale est un stack
"""
from lib.davbuild import *

from .Prog import *

class root(box):
	from .surf_typ import (clt_part_def,presta_part_def,
		admin_part_def,_set_inf_)

	def initialisation(self):
		self.clear_widgets()
		h = .07
		self.th_email = str()

		ret = self.sc.DB.check_connect()
		if ret:
			self.size_pos()

		else:
			th_b = stack(self,size_hint = (1,1),
				padding = dp(10))
			th_b.add_padd((1,.25))
			th_b.add_text("[size=18sp]Ooooops !!!![/size]\nVous êtes déconnecté d'internet...",
				halign = 'center',size_hint = (1,.2),
				font_size = "14sp",bold = True,
				text_color = self.sc.text_col3)
			th_b.add_padd((.25,h))
			th_b.add_button("Reconnexion",size_hint = (.5,h),
				bg_color = self.sc.aff_col3,
				text_color = self.sc.text_col1,
				on_press = self.relance_con)
			th_b.add_padd((.25,h))
			self.add_surf(th_b)

	def email_part(self):
		self.clear_widgets()
		th_b = stack(self,size_hint = (1,1),
		padding = dp(20),bg_color = self.sc.aff_col3)
		th_b.add_padd(1,.2)
		srf = box(self,size_hint = (1,.3),
			radius = dp(20),bg_color = self.sc.aff_col1,
			padding = dp(10),spacing = dp(1))
		srf.add_text('Email de connexion',size_hint =(1,.14),
			text_color = self.sc.text_col1)
		srf.add_input('email',size_hint = (1,.14),
			bg_color = self.sc.aff_col1,on_focus = true,
			placeholder = "email",on_text = self.set_email)
		srf.add_button("Confirmer",size_hint = (.5,.14),
			pos_hint = (.25,0),bg_color = self.sc.aff_col3,
			text_color = self.sc.text_col3,
			on_press = self.send_email)
		th_b.add_surf(srf)

		self.add_surf(th_b)

	def size_pos(self):

		th_srf = box(self,size_hint = (1,.93))
		self.aff_part = scroll(self,size_hint = (1,1))
		th_srf.add_surf(self.aff_part)

		self.menu_part = box(self,size_hint = (1,.07),
			orientation = 'horizontal')

		self.add_surf(th_srf)
		self.add_surf(self.menu_part)
		self.curent_show = 'Accueil'
		self.sc.curent_interface = "client"

		self._set_inf_()

# Gestion des actions des buttons
	def relance_con(self,wid):
		self.initialisation()

	def change_surf(self,wid):
		info = wid.info
		self._change_surf(info)

	def _change_surf(self,info):
		self.aff_part.clear_widgets()
		self.set_bold_part(info)
		srf = self.surf_def_dic.get(info)
		srf.add_all()

		self.aff_part.add_surf(srf)

	def change_interface(self,wid):
		self.sc.curent_interface = wid.info
		self.curent_show = "Accueil"
		self._set_inf_()

	def set_bold_part(self,info):
		for inf,bt in self.menu_but_obj.items():
			bt.bold = False
			self.menu_icon_obj[inf].color = self.sc.text_col3
		if info in self.menu_but_obj:
			self.menu_but_obj[info].bold = True
			self.menu_icon_obj[info].color = self.sc.text_col1








