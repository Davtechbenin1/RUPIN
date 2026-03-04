#Coding:utf-8
"""
	Générateur de video
"""
from kivy.uix.videoplayer import VideoPlayer
try:
	from .Surf import surf
except ImportError:
	from Surf import surf

class video_play(VideoPlayer):
	def __init__(self,source,**kwargs):
		VideoPlayer.__init__(self,**kwargs)
