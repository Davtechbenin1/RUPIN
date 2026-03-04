#Coding:utf-8
"""
	Cette maquette permet de créer une forme d'interface
	unique pour les parties du logiciel
"""
from lib.davbuild import *
class menu_surf_H_maquette(box):
	def __init__(self,mother,part2_surf,space = 10,
			part1_size = (.3,1),**kwargs):
		kwargs['orientation'] = "horizontal"
		kwargs['padding'] = dp(10)
		kwargs['spacing'] = dp(10)
		box.__init__(self,mother,**kwargs)

		w,h = self.part1_size = part1_size
		self.part2_size = 1-w,h
		self.part2_surf = part2_surf
		self.space = space
		self.size_pos()

	def size_pos(self):
		self.part1_surf = stack(self,size_hint = self.part1_size,
			padding = dp(10),spacing = dp(10),radius = dp(10),
			bg_color = self.sc.aff_col1)
		self.part2_surf = self.part2_surf(self,
			size_hint = self.part2_size,
			bg_color = self.sc.aff_col1,padding = dp(10),
			radius = dp(10),spacing = dp(self.space))
		self.add_surf(self.part1_surf)
		self.add_surf(self.part2_surf)

	def Foreign_surf(self):
		self.add_part1_surf()
		self.add_part2_surf()

	def add_part1_surf(self):
		pass

	def add_part2_surf(self):
		pass

	def add_title_to_part1(self,title):
		self.part1_surf.clear_widgets()
		B = box(self,size_hint = (1,.04),
			orientation = 'horizontal')
		B.add_button('',size_hint = (None,None),height = dp(20),
			width = dp(20),bg_color = self.sc.red,
			on_press = self.mother.BACK,pos_hint = (0,.25),
			)
		B.add_text(title,halign = 'center',
			text_color = self.sc.text_col1,)
		self.part1_surf.add_surf(B)

class menu_surf_V_maquette(box):
	def __init__(self,mother,**kwargs):
		box.__init__(self,mother,**kwargs)
		self.size_pos()
		self.initialisation()

	def size_pos(self):
		self.menu_in_action = str()
		self.part1_surf = stack(self,size_hint = (1,None),
			height = dp(40),padding_left = dp(10),
			bg_color = self.sc.aff_col3,radius = dp(10))
		self.part2_surf = box(self)
		
		self.add_surf(self.part1_surf)
		self.add_text('',size_hint = (1,None),height = dp(1),
			bg_color = self.sc.text_col1)
		self.add_surf(self.part2_surf)

	def Get_menu_infos(self):
		self.wid_dict = dict()
		self.icon_dict = dict()

	def Foreign_surf(self):
		self.add_menu_info()

	def add_menu_info(self):
		self.Get_menu_infos()
		self.part1_surf.clear_widgets()
		self.part2_surf.clear_widgets()
		for info,srf in self.wid_dict.items():
			if not self.menu_in_action:
				self.menu_in_action = info

			txt_col = self.sc.text_col1
			if self.menu_in_action == info:
				txt_col = self.sc.green
				srf = srf(self,bg_color = self.sc.aff_col1)
				srf.add_all()
				self.part2_surf.add_surf(srf)

			icon = self.icon_dict.get(info,"plus")
			self.part1_surf.add_icon_but(icon = icon,
				text_color = txt_col,font_size = "34sp",
				size_hint = (None,1),size = (dp(35),0),
				on_press = self.change_screen,info = info)

			self.part1_surf.add_button(info, text_color = txt_col,
				bg_color = None,halign = 'left',
				size_hint = (None,1),width = dp(20),on_press = self.change_screen)

	def change_screen(self,wid):
		self.menu_in_action = wid.info
		self.add_all()

class menu_surf_HH_maquette(box):
	def __init__(self,mother,**kwargs):
		box.__init__(self,mother,**kwargs)
		self.orientation = 'horizontal'
		self.size_pos()
		self.initialisation()

	def size_pos(self):
		self.menu_in_action = str()
		self.part1_surf = stack(self,size_hint = (None,1),
			width = dp(300),radius = [dp(10),0,0,dp(10)],
			bg_color = self.sc.aff_col1,padding_left = dp(10))
		self.part2_surf = box(self)
		
		self.add_surf(self.part1_surf)
		self.add_text('',size_hint = (None,1),width = dp(1),
			bg_color = self.sc.text_col1)
		self.add_surf(self.part2_surf)

	def Get_menu_infos(self):
		self.wid_dict = dict()
		self.icon_dict = dict()

	def Foreign_surf(self):
		self.add_menu_info()

	def add_menu_info(self):
		self.Get_menu_infos()
		self.part1_surf.clear_widgets()
		self.part2_surf.clear_widgets()
		self.part1_surf.add_text(self.menu_in_action,size_hint = (1,.05),
			text_color = self.sc.orange,valign = 'bottom')
		self.part1_surf.add_text('',size_hint = (.3,None),
			height = dp(1),bg_color = self.sc.orange,underline = True)
		self.part1_surf.add_padd((1,.025))
		for info,wid in self.wid_dict.items():
			if not self.menu_in_action:
				self.menu_in_action = info

			txt_col = self.sc.text_col1
			if self.menu_in_action == info:
				txt_col = self.sc.green
				wid = wid(self,bg_color = self.sc.aff_col1,
					radius = [0,dp(10),dp(10),0])
				self.part2_surf.add_surf(wid)

			icon = self.icon_dict.get(info,"plus")
			b = stack(self,size_hint = (1,None),
				height = dp(45))
			b.add_icon_but(icon = icon,text_color = txt_col,font_size = "34sp",
				size_hint = (None,1),size = (dp(35),0),on_press = self.change_screen)

			b.add_button(info, text_color = txt_col,
				bg_color = None,halign = 'left',
				size_hint = (None,1),width = dp(265),
				on_press = self.change_screen)
			self.part1_surf.add_surf(b)

	def change_screen(self,wid):
		self.menu_in_action = wid.info
		self.add_all()