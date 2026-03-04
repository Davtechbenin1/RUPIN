#Coding:utf-8
"""
	Gestion de la base Local distant
"""
from kivy.core.window import Window
import os, time, sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
import websocket, json, threading, time, sys, uuid
from kivy.uix.modalview import ModalView
import traceback,string
import functools

from lib.davbuild import *

def TH_CACHE(fonc_origin):
	@functools.wraps(fonc_origin)
	def wrapper(*args,**kwargs):
		self = args[0]
		try:
			return fonc_origin(*args,**kwargs)
		#"""
		except Exception as E:
			error = traceback.format_exc()
			error_log(error)
			Clock.schedule_once(self.set_error_mess,.1)
		#"""
	return wrapper

def set_error_mess(self,*args):
	self.sc.add_refused_error("Erreur Réseau, Opération échoué. Veillez vérifier votre connexion!")

def on_message(self, ws, message):
	msg = json.loads(message)
	status = msg.get('status')
	##print(msg)
	try:
		if status == 'ok':
			action = msg.get('action')
			trafic = msg.get('data')
			
			if action == "subscribe":
				return

			where = msg.get('where')

			if action in ("save","update"):
				#print("trafic\n",trafic)
				#print('___________\n')
				if "_z_o_e_" in where:
					where = where.split("_z_o_e_")[1]
				print(where,trafic)
				where_dic = self.sc._local_cache.setdefault(where,dict())
				where_dic[trafic.get('N°')] = trafic
				self.sc._local_cache[where] = where_dic
				
			elif action == "delete":
				where_dic = self.sc._local_cache.setdefault(where,dict())
				id = trafic.get('N°')
				if id in where_dic:
					where_dic.pop(id)
					self.sc._local_cache[where] = where_dic

			#print('-------------')
			#print(self.sc._local_cache)
			#print('-------------')
		
		else:
			self.Sync_in_progress = False
			print(msg)
	except:
		format_exc = traceback.format_exc()
		#print(format_exc)
		self.Sync_in_progress = False



def on_open(self, ws):
	ws.send(json.dumps({"action":"subscribe", 
		'base_name':self.th_entreprise}))

# Obtenir le backup
#@TH_CACHE
def local_backup(self):
	if self.th_entreprise:
		headers = {"Accept":"application/zip"}
		
		with self.session.post(self.th_url+f'backup/{self.th_entreprise}',
			headers = headers,stream = True, timeout = 300) as r:
			r.raise_for_status()
			now = self.sc.get_hour()
			now = now.replace(":","_")
			file_name = 'Last_Backup'+now+'.zip'
			ppp = Path(f"backup/{self.sc.real_date()}")
			os.makedirs(ppp, exist_ok=True)
			out_put = os.path.join(ppp,file_name)
			with open(out_put,"wb") as f:
				for chunk in r.iter_content(chunk_size = 1024*1024):
					if chunk:
						f.write(chunk)

class WSClient:
	connected = False
	def __init__(self,mother , ws, entreprise):
		"""
		ws : instance websocket (ex: websocket-client)
		entreprise : nom de l'entreprise pour base_name
		"""
		self.ws = ws
		self.th_entreprise = entreprise

		# Cache local
		self.mother = mother
		self.All_data_Table = dict()

		# Dict pour stocker les réponses en attente
		self._responses = {}  # request_id -> data
		self._responses_lock = threading.Lock()
		self._lock = threading.Lock()
		self._lock_bases = dict()
		self._pending = {}        # request_id -> Event
		self._pending_lock = threading.Lock()

		# Start listener WS
		#self._listener_thread = threading.Thread(target=self._listen, daemon=True)
		#self._listener_thread.start()

	# -------------------------
	# Utilitaires
	# -------------------------
	def uuid(self):
		return str(uuid.uuid4())

	def redo_ident(self, ident):
		"""Méthode pour standardiser les identifiants"""
		if ident:
			p = "1234567890_"+string.ascii_lowercase
			th_txt = str()
			for i in ident.lower():
				if i not in p:
					i = "xx"
				th_txt += i
			return th_txt
		return None
