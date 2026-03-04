#Coding:utf-8
"""
	Le main de la gestion des données
"""
from ..serveur.main import data_main
from .bridge import bridge
from lib.davbuild import *

class base_handler(bridge):
	from .base_table import (formatage,get_data,save_data,delete_data,
		update_data,get_history)

	def __init__(self,screen):
		self.sc = screen
		data_main.Get_path = self.sc.Get_path
		data_main.Save_local = self.sc.Save_local
		data_main.Get_local = self.sc.Get_local

		data_main.get_today = self.sc.get_today
		data_main.get_hour = self.sc.get_hour
		data_main.get_now = self.sc.get_now


		self._data_main_obj = data_main()

		self.Save_image = self._data_main_obj.DB.Save_image
		self._data_main_obj.check_connect = self.check_connect
		#self.check_connect()
		bridge.__init__(self)

	def check_connect(self,*args):
		self._data_main_obj.DB.check_connexion_to_sever()
		self.connected = self._data_main_obj.connected
		return self.connected

	def get_inprogress(self):
		return self._data_main_obj.DB.Sync_in_progress

	def set_inprogesst(self,val:bool):
		self._data_main_obj.DB.Sync_in_progress = val
