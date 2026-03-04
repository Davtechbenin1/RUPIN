#Coding:utf-8

from kivy.app import App

from text import text
from button import but
from video_play import video_play

class ThisApp(App):
	def build(self):
		wid = video_play(source="Tuto_00007.mp4")
		return wid

ThisApp().run()


