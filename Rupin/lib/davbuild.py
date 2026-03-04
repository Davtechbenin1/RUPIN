
#Coding:utf-8
try:
	from .kivy_dav.davbuild import *
	from .kivy_dav.My_Screen import My_Screen
	from .General.periode_set import Periode_set
	from .General.liste_set import *
	from .General.Table_surf import Table
	from .General.liste_deroulante import liste_deroulante
	from .General.input_search_lay import *
	from .General.maquette import *
	from .General.choix_mult import liste_choice
	from .General.dynamique_tab import dynamique_tab
	from .General.Dialog_box import dialog_box
	from .General.Confirmation import Confirmation_srf


except ImportError:
	from kivy_dav.davbuild import *
	from kivy_dav.My_Screen import My_Screen
	from General.periode_set import Periode_set
	from General.liste_set import *
	from General.Table_surf import Table
	from General.liste_deroulante import liste_deroulante
	from General.input_search_lay import *
	from General.maquette import *
	from General.choix_mult import liste_choice
	from General.dynamique_tab import dynamique_tab
	from General.Dialog_box import dialog_box
	from General.Confirmation import Confirmation_srf

import os, json
import os.path
from threading import Thread
import webbrowser
import requests,sys,time
from random import choice
import websocket
import ssl, webbrowser, urllib.parse
import threading
from lib.serveur.DAV_BASE.MyData import date_obj
from datetime import timedelta
from datetime import datetime, timedelta


from kivy.utils import get_color_from_hex
import ssl
import certifi

from .dav_fic_handler import *
from pathlib import Path
import datetime as THHHHH

from kivy.uix.modalview import ModalView
import traceback
import functools

from kivy.uix.spinner import Spinner
from kivy.clock import Clock

class LoadingView(ModalView):
	def __init__(self,mother,th_text = 'Chargement...',
		bg_color = (0,0,0,.2),font_size = '12sp',
		text_color = (0,0,0,1),halign = 'center',
		overlay_color = (1,1,1,.2), **kwargs):
		kwargs['background_color'] = bg_color
		super().__init__(**kwargs)
		self.size_hint = (1, 1)
		self.auto_dismiss = False
		self.overlay_color = overlay_color
		b = float_l(mother,bg_color = bg_color)
		b.add_image('media/Wait_img.png',
			keep_ratio = False)
		b.add_text(th_text,text_color = text_color,
			halign = halign,font_size = font_size,
			bold = True)
		self.add_widget(b)

	def show(self):
		Clock.schedule_once(self._show,.01)
		#self._show()
		

	def _show(self,*args):
		self.open()

	def hide(self):
		Clock.schedule_once(self._hide,.01)
		#self._hide()

	def _hide(self, *args):
		self.dismiss()

def get_date_from_N(Num):
	return Num.split("N°")[-1].split("_")[0]

def send_wht_message(lien,message):
	message_code = urllib.parse.quote(message)
	lien+=f"?text={message_code}"
	webbrowser.open(lien)


out_put = ""

def Cache_error(fonc_origin):
	@functools.wraps(fonc_origin)
	def wrapper(*args,**kwargs):
		try:
			return fonc_origin(*args,**kwargs)
		#"""
		except Exception as E:
			self = args[0]
			modal = ModalView(auto_dismiss = True,size_hint = (.8,.3),
				overlay_color = self.sc.overlay_color, )
			def close(*args):
				modal.dismiss()
			
			h = .1
			ERROR = traceback.format_exc()
			error_log(ERROR)
			error = ERROR.split('\n')[-2]
			S = stack(self,bg_color = self.sc.aff_col3,
				padding = dp(5), radius = dp(10))
			S.add_icon_but(icon = 'alert',text_color = self.sc.red,
				size_hint = (.1,.13),font_size = "18sp")
			S.add_text("Erreur d'exécution",text_color = self.sc.red,
				size_hint = (.8,.13))
			S.add_icon_but(icon = 'close',text_color = self.sc.black,
				size_hint = (.1,.13),on_press = close,
				font_size = "18sp")

			S.add_text(error,size_hint = (1,.87),padding = dp(10),
				halign = 'center',text_color = self.sc.red,
				bg_color = self.sc.aff_col1,radius = dp(10))
			modal.add_widget(S)
			modal.open()
		#"""
	return wrapper

