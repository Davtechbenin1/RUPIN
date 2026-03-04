#Coding:utf-8
from kivy.uix.gridlayout import GridLayout
try:
	from .wid import wid
except ImportError:
	from wid import wid

class grid(wid,GridLayout):
	def __init__(self,mother,rows =None,
		cols = None,
		**kwargs):
		GridLayout.__init__(self)
		if cols:
			self.cols = cols
		if rows:
			self.rows = rows
		wid.__init__(self,mother,**kwargs)
		
		