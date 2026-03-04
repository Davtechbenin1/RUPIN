#Coding:utf-8
from kivy.uix.scrollview import ScrollView
try:
	from .wid import wid
except ImportError:
	from wid import wid
from kivy.graphics import*
from kivy.graphics.vertex_instructions import*

from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock

#"""
class FastScroll(ScrollView):
	container = ObjectProperty(None)
	all_widgets = ListProperty([])
	buffer_zone = NumericProperty(20)  # marge pour pré-chargement autour
	_round_event = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.scroll_type = ['bars', 'content']
		self.bar_width = 2
		self.effect_cls = 'ScrollEffect'
		self.do_scroll_x = True
		self.do_scroll_y = True

		self.bind(scroll_y=self._on_scroll, scroll_x=self._on_scroll)
		Clock.schedule_once(self._init_container, 0)

	def _init_container(self, dt):
		if self.container:
			self.update_visible_widgets()

	def add_widget_to_stack(self, widget):
		self.all_widgets.append(widget)
		self.container.add_widget(widget)

	def _update_height(self, instance, value):
		self.container.height = int(value)
		self._round_stack_positions()

	def _update_width(self, instance, value):
		self.container.width = value

	def _on_scroll(self, *args):
		if self._round_event is None:
			self._round_event = Clock.schedule_once(self._round_stack_positions, 0)

	def _round_stack_positions(self, *args):
		# Corrige toutes les positions floues des enfants
		self._round_event = None
		if not self.container:
			return

		for child in self.container.children:
			x, y = child.pos
			if not float(x).is_integer() or not float(y).is_integer():
				child.pos = (int(x), int(y))

	def update_visible_widgets(self):
		# Pour l'instant on ne fait pas de suppression : on affiche tout
		# (optimisation avancée possible avec calculs de coordonnées)
		pass  # À implémenter plus tard si besoin de très gros volumes

class scroll(wid,FastScroll):
	def __init__(self,mother,**kwargs):
		FastScroll.__init__(self)
		wid.__init__(self,mother,**kwargs)
		self.SC = True

	def on_touch_down(self,touch):
		FastScroll.on_touch_down(self,touch)

	def add_surf(self, widget):
		self.container = widget
		self.clear_widgets()  # 🔑 Vide d'abord le ScrollView

		for child in widget.children:
			child.pos = (int(child.x), int(child.y))
			child.size = (int(child.width), int(child.height))

		self.container.bind(
			minimum_height=self._update_height,
			minimum_width=self._update_width
		)
		self.add_widget(self.container)
#"""

class FastStackLayout(StackLayout):
	...

class scroll_new(ScrollView):
	container = ObjectProperty(None)
	all_widgets = ListProperty([])
	buffer_zone = NumericProperty(50)  # marge pour pré-chargement autour

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.container = FastStackLayout(size_hint=(1, None))
		self.container.bind(minimum_height=self._update_height)
		self.layout = True
		self.container.layout = True
		self.add_widget(self.container)

		self.scroll_type = ['bars', 'content']
		self.bar_width = 10
		self.effect_cls = 'ScrollEffect'

		self.bind(scroll_y=self._on_scroll, scroll_x=self._on_scroll)
		Clock.schedule_once(lambda dt: self.update_visible_widgets(), 1)

	def add_widget_to_stack(self, widget):
		self.all_widgets.append(widget)
		self.container.add_widget(widget)

	def _update_height(self, instance, value):
		self.container.height = value

	def _update_width(self, instance, value):
		self.container.width = value

	def _on_scroll(self, *args):
		Clock.schedule_once(lambda dt: self.update_visible_widgets(), 0)

	def update_visible_widgets(self):
		# Pour l'instant on ne fait pas de suppression : on affiche tout
		# (optimisation avancée possible avec calculs de coordonnées)
		pass  # À implémenter plus tard si besoin de très gros volumes
