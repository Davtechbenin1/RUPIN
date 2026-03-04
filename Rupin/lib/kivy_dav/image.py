#Coding:utf-8
"""
	Générateur d'image
"""
from kivy.uix.image import AsyncImage
from kivymd.uix.fitimage import FitImage

try:
	from .Surf import surf
except ImportError:
	from Surf import surf


from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from io import BytesIO
import threading
import requests

class imag(surf,Image):
	CACHE_IMAGE = dict()
	def __init__(self,source,border = 1,
		fit_mode = 'fill',allow_stretch = True,
		image_color = [1,1,1,1],keep_ratio=True,
		mipmap = False,opacity = 1,info = str(),**kwargs):

		Image.__init__(self,
			fit_mode = fit_mode,
			allow_stretch = allow_stretch,
			#color = image_color,
			keep_ratio = keep_ratio,
			mipmap = mipmap,
			anim_loop = 0,
			#opacity = opacity,
			)
		#kwargs['bg_color'] = image_color
		surf.__init__(self,**kwargs)
		self.info = info
		
		self.url = source
		self.image_data = None  # Ici on stocke l'image binaire

		if self.image_data:
			self.load_from_bytes(self.image_data)
		elif self.url:
			# lance le téléchargement en arrière-plan
			threading.Thread(target=self.download_image, daemon=True).start()

	def download_image(self):
		"""
		Charge l'image depuis l'URL si c'est un lien distant,
		ou depuis le disque si c'est un fichier local.
		"""
		if self.url in imag.CACHE_IMAGE:
			image_data = imag.CACHE_IMAGE[self.url]
			Clock.schedule_once(lambda dt: self.load_from_bytes(image_data),1)
		else:
			try:
				if self.url.startswith("http://") or self.url.startswith("https://"):
					# Image distante → téléchargement
					resp = requests.get(self.url)
					if resp.status_code == 200 and resp.text != "Connexion error":
						self.image_data = resp.content
						Clock.schedule_once(lambda dt: self.load_from_bytes(self.image_data),1)
					else:
						print(f"Erreur téléchargement: statut {resp.status_code}")
						Clock.schedule_once(lambda dt: self.stop_spinner(),1)
				else:
					# Image locale → lecture du fichier
					with open(self.url, "rb") as f:
						self.image_data = f.read()
					Clock.schedule_once(lambda dt: self.load_from_bytes(self.image_data),1)
			except Exception as e:
				print("Erreur téléchargement / lecture fichier:", e)
				Clock.schedule_once(lambda dt: self.stop_spinner(),1)

	def load_from_bytes(self, data, save_in = True):
		"""Charge l'image à partir de bytes"""
		if save_in:
			if self.url not in imag.CACHE_IMAGE:
				imag.CACHE_IMAGE[self.url] = data
		buf = BytesIO(data)
		img = CoreImage(buf, ext="png")  # tu peux changer ext selon le format
		self.texture = img.texture

	def stop_spinner(self):
		with open("media/logo.png", "rb") as f:
			self.image_data = f.read()
		Clock.schedule_once(lambda dt: self.load_from_bytes(self.image_data,save_in = False),1)

