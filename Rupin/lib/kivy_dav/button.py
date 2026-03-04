#Coding:utf-8
"""
	Générateur de Button
"""
from kivy.uix.button import Button
from kivymd.uix.button import MDIconButton

try:
	from .Surf import surf
	from .metrics import dp,sp
except ImportError:
	from Surf import surf
	from metrics import dp,sp

from kivy.core.window import Window

class but(surf,Button):
	def __init__(self,txt,base_direction = None,
		line_height = 1,
		markup = True,max_lines = 0,mipmap = False,
		bold =False,on_press = None,on_state = None,
		on_motion = None,on_release = None,
		italic = False,underline = False,
		font_name = 'Roboto',halign = 'center',
		font_size = "15sp",valign = 'middle',
		text_color = (1,1,1),shorten = False,
		strip = True,language = 'fr',
		bg_color = None,
		radius = dp(10),shadow = 0,
		shadow_color = (.1,.1,.1),
		bg_opact = 0,**surf_args):
		Button.__init__(self,text = txt,
			base_direction = base_direction,
			bold = bold,color = text_color,
			font_name = font_name,mipmap = mipmap,
			font_size = font_size,halign = halign,
			italic = italic,line_height = line_height,
			markup = markup,max_lines = max_lines,
			shorten = shorten,strip = strip,
			text_language = language,underline = underline,
			valign = valign,
			background_color = (0,0,0,bg_opact))
		surf.__init__(self,bg_color = bg_color,radius = radius,
			shadow = shadow,
			shadow_color = shadow_color,**surf_args)
		if on_press:
			self.bind(on_press = on_press)
		if on_release:
			self.bind(on_release = on_release)
		if on_state:
			self.bind(on_state = on_state)
		self.background_normal = str()
	
	def Another_event(self,value):
		self.text_size = self.size

class icon_but(MDIconButton):
	def __init__(self,on_press = None,on_release = None,
		pos_hint = (.5,.5),on_motion = None,bg_color = (1,1,1,1),
		text_color = (0,0,0,1),theme_text_color = 'Primary',**kwargs):
		super().__init__(**kwargs)
		self.theme_text_color = theme_text_color
		self.size_hint = kwargs.get('size_hint',(1,1))
		self.size = kwargs.get("size",((dp(100),dp(100))))
		self.font_size = str(sp(kwargs.get('font_size',"17sp")))
		self.text_color = tuple(text_color)
		self.pos_hint = {"center_x": pos_hint[0], "center_y": pos_hint[1]}
		self.layout = False
		if on_release:
			self.bind(on_release = on_release)
		if on_motion:
			self.bind(on_motion = on_motion)
		if on_press:
			self.bind(on_press = on_press)
		
