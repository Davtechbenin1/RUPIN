#Coding:utf-8
"""
	Cette classe permet maintenant de gérer la connexion entre
	le gestionnaire de service interne et l'application.

	Ici, on envoie et demande des données. Aucun traitement logique
	n'est fait.

	donc coté serveur, nous avons des api qui permette la gestion
	de chaque action-name en fonction du fichier.


	La gestion par magasin permet de préciser le type de donné,
	type de gestion a prendre en compte. Pour les magasins, nous
	avons les données générales disponibles de façon général.
"""
'''
trafic_format = {
	"action":"get" | "save" | "delete" | "update",
	"where":"fichier",
	"id":str(),
	"data":"JSONB",
	"trafic-id":"uuid",
	"date":str(),
	"heure":str()
}
'''
import uuid, datetime, sys, json

def formatage(self,action,where,data = dict(),id = None):
	date = self.sc.get_today()
	trafic = {
		"action":action,
		"where":where.lower(),
		"id":id,
		"data":data,
		"trafic-id":f"{where} {uuid.uuid4()}",
		"date":date,
		"base_name":'rupin',
	}
	ret = self._data_main_obj.message_handler(trafic)
	if ret == True:
		pass
	elif ret:
		if ret.get('status') == "ok":
			dic = ret.get("data")
			return dic
		else:
			raise ValueError(ret.get('message'))
	else:
		return ret

def get_data(self,where,id = None):
	self.th_url = self._data_main_obj.DB.th_url
	self.th_entreprise = self._data_main_obj.DB.th_entreprise
	self.session = self._data_main_obj.DB.session
	local_info = self._data_main_obj._get_from_local(where,id)
	if local_info:
		return local_info
		
	date = self.sc.get_today()
	trafic = {
		"action":"get",
		"where":where.lower(),
		"id":id,
		"data":dict(),
		"trafic-id":f"{where} {uuid.uuid4()}",
		"date":date,
		"base_name":'rupin',
	}
	rep = self.session.put(self.th_url+f"select/{self.th_entreprise}",
		json = json.dumps(trafic))
	if rep.status_code == 200:
		th_dic = rep.json()
		if th_dic.get('status') == "ok":
			dic = th_dic.get('data')
			self._data_main_obj._update_local(where,dic)
			return dic
		else:
			raise ValueError(f"La demande de donnée à échouer {th_dic.get('message')}")
	else:
		raise ConnectionRefusedError('La connexion vers le serveur à échouer')

def save_data(self,where,data):
	return formatage(self,"save",where, data)

def delete_data(self,where,id):
	return formatage(self,"delete", where, id = id)

def update_data(self,where,data,id):
	return formatage(self,"update",where, data,id)

def get_history(self,where, date:str = None):
	return formatage(self,"get-history",where,id = date)


