#Coding:utf-8
"""
	Moteur de gestion des données
"""
import sys
def manage_my_presta_commande(self):
	self.User_dict = self.sc.get_this_user()
	cmds = self.User_dict.get('commandes').keys()

	self.my_presta_cmd = dict()
	self.my_presta_cmd_encoure = dict()
	self.my_presta_cmd_livrer = dict()
	self.my_presta_cmd_rejetee = dict()

	self.my_client_cmd = dict()
	self.my_client_cmd_encoure = dict()
	self.my_client_cmd_livrer = dict()
	self.my_client_cmd_rejetee = dict()

	for ident in cmds:
		cmd = self.sc.get_commandes(ident)
		if cmd.get("prestataire") == self.User_dict.get('N°'):
			self.my_presta_cmd[cmd.get('N°')] = cmd
			if cmd.get('status').lower() == 'livrée':
				self.my_presta_cmd_livrer[cmd.get('N°')] = cmd
			elif cmd.get('status').lower == "rejetée":
				self.my_presta_cmd_rejetee[cmd.get('N°')] = cmd
			else:
				self.my_presta_cmd_encoure[cmd.get('N°')] = cmd

		if cmd.get("client") == self.User_dict.get('N°'):
			self.my_client_cmd[cmd.get('N°')] = cmd
			if cmd.get('status').lower() == 'livrée':
				self.my_client_cmd_livrer[cmd.get('N°')] = cmd
			elif cmd.get('status').lower == "rejetée":
				self.my_client_cmd_rejetee[cmd.get('N°')] = cmd
			else:
				self.my_client_cmd_encoure[cmd.get('N°')] = cmd

def get_my_presta_cmd_encoure(self):
	try:
		return self.my_presta_cmd_encoure
	except AttributeError:
		return dict()

def get_my_presta_cmd_livree(self):
	try:
		return self.my_presta_cmd_livrer
	except AttributeError:
		return dict()

def get_my_presta_cmd_rejetee(self):
	try:
		return self.my_presta_cmd_rejetee
	except AttributeError:
		return dict()
# -----------------------------------------------

def get_my_client_cmd_encoure(self):
	try:
		return self.my_client_cmd_encoure
	except AttributeError:
		return dict()

def get_my_client_cmd_livree(self):
	try:
		return self.my_client_cmd_livrer
	except AttributeError:
		return dict()

def get_my_client_cmd_rejetee(self):
	try:
		return self.my_client_cmd_rejetee
	except AttributeError:
		return dict()

def get_my_client_cmd(self):
	try:
		return self.my_client_cmd
	except AttributeError:
		return dict()

# Clarrification des ménus
def manage_menu(self):
	all_menu = self.sc.DB.get_menus().values()
	menu_part_cate = dict()
	for menu_d in all_menu:
		cat = menu_d.get('catégorie')
		cate_d = self.sc.DB.get_categories(cat)
		if not cate_d:
			cate_d = self.sc.DB.get_categorie_by_name(cat)

		if cate_d:
			cat_name = cate_d.get('nom')
			cate_dic = menu_part_cate.setdefault(cat_name,list())
			cate_dic.append(menu_d)
	return menu_part_cate





