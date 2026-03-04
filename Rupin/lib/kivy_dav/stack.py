#Coding:utf-8
from kivy.uix.stacklayout import StackLayout
try:
	from .wid import wid
except ImportError:
	from wid import wid

from kivy.metrics import dp

class stack(wid,StackLayout):
	def __init__(self,mother,**kwargs):
		StackLayout.__init__(self)
		wid.__init__(self,mother,**kwargs)


	def add_padd(self,size):
		self.add_text('',size_hint = size)

	def add_separateur(self,size_hint,width = 100,
		height = 100,bg_color = (0,0,0)):
		bg_color = self.sc.sep
		self.add_text('',size_hint = size_hint,
			width = width,height = height,
			bg_color = bg_color)

	def add_stack_but(self,fonc,txt = "",padd = None,bg_color = tuple()):
		col = self.sc.red
		if bg_color:
			col = bg_color
		if padd:
			self.add_padd(padd)
		self.add_button("",size_hint = (None,None),
			width=dp(25),height = dp(25),on_press = fonc,
			bg_color = col,radius = dp(15))

	def add_button_custom(self,text,fonc,bg_color = tuple(),
		text_color = tuple(),padd = None,**kwargs):
		if not bg_color:
			bg_color = self.sc.green
		if not text_color:
			text_color = self.sc.text_col3
		if padd:
			self.add_padd(padd)
		kwargs['on_press'] = fonc
		return self.add_button(text,text_color = text_color,
			bg_color = bg_color,**kwargs)

		
		