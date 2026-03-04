#Coding:utf-8
from .connexion import local
import uuid, datetime, sys, json

from lib.serveur.DAV_BASE.MyData import date_obj

from lib.davbuild import get_storage_dir,os

from . import (Base_table)

class data_main(local):
	def __init__(self):
		self.date_format = "%d-%m-%Y"

		self.base_dir = get_storage_dir("RUPIN")
		self.db_path = os.path.join(self.base_dir, "nanabinze.db")

		self._local_cache = dict()
		self._lock_dict = dict()
		self.created_table = set()
		self.connected = False
		self.sc = self
		self.DB = Base_table(self)

	def message_handler(self,msg):
		#print('______________')
		#print(msg)
		return self.DB.msg_handler(msg)


# Obtenir toutes les informations d'un coup
	def get_all_base(self):
		dic = {
			"base_name":self.th_entreprise,
			'where':["users","menus"],
			'id':str(),
			'date':str(),
		}
		ret = self.session.put(self.th_url+f"select/{self.th_entreprise}",
			json = json.dumps(dic))
		if ret.status_code == 200:
			th_dic = ret.json()
			if th_dic.get('status') == "ok":
				self.update_local_from_all(th_dic.get('data'))

		return ret

	def update_local_from_all(self,dic):
		for part,part_dic in dic.items():
			where = part.split("_z_o_e_")[1]
			self._local_cache[where] = {d.get('N°'):d 
				for d in part_dic.values()}

	def _update_local(self,part,dic):
		th_dic = self._local_cache.setdefault(part,dict())
		th_dic.update({d.get('N°'):d for d in dic.values()})
		self._local_cache[part] = th_dic

	def _get_from_local(self,part,ident):
		part_dic = self._local_cache.setdefault(part,dict())
		#print(part,ident,part_dic,sep = '--->')
		if not part_dic:
			return False
		else:
			if ident:
				return part_dic.get(ident)
			else:
				return part_dic



