#Coding:utf-8
from kivy.uix.boxlayout import BoxLayout
try:
	from .wid import wid
except ImportError:
	from wid import wid

class box(wid,BoxLayout):
	def __init__(self,mother,orientation = "vertical",
		**kwargs):
		BoxLayout.__init__(self,
			orientation = orientation)
		wid.__init__(self,mother,**kwargs)

	def add_padd(self,size):
		self.add_text('',size_hint = size)

