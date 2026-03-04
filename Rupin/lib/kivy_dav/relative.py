#Coding:utf-8
from kivy.uix.relativelayout import RelativeLayout
try:
	from .wid import wid
except ImportError:
	from wid import wid

class relative(wid,RelativeLayout):
	def __init__(self,mother,**kwargs):
		RelativeLayout.__init__(self)
		wid.__init__(self,mother,**kwargs)

