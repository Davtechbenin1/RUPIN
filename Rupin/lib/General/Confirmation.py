#Coding:utf-8
"""
	Surface de confirmation
"""
from lib.davbuild import *

class Confirmation_srf(stack):
	font_s = "20sp"
	def add_all(self,conf_metho):
		self.spacing = dp(10)
		#perso_obj = self.sc.DB.Get_this_perso(self.sc.get_curent_perso())
		self.this_pas = "admin" #perso_obj.get('mot de pass')
		self.conf_metho = conf_metho
		
		#self.add_padd((1,.15))
		self.add_text('Entrer votre mot de pass pour continuer',
			text_color = self.sc.text_col1,halign = 'center',
			font_size = self.font_s,size_hint = (1,.4),
			valign = 'bottom')
		
		self.add_padd((.1,.1))
		Get_border_input_surf(self,"password",
			size_hint = (.8,.26),
			text_color = self.sc.text_col1,on_text = self.verif_pass,
			bg_color = self.sc.aff_col1,password = True,
			password_mask = '_*')
		self.add_padd((.1,.1))

	def verif_pass(self,wid,val):
		if val == self.this_pas:
			self.conf_metho()
			self.mother.close_modal()
