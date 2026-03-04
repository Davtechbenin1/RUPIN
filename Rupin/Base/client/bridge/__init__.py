#Coding:utf-8
"""
	Ici, on regroupe les méthodes servant de pont de chaque
	module de gestion de la base de donnée
"""
class bridge:
	def __init__(self):
		self.general_fic = "general"
		self.user_fic = "users"
		self.menu_fic = "menus"
		self.categorie_fic = 'categories'
		self.commande_fic = 'commandes'
		self.livraison_fic = 'livraisons'

# Gestion des Commandes
	def get_commandes(self,ident = None):
		all_commande = self.get_data(self.commande_fic)
		if ident:
			return all_commande.get(ident)
		return all_commande

	def save_commande(self,dic):
		return self.save_data(self.commande_fic,dic)

	def update_commande(self,dic):
		id = dic.get("N°")
		if id:
			return self.update_data(self.commande_fic,dic,id)
		else:
			return self.save_commande(dic)

	def delete_commande(self,ident):
		return self.delete_data(self.commande_fic,ident)

# Gestion des catégories
	def get_categories(self,ident = None):
		all_categorie = self.get_data(self.categorie_fic)
		if ident:
			return all_categorie.get(ident)
		return all_categorie

	def get_categories_list(self):
		return [i.get('nom') for i in self.get_categories().values()]

	def get_categorie_by_name(self, name):
		all_cate = self.get_categories().values()
		for dic in all_cate:
			if dic.get('nom').lower() == name.lower():
				return dic
		return None

	def save_categorie(self,dic):
		return self.save_data(self.categorie_fic,dic)

	def update_categorie(self,dic):
		id = dic.get("N°")
		if id:
			return self.update_data(self.categorie_fic,dic,id)
		else:
			return self.save_categorie(dic)

	def delete_categorie(self,ident):
		return self.delete_data(self.categorie_fic,ident)

	
# Gestion des Users
	def get_users(self,ident = None):
		all_user = self.get_data(self.user_fic)
		if ident:
			return all_user.get(ident)
		return all_user

	def save_user(self,dic):
		return self.save_data(self.user_fic,dic)

	def get_users_by_num(self,num):
		all_user = self.get_users()
		for dic in all_user.values():
			if dic.get('téléphone') == num:
				return dic
		return dict()

	def update_user(self,dic):
		id = dic.get("N°")
		if id:
			return self.update_data(self.user_fic,dic,id)
		else:
			return self.save_user(dic)

	def delete_user(self,ident):
		return self.delete_data(self.user_fic,ident)

# Gestion des menus:
	def get_menus(self,ident = None):
		all_menu = self.get_data(self.menu_fic)
		if ident:
			return all_menu.get(ident)
		return all_menu

	def save_menu(self,dic):
		return self.save_data(self.menu_fic,dic)

	def update_menu(self,dic):
		id = dic.get("N°")
		if id:
			return self.update_data(self.menu_fic,dic,id)
		else:
			return self.save_menu(dic)

	def delete_menu(self,ident):
		return self.delete_data(self.menu_fic,ident)