def error_log(message):
	now = THHHHH.datetime.now()
	fic_name = now.strftime("%H-%M.txt")

	log_pat = Path(f"Log")
	os.makedirs(log_pat,exist_ok = True)
	log_pat = os.path.join(log_pat,f"{now.strftime('%Y-%m-%d')}")
	os.makedirs(log_pat,exist_ok = True)

	fic_name = os.path.join(log_pat,fic_name)
	with open(fic_name,'a') as fic:
		fic.write(message)
		fic.write('\n\n')
	print(message)

def Get_border_surf(mother,srf,color,pos_hint = (0,0),padd = dp(1),
	**kwargs):
	size_hint = srf.size_hint
	b = box(mother,size_hint = size_hint,bg_color = color,
		padding = padd,radius = srf.radius,pos_hint = pos_hint,
		**kwargs)
	srf.size_hint = (1,1)
	b.add_surf(srf)
	mother.add_surf(b)
	return srf

def Get_border_input_surf(mother,info,size_hint,
	border_col = None,bg_color = None,
	border_srf_parr = dict(),**inp_param):
	if not border_col:
		border_col = mother.sc.orange

	if not bg_color:
		bg_color = mother.sc.aff_col3

	b = box(mother,size_hint = size_hint,bg_color = bg_color,
		radius = dp(10),padding = dp(5))
	if 'placeholder' not in inp_param:
		inp_param['placeholder'] = info
	inp_param['bg_color'] = bg_color
	inp_surf = b.add_input(info,**inp_param)
	b = Get_border_surf(mother,b,border_col,**border_srf_parr)
	return b,inp_surf

def Save_local_json(fichier,donne):
	if not '.json' in fichier:
		fichier+='.json'	
	log_pat = os.path.join(out_put,"INFO")
	os.makedirs(log_pat,exist_ok = True)
	file_path = os.path.join(log_pat,fichier)
	with open(file_path,"w",encoding = 'utf-8')as f:
		json.dump(donne,f,indent = 4)

def Get_local_json(fichier):
	if not '.json' in fichier:
		fichier+='.json'
	log_pat = os.path.join(out_put,"INFO")
	os.makedirs(log_pat,exist_ok = True)
	file_path = os.path.join(log_pat,fichier)
	try:
		with open(file_path,"r",encoding = 'utf-8')as f:
			donne = json.load(f)
	except:
		donne = dict()
	return donne

def get_session():
	import requests
	return requests.Session()

def add_image_box_as_but(mother,img,txt,press_fonc,but_info,
	font_size = '10sp',txt_height = .2,text_color = None,
	size_hint = (1,1),size = (100,100)):
	Clock.schedule_once(partial(_add_image_box_as_but,
		mother,img,txt,press_fonc,but_info,
		font_size,txt_height,text_color,
		size_hint,size))

def _add_image_box_as_but(mother,img,txt,press_fonc,but_info,
	font_size,txt_height,text_color,size_hint,
	size,dt):
	img_h = 1-txt_height
	if not text_color:
		text_color = mother.sc.text_col1
	f = float_l(mother,radius = dp(10),
		bg_color = mother.sc.aff_col3,size_hint = size_hint)
	b = box(mother,padding = dp(10),height = size[1],
		size_hint = (1,None))
	f = Get_border_surf(mother,f,mother.sc.orange,
		width = size[0],height = size[1])
	f.add_surf(b)
	f.add_button("",bg_color = None,on_press = press_fonc,
		info = but_info)
	
	b.add_image(img,size_hint = (1,img_h))

	b.add_text(txt,halign = 'center',size_hint = (1,txt_height),
		text_color = text_color, font_size = font_size)


# Gestion du dossier de stockage
from kivy.utils import platform
from kivy.app import App

def get_storage_dir(app_name="zoecorp"):
	if platform == "android":
		try:
			from jnius import autoclass
			pythonactivity = autoclass('org.kivy.android.PythonActivity')
			activity = pythonactivity.mActivity
			file = activity.getExternalFilesDir(None)
			if file == None:
				return ''
			base_path = file.getAbsolutePath()
		except:
			print(traceback.format_exc())
			base_path = ''
	else:
		base_path = os.path.join(os.path.expanduser("~"), f".{app_name}")

	os.makedirs(base_path, exist_ok=True)
	return base_path


