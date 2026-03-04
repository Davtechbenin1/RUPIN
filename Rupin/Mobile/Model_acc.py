#Coding:utf-8
"""
	Modèle de l'accueil de chaque partie
"""

from lib.davbuild import *
from General_surf import *

class Model_acc(stack):
	@Cache_error
	def initialisation(self):
		self.size_pos()

		self.padding = dp(15)
		self.spacing = dp(15)
		self.but_dic = dict()
		self.icon_dic = dict()
		self.my_info_dict = dict()
		self.titre = str()
		self.y_label = list()
		self.data_dict = dict()
		self.cols = list()
		self.th_padd = 1
		self.t = time.time()
		#self.add_image('media/accueil.png',keep_ratio = False,
		#	size_hint = (.97,.97),pos_hint = (.015,.015))
		#self.All_surf = scroll(self,
		#	size_hint = (1,1),
		#	padding = dp(20),spacing = dp(30))
		#self.th_but_surf = stack(self,size_hint = (1,1),
		#	padding = dp(20),spacing = dp(20),
		#	radius = self.radius)

		#self.All_surf.add_surf(self.th_but_surf)
		#self.add_surf(self.th_but_surf)
		
		self.mult = 0

	def Set_but_icon_info(self):
		...

	def size_pos(self):
		self.part_size = (.33,.15)

	@Cache_error
	def Foreign_surf(self,*args):
		self.Set_but_icon_info()
		self.add_part_button()
		#self.excecute(self.add_part_button)

	def add_part_button(self):
		self.clear_widgets()

		th_l = [i for i in self.but_dic.keys()]

		for k in th_l:
			self._add_part_of(k)

	def _add_part_of(self,key,*args):
		if key:
			icon,col = self.icon_dic.get(key)
			lenf = self.my_info_dict.get(key)
			
			b_col = self.sc.aff_col3
			txt_col = self.sc.text_col1
			B = box(self,bg_color = b_col,padding = dp(5),
				radius = dp(20),size_hint = (.5,.2))
			B.add_icon_but(icon = icon,#size_hint = (None,1),
				text_color = col,#size = (dp(30),dp(1)),
				font_size = "20sp",info = key,
				on_press = self.set_foreign_screen)
			B.add_button(key + f" [color=#FF9800]{lenf}[/color]" if lenf else key,
				size_hint = (1,1),text_color = txt_col,
				on_press = self.set_foreign_screen,
				font_size = "14sp",bg_color = None,
				halign = 'center',info = key,bold = True, 
				italic = True,valign = 'top'
				)
			
			self.add_surf(B)
		
	@Cache_error
	def set_foreign_screen(self,wid):
		info = wid.info
		surf = self.but_dic.get(info)
		ret = True #self.sc.DB.Get_access_of(info)
		if ret == False :
			self.sc.add_refused_error(f"Accèss non autorisé! Veillez informer votre supérieur!!")
		if ret == None:
			...
		else:
			surf = surf(self,bg_color = self.sc.aff_col2)
			surf.add_all()
			self.add_modal_surf(surf,size_hint = (1,1),
				titre = wid.info,radius = dp(0))

