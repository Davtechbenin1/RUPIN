#Coding:utf-8
"""
	Surface de définition d'un objet popup général
"""
from kivy.uix.modalview import ModalView

class dialog_box(ModalView):
	def __init__(self, **kwargs):
		super().__init__(auto_dismiss=False, **kwargs)
		
	def fermer_popup(self, *args):
		self.dismiss()

