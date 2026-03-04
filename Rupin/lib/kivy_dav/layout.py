#Coding:utf-8
"""
	Cette interface définie le cadre de programmation
	d'une surface d'affichage complète. 

	C'est le seul conteneur agréé pour contenir les
	information d'une surface d'affichage
"""
from kivy.uix.screenmanager import Screen
try:
	from .wid import wid
except ImportError:
	from wid import wid
try:
	from .image import imag
except ImportError:
	from image import imag
from kivy.metrics import dp
from color import *

class layout(wid,Screen):
	def __init__(self,mother,name,img_bg = str(),
		menu_but = False,**kwargs):
		"""
			Le nom est obligatoire
		"""
		Screen.__init__(self,name = name)
		wid.__init__(self,mother,**kwargs)
		self.My_Mother = self.SCREEN.root
		"""
			La variable self.My_Mother représente l'objet
			screenmanager de l'application qui est le root
		"""
		self.menu_but_color = 1,1,1
		self.menu_txt_color = 0,0,0
		self.img_bg = img_bg
		self.menu_but = menu_but

	def add_all(self):
		self.init_list()
		if self.PRIORITY_LAY:
			self.add_surf(self.PRIORITY_LAY)
		else:
			if self.img_bg:
				img = imag(self.img_bg,keep_ratio = False,
					size_hint = (1,1),pos_hint = (0,0))
				self.add_widget(img)
			if self.menu_but:
				self.add_menu_but()
			self.Foreign_surf()

	def add_menu_but(self):
		self.add_text('| | |',size_hint = (None,None),
			width = dp(34),height = dp(34),
			font_size = '16sp',
			radius = dp(30),#bg_color = self.menu_but_color,
			text_color =self.menu_txt_color,info = 'Menu_surf',
			pos_hint = (.02,.95))
		self.add_text(self.SCREEN.TITRE,font_size = "15sp",
			text_color = TEXT_COL1,halign = 'left',
			size_hint = (.8,None),
			height = dp(34),pos_hint = (.14,.95))

	def Ret_hand(self,ret):
		return ret

	def Ret_handler(self,ret):
		ret = self.Ret_hand(ret)
		if ret == 'CLOSES':
			"""
				Le principe ici est que, chaque fois qu'une
				demande de fermetture est emis, on parcours
				l'ensemble des fenettres afin de fermer toutes
				les Priority_lay. Si tout est bon, on envoie
				une True pour signaler que l'application peut fermet
			"""
			return True



