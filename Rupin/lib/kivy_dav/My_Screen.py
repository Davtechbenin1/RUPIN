#Coding:utf-8
"""
	Cet module permet la définition de la surface de gestion
	des écrans avec le screen manager de kivy
"""
try:
	from davbuild import*
except ImportError:
	from .davbuild import*
from color import *
from kivy.core.window import Window

from kivy.uix.screenmanager import Screen,ScreenManager

class My_Screen(ScreenManager):
	def __init__(self,SCREEN,bg_color = 0,**kwargs):
		ScreenManager.__init__(self,**kwargs)
		self.SCREEN = SCREEN
		self.RECT = None
		if bg_color:
			if type(bg_color) in (int,float):
				bg_color = [bg_color]*3
			if len(bg_color) == 3:
				r,g,b = bg_color
				a = 1
			else:
				r,g,b,a = bg_color
			Window.clearcolor = r,g,b,a
		self.CLOSE_LAY = None
		self.Leaving_in_progress = False
		self.screen_dic = dict()

	def add_all(self):
		self.clear_widgets()
		for wid in self.screen_dic.values():
			self.add_screen(wid)
		self.Foreign_surf()

	def Foreign_surf(self):
		if self.CLOSE_LAY:
			self.add_widget(self.CLOSE_LAY)
			self.current = 'close'

	def add_screen(self,screen_obj):
		"""
			screen_obj doit être un objet screen.
			il doit avoir un nom
		"""
		self.add_widget(screen_obj)
		if not self.current:
			self.current = screen_obj.name
		self.screen_dic[screen_obj.name] = screen_obj

	def on_close(self):
		if self.Leaving_in_progress:
			Window.close()
		else:
			obj = self.screen_dic.get(self.current)
			if obj:
				ret = obj.Ret_handler('CLOSES')
				if ret:
					self.close_handler()
				return True
			else:
				self.close_handler()
				return False

	def close_handler(self):
		scr = Screen(name = 'close')
		obj = Fermetture(self)
		scr.add_widget(obj)
		scr.Ret_handler = obj.Ret_handler
		self.CLOSE_LAY = scr
		self.add_all()

	def Ret_handler(self,ret):
		if self.CLOSE_LAY:
			self.CLOSE_LAY.Ret_handler(ret)
		elif ret in self.screen_dic:
			self.current = ret
		else:
			obj = self.screen_dic.get(self.current)
			if obj:
				obj.Ret_handler(ret)

class Fermetture(float_l):
	def __init__(self,mother,**kwargs):
		kwargs['alpha'] = .8
		kwargs['bg_color'] = (0,0,0)
		kwargs['size_hint'] = 1,1
		kwargs['pos_hint'] = 0,0
		float_l.__init__(self,mother,**kwargs)
		self.add_all()

	def Foreign_surf(self):
		self.add_conf_surf()

	def add_conf_surf(self):
		self.conf_surf = box(self,size_hint = (None,None),
			width = dp(300),height = dp(90),
			padding = dp(5),spacing = dp(5),
			bg_color = AFF_COL2,radius = dp(5),
			pos_hint = (.1,.5))
		b1 = box(self,size_hint = (1,.3),
			orientation = 'horizontal')
		b1.add_button('X',size_hint = (.1,1),
			radius = dp(20),text_color = TEXT_COL2,
			bg_color = RED_,font_size = "20")
		b1.add_text("Quitter l'application?",
			halign = 'center',font_size = "14sp",
			text_color = TEXT_COL1)
		self.conf_surf.add_surf(b1)
		b2 = box(self,size_hint = (1,.5),
			orientation = "horizontal",
			padding = [dp(30),dp(10),dp(30),dp(10)],
			spacing = dp(40))
		b2.add_button("Non",font_size = '13sp',
			text_color = TEXT_COL1,bg_color = GREEN,
			radius = dp(5))

		b2.add_button("Oui",font_size = '13sp',
			text_color = TEXT_COL1,bg_color = RED_,
			radius = dp(5))
		self.conf_surf.add_surf(b2)

		self.add_surf(self.conf_surf)

	def Ret_handler(self,ret):
		if ret == 'Oui':
			Window.close()
		else:
			self.mother.SCREEN.root.Leaving_in_progress = False
			self.mother.CLOSE_LAY = None
			self.mother.add_all()





