#Coding:utf-8
"""
	Générateur de Label
"""
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
try:
	from .Surf import surf
except ImportError:
	from Surf import surf

from kivy.core.window import Window
import traceback
from kivy.utils import platform

from .metrics import *

class text_input(surf,TextInput):
	def __init__(self,allow_copy = True,
		auto_indent = False,bg_color = (.8,.8,.8),
		alpha = 1,bg_active = str(),bg_normal = str(),
		write_tab = False,
		multiline = False,focus = False,
		on_enter = None,on_text = None,
		default_text = str(),font_name = 'Roboto',
		text_color = (0,0,0),border = 4,font_size = "15sp",
		halign = 'left',placeholder = str(),
		placeholder_color = (.5,.5,.5),
		password = False,password_mask = "*",readonly = False,
		language = 'fr'
		,**kwargs):
		placeholder = str(placeholder)
		default_text = str(default_text)
		text_color = text_color
		r,g,b = bg_color
		col = r,g,b,alpha
		if type(border) in (int,float):
			border = [border] * 4
		TextInput.__init__(self,allow_copy = allow_copy,
			auto_indent = auto_indent,background_color = col,
			border = border,font_name = font_name,
			focus = focus,top = 50,
			font_size = font_size,foreground_color = text_color,
			halign = halign,
			hint_text = placeholder,multiline = multiline,
			password = password,hint_text_color = placeholder_color,
			readonly = readonly,text = default_text,
			text_language = language,write_tab = write_tab,
			password_mask = password_mask,use_bubble = True,)
		self.background_active = bg_active
	
		self.background_normal = bg_normal

		padding_top = kwargs.get('padding_top',5)
		padding_left = kwargs.get('padding_left',10)
		padding_right = kwargs.get('padding_right',10)
		kwargs['padding_top'] = padding_top
		kwargs['padding_left'] = padding_left
		kwargs['padding_right'] = padding_right
		
		surf.__init__(self,**kwargs)

		if on_text:
			self.bind(text = on_text)
		if on_enter:
			self.bind(on_text_valide = on_enter)

		self.bind(focus = self.show_ent)

	def show_ent(self,*args):
		try:
			if platform == "android":
				if self.focus:
					self.parent.sc.show_clavier(dp(290))
				else:
					self.parent.sc.show_clavier(0)
		except:
			ERROR = traceback.format_exc()

	def _update_padding(self, *args):
		# Calcule un padding vertical pour centrer le texte
		total_height = self.height
		text_height = self.line_height
		padding = ( (total_height - text_height) / 4, )
		self.padding_y = padding

