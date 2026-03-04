#Coding:utf-8
"""
	Gestion de la connexion à distance vers le serveur
	cloud.

	Deux architecture possible:
		- Une en streaming
		- Une en sauvegarde synchroniser.
"""
import os,os.path,json,uuid,traceback,websocket
from lib.davbuild import Clock

def get_sync_dir(self):
	th_base_name = os.path.join(self.base_dir,'SYNC')
	os.makedirs(th_base_name, exist_ok=True)
	return th_base_name

def save_msg_to_sync(self,msg):
	date = self.get_today().replace("-",'')
	sync_dir = self.get_sync_dir()
	general_fic_name = os.path.join(sync_dir,'general.json')
	general_fic_dic = self.get_from(general_fic_name)
	if date not in general_fic_dic:
		general_fic_dic[date]=date
		self.save_to(general_fic_name,general_fic_dic)

	date_fic = os.path.join(sync_dir,f'{date}.gsmart')
	with self._Lock:
		self.save_today_log(date_fic,msg)

def get_msg_from(self,date):
	date = date.replace("-",'')
	sync_dir = self.get_sync_dir()
	date_fic = os.path.join(sync_dir,f'{date}.gsmart')
	return self.get_today_log(date_fic)

def send_all_general_cmds(self,*args):
	sync_dir = self.get_sync_dir()
	general_fic_name = os.path.join(sync_dir,'general.json')
	general_fic_dic = self.get_from(general_fic_name)
	#print(general_fic_dic)
	keys = list(general_fic_dic.keys())

	for date in keys:
		date = date.replace("-",'')
		#print(date)
		sync_dir = self.get_sync_dir()
		date_fic = os.path.join(sync_dir,f'{date}.gsmart')
		
		date_dic = self.get_msg_from(date)
		#print(date_dic)
		request_id = f"{uuid.uuid4()}"
		sync_info = {
			"data":date_dic,
			"date_fic": date_fic,
			"date":date,
			"action":'sync',
			"base_name":self.Get_local("Info_gene"),
			"request_id":request_id
		}
		self.save_request_id(request_id)
		#self.request_id += 1
		
		ret = self.send_to_cloud(sync_info)
		if ret:
			#print(date_fic)
			self.replace_this_(date_fic)
			general_fic_dic.pop(date)
	self.save_to(general_fic_name,general_fic_dic)

def send_to_cloud(self,msg):
	try:
		self.ws_client.ws.send(json.dumps(msg))
		return True
	except:
		print(traceback.format_exc())
		return False

# Gestionnaires des instruction de sauvegarde
def msg_handler(self,msg):
	msg['request_id'] = f"{uuid.uuid4()}"
	return self._msg_handler(msg)

def _msg_handler(self,msg):
	action = msg.get('action')
	if action:
		action = action.lower()
		if 'get' in action:
			self.last_connected_info = self.sc.connected
			if self.sc.connected:

				resp = self.session.put(self.th_url + f"select/{self.th_entreprise}",
					json = msg)
				return resp

		else:
			self.last_connected_info = self.sc.connected
			if self.sc.connected:
				self.save_request_id(msg.get('request_id'))
				try:
					self.ws_client.ws.send(json.dumps(msg))
				except websocket._exceptions.WebSocketConnectionClosedException:
					#self.excecute(self.relance_conexion,msg)
					self.relance_conexion(msg)
	return self.sc.connected

def relance_conexion(self,msg):
	self.sc.check_connect()
	if self.last_connected_info != self.sc.connected:
		self.last_connected_info = self.sc.connected
		self.ws_client.ws.send(json.dumps(msg))
		Clock.schedule_once(self.sc.redef_menu,.01)
	
