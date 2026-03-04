#Coding:utf-8

from kivy.uix.anchorlayout import AnchorLayout
try:
	from .wid import wid
except ImportError:
	from wid import wid

class anchor(wid,AnchorLayout):
	def __init__(self,mother,anchor_x ='left',
		anchor_y = 'top',
		**kwargs):
		AnchorLayout.__init__(self,anchor_x  = anchor_x,
			anchor_y = anchor_y)
		wid.__init__(self,mother,**kwargs)
		