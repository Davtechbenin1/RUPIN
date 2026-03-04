#Coding:utf-8
"""
	Liste déroulante pro & stylisée pour sélectionner une info.
"""
from lib.davbuild import *

# coding:utf-8
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import ListProperty, StringProperty
from kivy.uix.label import Label

from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp


class modal_list(DropDown):
	def __init__(self, bg_color=(1, 1, 1, 1), **kwargs):
		super().__init__(**kwargs)
		self.bg_color = bg_color
		if self.bg_color:
			with self.canvas.before:
				Color(*self.bg_color)
				self.rect = Rectangle(size=self.size, pos=self.pos)

			self.bind(size=self._update_rect, pos=self._update_rect)

	def _update_rect(self, *args):
		self.rect.size = self.size
		self.rect.pos = self.pos


class liste_set(box):
	"""
	Liste déroulante pro & stylisée pour sélectionner une info.

	- mother (obligatoire)
	- info : valeur initiale
	- list_info : liste de choix
	- mother_fonc(info) : callback après sélection
	- readonly : empêche l’ouverture
	"""

	main_color = ListProperty([0.2, 0.6, 0.86, 1])   # bleu principal
	text_color = ListProperty([1, 1, 1, 1])          # texte blanc
	hover_color = ListProperty([0.85, 0.9, 0.95, 1]) # hover clair

	def __init__(self,
				 mother,
				 info="",
				 list_info=None,
				 orient = str(),
				 mother_fonc=None,
				 readonly=False,
				 font_size = "12sp",
				 max_items=20,
				 mult = None,
				 add_null_text = True,
				 sub_mod = None,
				 drop_width = dp(200),
				 orientation="horizontal",
				 **kwargs):
		box.__init__(self,mother,orientation="horizontal", 
			**kwargs)

		self.info = info or ""
		self.list_info = self.normal_list(list_info or [], max_items)
		self.mother_fonc = mother_fonc
		self.readonly = readonly
		self.add_null_text = add_null_text

		# bouton principal stylé
		self.add_icon_but(icon="chevron-down",
			text_color=self.sc.text_col1, font_size="20sp",
			size_hint=(None,1), size=(dp(20),dp(2)),
			on_release=self.open_dropdown, info=self.info)

		self.main_button = self.add_button(
			self.info or "Sélectionner...",
			size_hint=(1, 1),
			#height=dp(35),
			padding_left = dp(0),
			text_color=self.sc.green,
			font_size=font_size,
			bold=True, valign="middle",
			halign="left",
			bg_color=None,
			padding_top= dp(2),
			on_release=self.open_dropdown
		)

		self.dropdown = modal_list(auto_width=False, width=drop_width,
			bg_color=self.sc.aff_col3)
		self.populate_dropdown()

	def normal_list(self, liste, max_items):
		return [i for i in liste if i]#[:max_items]

	def populate_dropdown(self):
		"""Remplit le menu déroulant avec les items + option par défaut"""
		self.dropdown.clear_widgets()
		if self.add_null_text:
			items = ["Sélectionner..."] + self.list_info
		else:
			items = self.list_info
		for item in items:
			btn = but(
				str(item),
				size_hint=(1,None),
				height=dp(40),
				font_size='12sp',#self.sc.default_font_size,
				text_color=self.sc.text_col1,
				halign="left",
				bg_color=None,
				#bold=True,
				padding_left=dp(10)
			)
			btn.bind(on_release=lambda btn: self.select_item(btn.text))
			self.dropdown.add_widget(btn)

	def open_dropdown(self, *args):
		if not self.readonly:
			self.dropdown.open(self.main_button)

	def select_item(self, value):
		"""Gestion du choix dans la liste"""
		if value == "Sélectionner...":
			self.info = ""
			self.main_button.text = "Sélectionner"
		else:
			self.info = value
			self.main_button.text = f"{value}"

		self.dropdown.dismiss()
		if self.mother_fonc:
			Clock.schedule_once(lambda dt: self.mother_fonc(self.info))

	# -------- API externe --------

	def set_list_info(self, new_list):
		self.list_info = self.normal_list(new_list, max_items=20)
		self.populate_dropdown()

	def set_value(self, value):
		if value in self.list_info:
			self.info = value
			self.main_button.text = f"{value}"
		else:
			self.info = ""
			self.main_button.text = "Sélectionner"
