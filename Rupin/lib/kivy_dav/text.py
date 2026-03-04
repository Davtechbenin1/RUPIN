#Coding:utf-8
"""
	Générateur de Label
"""
from kivy.uix.label import Label
try:
	from .Surf import surf
except ImportError:
	from Surf import surf

class text(surf,Label):
	def __init__(self,txt,base_direction = None,
		line_height = 1,
		markup = True,max_lines = 0,mipmap = False,
		bold =False,
		italic = False,underline = False,
		font_name = 'Roboto',halign = 'left',
		font_size = "15sp",valign = 'middle',
		text_color = (1,1,1),shorten = False,
		strip = True,language = 'fr',**surf_args):
		Label.__init__(self,text = txt,
			base_direction = base_direction,
			bold = bold,color = text_color,
			font_name = font_name,mipmap = mipmap,
			font_size = font_size,halign = halign,
			italic = italic,line_height = line_height,
			markup = markup,max_lines = max_lines,
			shorten = shorten,strip = strip,
			text_language = language,underline = underline,
			valign = valign)
		surf.__init__(self,**surf_args)
	
	def Another_event(self,value):
		self.text_size = self.size


