#Coding:utf-8
from kivy.uix.floatlayout import FloatLayout
try:
	from .wid import wid
except ImportError:
	from wid import wid

class float_l(wid,FloatLayout):
	def __init__(self,mother,**kwargs):
		FloatLayout.__init__(self)
		wid.__init__(self,mother,**kwargs)

