#Coding:utf-8
try:
	from .wid import wid
	from .box import *
except ImportError:
	from wid import wid
	from box import *

from kivy.graphics import*
from kivy.graphics.vertex_instructions import*

from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
import time

from kivy.uix.scrollview import ScrollView
from kivy.uix.layout import Layout
from kivy.clock import Clock
from collections import deque
from kivy.uix.widget import Widget
from kivy.metrics import dp
from math import ceil

class MyRecycleLayout(Widget):
	def __init__(self, mother, **kwargs):
		super().__init__(**kwargs)
		self.mother = mother

		self.size_hint_y = None
		self.size_hint_x = 1

		self.viewclass = None
		self.data = []
		self.item_h = dp(40)
		self.buffer = 1
		self.viewport_h = 0

		self.slots = deque()
		self.first_index = 0

	# ---------- API ----------
	def set_viewport_height(self, h):
		self.viewport_h = max(0, h)
		self._update_content_height()
		self._build_slots()
		self._clamp_first_and_refresh()

	def set_viewclass(self, cls):
		self.viewclass = cls
		self._build_slots()
		self._clamp_first_and_refresh()

	def set_data(self, data):
		self.data = data or []
		self._update_content_height()
		self._build_slots()
		self._clamp_first_and_refresh(force=True)

	def update_by_scroll_y(self, scroll_y):
		if not self.data or self.viewport_h <= 0:
			return

		content_h = self.height
		if content_h <= self.viewport_h:
			new_first = 0
		else:
			top_px = (1.0 - scroll_y) * (content_h - self.viewport_h)
			new_first = int(top_px // self.item_h)

		visible = self._visible_count()
		max_first = max(0, len(self.data) - visible)
		new_first = max(0, min(new_first, max_first))

		if new_first != self.first_index:
			old = self.first_index
			self.first_index = new_first
			self._recycle_slots(old, new_first)

	# ---------- INTERNE ----------
	def _visible_count(self):
		return max(1, ceil(self.viewport_h / self.item_h))

	def _update_content_height(self):
		self.height = max(
			int(len(self.data) * self.item_h),
			int(self.viewport_h)
		)

	def _calc_needed_slots(self):
		if self.viewport_h <= 0:
			return 0
		visible = self._visible_count()
		return min(len(self.data), visible + 2 * self.buffer)

	def _build_slots(self):
		if not self.viewclass:
			return

		target = self._calc_needed_slots()
		current = len(self.slots)

		# déjà assez de slots
		if current >= target:
			return

		# ajouter les slots nécessaires
		for _ in range(target - current):
			w = self.viewclass(self.mother)
			if w.height:
				self.item_h = w.height
			w.data_index = -1
			self.add_widget(w)
			self.slots.append(w)

		self._refresh_slots(force=True)

	def _y(self, index):
		return self.height - (index + 1) * self.item_h

	def _up_wid(self,data_index,w,n,force,dt):
		if data_index < n:
			if force or w.data_index != data_index:
				w.set_data(data_index, self.data[data_index])
				w.data_index = data_index

			w.size = (self.width, self.item_h)
			w.pos = (self.x, self.y + self._y(data_index))
			w.opacity = 1
			w.disabled = False
		else:
			w.opacity = 0
			w.disabled = True

	def _refresh_slots(self, force=False):
		updates = []

		n = len(self.data)
		for slot_offset, w in enumerate(self.slots):
			data_index = self.first_index + slot_offset
			updates.append((data_index, w, n, force))

		# On stocke la file des updates
		self._pending_updates = deque(updates)

		# On lance un worker si pas déjà lancé
		if not getattr(self, "_pending_scheduled", False):
			self._pending_scheduled = True
			Clock.schedule_interval(self._process_refresh_queue, 0)


	def _process_refresh_queue(self, dt):
		"""Traite 1 ou plusieurs widgets par frame sans bloquer l'UI."""
		if not self._pending_updates:
			self._pending_scheduled = False
			return False

		# Tu peux traiter 1, 2 ou 3 par frame
		max_per_frame = 1  

		for _ in range(max_per_frame):
			if not self._pending_updates:
				break

			data_index, w, n, force = self._pending_updates.popleft()
			self._up_wid(data_index, w, n, force, dt)

		return True


			

	def _recycle_slots(self, old_first, new_first):
		step = new_first - old_first
		n = len(self.data)

		if abs(step) >= len(self.slots):
			self._refresh_slots(force=True)
			return

		if step > 0:
			# scroll vers le bas
			for _ in range(step):
				w = self.slots.popleft()
				new_i = self.first_index + len(self.slots)

				if new_i < n:
					w.set_data(new_i, self.data[new_i])
					w.data_index = new_i
					w.pos = (self.x, self.y + self._y(new_i))
					w.opacity = 1
					w.disabled = False
				else:
					w.opacity = 0
					w.disabled = True

				self.slots.append(w)

		else:
			# scroll vers le haut
			for _ in range(-step):
				w = self.slots.pop()
				new_i = self.first_index

				if new_i < n:
					w.set_data(new_i, self.data[new_i])
					w.data_index = new_i
					w.pos = (self.x, self.y + self._y(new_i))
					w.opacity = 1
					w.disabled = False
				else:
					w.opacity = 0
					w.disabled = True

				self.slots.appendleft(w)

	def _clamp_first_and_refresh(self, force=False):
		visible = self._visible_count()
		max_first = max(0, len(self.data) - visible)

		if self.first_index > max_first:
			self.first_index = max_first

		self._refresh_slots(force)

class vscroll(ScrollView):
	def __init__(self, mother, **kwargs):
		super().__init__(**kwargs)
		self.do_scroll_x = False
		self.do_scroll_y = True
		self.Layout = MyRecycleLayout(mother, **kwargs)
		self.add_widget(self.Layout)

		self.bind(height=self._on_viewport_resize,
				  scroll_y=self._on_scroll)
		#self.Layout.set_viewport_height(self.height)
		Clock.schedule_once(lambda *_: self.Layout.set_viewport_height(self.height), 0)

	def set_viewclass(self, cls):
		self.Layout.set_viewclass(cls)

	def set_data(self, data):
		self.Layout.set_data(data)

	def _on_viewport_resize(self, *_):
		self.Layout.set_viewport_height(self.height)

	def _on_scroll(self, *_):
		self.Layout.update_by_scroll_y(self.scroll_y)

# -------- 1) Élément (léger) --------
class MyItem(box):
	"""Widget de ligne léger, réutilisé (recyclé)."""
	text_data = StringProperty("")

	def __init__(self,mother, **kwargs):
		#kwargs['bg_color'] = mother.sc.sep
		super().__init__(mother,**kwargs)
		self.size_hint_y = None
		self.size_hint_x = 1
		self.height = dp(40)
		#self.orientation = "horizontal"
		self._data_index = -1  # index courant dans la data (pour éviter les set_data inutiles)

	def set_data(self, data_index: int, row: dict):
		"""Assigne les données SI l'index change (évite de retoucher la texture)."""
		if data_index != self._data_index:
			self._data_index = data_index
			# écrire directement dans text (Label dessine text)
		
		self.Foreign_surf(row)

	def Foreign_surf(self,data_dict):
		"""
			Doit être redéfinie par l'utilisateur pour établir un 
			viewclass unique
		"""

# Horizontal
class MyHorizontalItem(box):
	"""Widget de ligne horizontal léger, réutilisé (recyclé)."""
	text_data = StringProperty("")

	def __init__(self, mother, **kwargs):
		super().__init__(mother, **kwargs)
		self.size_hint_x = None
		self.size_hint_y = 1
		self.width = dp(100)  # largeur d’un élément
		self.halign = "center"
		self.valign = "middle"
		self.padding = (dp(5), 0)
		self._data_index = -1

	def set_data(self, data_index: int, row: dict):
		if data_index != self._data_index:
			self._data_index = data_index
		self.Foreign_surf(row)

	def Foreign_surf(self, data_dict):
		"""À redéfinir pour personnaliser le contenu horizontal."""
		pass


class MyHorizontalRecycleLayout(wid, Layout):
	def __init__(self, mother, **kwargs):
		Layout.__init__(self)
		wid.__init__(self, mother, **kwargs)
		self.size_hint_y = 1
		self.size_hint_x = None  # largeur totale dépend de la data

		self.viewclass = None
		self.data = []
		self.item_w = dp(100)
		self.buffer = 2
		self.viewport_w = 0
		self.slots = []
		self.first_index = 0
		self._update_scheduled = False

	def do_layout(self, *args):
		self._update_content_width()
		self.update_visible_by_first_index(self.first_index)

	def set_viewport_width(self, w: float):
		self.viewport_w = max(0, w)
		self._rebuild_slots()

	def set_viewclass(self, cls):
		self.viewclass = cls
		self._rebuild_slots()

	def set_data(self, data):
		self.data = data or []
		self._update_content_width()
		self._rebuild_slots()
		self.update_visible_by_first_index(self.first_index)

	def update_by_scroll_x(self, scroll_x: float):
		if not self.data or self.viewport_w <= 0:
			return
		content_w = self.width
		if content_w <= self.viewport_w:
			new_first = 0
		else:
			left_px = scroll_x * (content_w - self.viewport_w)
			new_first = int(left_px // self.item_w)
		new_first = max(0, min(new_first, max(0, len(self.data) - 1)))
		if new_first != self.first_index:
			self.first_index = new_first
			self._schedule_update()

	# ----- Interne -----
	def _update_content_width(self):
		self.width = max(self.item_w * len(self.data), self.viewport_w)

	def _calc_needed_slots(self) -> int:
		if self.viewport_w <= 0:
			return 0
		visible = ceil(self.viewport_w / self.item_w)
		needed = min(len(self.data), visible + 2 * self.buffer)
		return max(visible, needed)

	def _rebuild_slots(self):
		if not self.viewclass:
			return
		target = self._calc_needed_slots()
		while len(self.slots) < target:
			w = self.viewclass(self)
			self.add_widget(w)
			self.slots.append(w)
		while len(self.slots) > target:
			w = self.slots.pop()
			self.remove_widget(w)
		self._schedule_update()

	def _schedule_update(self):
		if not self._update_scheduled:
			self._update_scheduled = True
			Clock.schedule_once(self._do_update)

	def _do_update(self, *_):
		self._update_scheduled = False
		self.update_visible_by_first_index(self.first_index)

	def update_visible_by_first_index(self, first_index: int):
		if not self.slots:
			return
		n = len(self.data)
		content_w = self.width
		for slot_i, w in enumerate(self.slots):
			data_index = first_index + slot_i
			if data_index < n:
				w.set_data(data_index, self.data[data_index])
				w.opacity = 1.0
				w.disabled = False
				x = data_index * self.item_w
				w.size = (self.item_w, self.height)
				w.pos = (self.x + x, self.y)
			else:
				w.opacity = 0.0
				w.disabled = True
				w.pos = (self.x - 1000, self.y)

	def on_size(self, *_):
		self._schedule_update()


class hscroll(ScrollView):
	"""Scroll horizontal intelligent"""
	def __init__(self, mother, **kwargs):
		super().__init__()
		self.do_scroll_x = True
		self.do_scroll_y = False
		self.layout = True

		self.Layout = MyHorizontalRecycleLayout(mother, **kwargs)
		self.add_widget(self.Layout)

		self.bind(width=self._on_viewport_resize,
				  scroll_x=self._on_scroll)

		Clock.schedule_once(lambda *_: self.Layout.set_viewport_width(self.width), 0)

	def set_viewclass(self, cls):
		self.Layout.set_viewclass(cls)

	def set_data(self, data):
		self.Layout.set_data(data)

	def _on_viewport_resize(self, *_):
		self.Layout.set_viewport_width(self.width)

	def _on_scroll(self, *_):
		self.Layout.update_by_scroll_x(self.scroll_x)
