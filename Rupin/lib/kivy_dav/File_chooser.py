#Coding:utf-8

"""
	Cet module définie le root lay de façon a ce que,
	toutes les informations de sortie et la gestion
	des ret sont à définir ici
"""
from lib.davbuild import *
import sys
from pathlib import Path
from color import *
import asyncio
from image_process import Gest_img_format

class File_chooser(box):
	def __init__(self,SCREEN,**kwargs):
		gene_col = APP_COL
		box.__init__(self,SCREEN,Id = 'Main',
			orientation = 'horizontal',
			bg_color = gene_col,**kwargs)
		self.Path_obj = Path()
		self.home_dir = Path.home()

		self.dossier_list = list()
		self.curent_path = str()

		asyncio.run(self.add_all())

	async def add_all(self):
		self.init_list()
		await self.Foreign_surf()

	async def Foreign_surf(self):
		self.size_pos()
		await self.add_doss()
		await self.add_aff()

	def size_pos(self):
		w,h = self.dossier_size = .25,1
		self.aff_size = 1-w,1

	async def add_doss(self):
		h = dp(40)
		self.dossier_surf = box(self,size_hint = self.dossier_size,
			bg_color = AFF_COL2,spacing = dp(10),
			padding = dp(10))
		self.dossier_surf.add_text("Choix de dossier",
			size_hint = (1,.05),text_color = TITRE_COL,
			halign = 'center',font_size = '13sp',
			underline = True)

		dossier_list = list()
		fic_list = list()
		size = 1,.05
		n_liste = list()
		for child in self.home_dir.iterdir():
			if child.is_dir():
				name = child.name
				if '.' == name[0]:
					pass
				else:
					n_liste.append(name)
		n_liste.sort()
		H = (h+dp(10)) * len(n_liste)
		H += dp(10)
		stk_surf = stack(self,size_hint = (1,None),
			height = H,)
		for name in n_liste:
			self.dossier_list.append(name)
			img = 'media/dir.png'
			dossier_list.append((name,img))

		ASY_list = list()
		for tup in dossier_list:
			txt,img = tup
			txt_col = TEXT_COL1
			bg_color = self.dossier_surf.bg_color
			if self.curent_path == txt:
				txt_col = TEXT_COL2
				bg_color = AFF_COL1
			B = box(self,size_hint = (1,None),
				height = h,padding = dp(5),spacing = dp(5),
				radius = dp(5),bg_color = bg_color,
				orientation = 'horizontal')
			B.add_image(img,size_hint = (.2,1),info = txt,
				bg_color = None)
			B.add_text(txt,size_hint = (.8,1),
			text_color = txt_col,bg_color = bg_color)
			stk_surf.add_surf(B)
		src = scroll(self,size_hint = (1,.95),
			)
		src.add_surf(stk_surf)
		self.dossier_surf.add_surf(src)
			
		self.add_surf(self.dossier_surf)

	async def add_aff(self):
		self.Liste_des_fichier = list()
		img_w = dp(90)
		img_h = dp(70)
		self.aff_surf = stack(self,size_hint = self.aff_size,
			bg_color = self.bg_color, padding = dp(10),
			spacing = dp(10))

		self.CUR_DIR = curent_direct = self.home_dir.joinpath(self.curent_path)
		txt = "Cliquez sur un fichier pour le choisir"
		
		self.aff_surf.add_text(txt,size_hint = (.9,.04),
			halign = 'center',underline = True,
			text_color = TITRE_COL,font_size = "14sp")

		self.aff_surf.add_button('Close',size_hint = (.07,.04),
			halign = "center",text_color = TEXT_COL2,
			bg_color = RED_,shadow_color = GRIS_,
			font_size = '13sp',info = "CLOSE_ME")

		ASY_list = list()
		stk_surf = stack(self,size_hint=(1,None),
			height = self.aff_surf.size[1],spacing = dp(15))
		for child in curent_direct.iterdir():
			name = child.name
			if '.' == name:
				pass
			else:
				if child.is_file():
					img_surf = self.get_name_surf(name,child,
						img_w,img_h)
					if img_surf:
						stk_surf.add_surf(img_surf)
		src = scroll(self,size_hint = (1,1))
		src.add_surf(stk_surf)
		self.aff_surf.add_surf(src)
						
		
		self.add_surf(self.aff_surf)

	def checking(self,name):
		tup = name.split(".")
		if len(tup)==2:
			name,prefice = tup
		else:
			prefice = ""
		if prefice in ("png","jpg",'jpeg'):
			return True
		else:
			return False

	def get_name_surf(self,name,child,w,h):
		if self.checking(name):
			img = str(child)
			self.Liste_des_fichier.append(img)
			lay = box(self,size_hint = (None,None),
				width = w,height = h)
			lay.add_image(img,size_hint = (1,.8),
				info = img,bg_color = None)
			lay.add_text(name,size_hint = (1,.2),
				text_color = TEXT_COL1,info = img,
				halign = 'center')
			return lay
		else:
			return None
		
	def Ret_handler(self,ret):
		if ret:
			if ret in self.dossier_list:
				self.curent_path = ret
				asyncio.run(self.add_all())
			elif ret in self.Liste_des_fichier:
				self.SCREEN.FICHIER = Gest_img_format(ret)
				return Gest_img_format(ret)
			elif ret == 'CLOSE_ME':
				return ret



