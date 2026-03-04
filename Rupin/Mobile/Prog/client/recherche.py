#Coding:utf-8

from lib.davbuild import *

class recherche(box):
	def initialisation(self):
		self.padding = [dp(10),dp(10),dp(10),0]
		self.spacing = dp(10)
		self.search_txt = str()
		self.curent_base = dict()
		self.part_txt = "Menus"
		self.part_txt_list = ["Restaurants","Catégories","Menus"]
		self.set_curent_base()
		self.size_pos()

	def size_pos(self):
		h = .07
		self.clear_widgets()
		b = Get_border_surf(self,box(self,size_hint = (1,h),
			bg_color = self.sc.aff_col3,radius = dp(15),
			orientation = "horizontal"),
		self.sc.aff_col3)
		b.add_icon_but(icon = "magnify",size_hint = (.1,1),
			)
		b.add_input("recherche",size_hint = (.5,1),
			on_text = self.set_search_txt,bg_color = None,
			placeholder = "rechercher dans",
			padding = [dp(0),dp(13),0,dp(0)],
			default_text = self.search_txt)
		b.add_surf(liste_set(self,self.part_txt,self.part_txt_list,
			mother_fonc = self.set_part_txt,size_hint = (.4,1)))
		
		self.aff_srf = box(self,size_hint = (1,None),
			spacing = dp(10),
			)

		sc = scroll(self,size_hint = (1,.93),
			radius = [dp(15),dp(15),0,0],
			bg_color = self.sc.aff_col3)
		sc.add_surf(self.aff_srf)
		self.add_surf(sc)

	def Foreign_surf(self):
		self.add_aff_srf()

	def proceed_to(self,menu_list):
		for dic in menu_list:
			if self.part_txt in ("Menus","Catégories"):
				Clock.schedule_once(partial(self.menu_content,dic),.01)
			elif self.part_txt == "Restaurants":
				Clock.schedule_once(partial(self.user_content,dic),.01)

	def menu_content(self,dic,*args):
		inf = f"Prix : [b]{dic.get('prix')}[/b]\t \t dispo : [b][i]{dic.get('temps de cuisson')}[/b][/i]"
		img = dic.get('img')
		if not img:
			img = 'media/logo.png'
		b = float_l(self,size_hint = (.5,None),
			height = self.sc.get_this_height(.3))
		b_ = box(self,radius = dp(10),
			bg_color = self.sc.aff_col3,
			padding = [dp(5),dp(5),dp(5),0])
		b_.add_image(img,radius = dp(20),
			size_hint = (1,.65))
		b_.add_text(dic.get('désignation'),
			halign = 'center',size_hint = (1,.2),
			font_size = '13sp',bold = True)
		b_.add_text(inf,strip = False,shorten = True,
			size_hint = (1,.15))
		b.add_surf(b_)
		b.add_button('',bg_color = None,
			on_press = self.show_vent_surf,
			info = dic.get('N°'))
		self.aff_srf.add_surf(b)

	def user_content(self,dic,*args):
		inf = self.sc.set_curent_adresse(dic.get("adresse"))
		nom = f"{dic.get('nom')} {dic.get('prénom')}".strip()
		img = dic.get('img')
		if not img:
			img = 'media/logo.png'
		b = float_l(self,size_hint = (.5,None),
			height = self.sc.get_this_height(.3))
		b_ = box(self,radius = dp(10),
			bg_color = self.sc.aff_col3,
			padding = [dp(5),dp(5),dp(5),0])
		b_.add_image(img,radius = dp(20),
			size_hint = (1,.65))
		b_.add_text(nom,
			halign = 'center',size_hint = (1,.2),
			font_size = '13sp',bold = True)
		b_.add_text(inf,strip = False,shorten = True,
			size_hint = (1,.15))
		b.add_surf(b_)
		b.add_button('',bg_color = None,
			on_press = self.show_menu_of,
			info = dic.get('N°'))
		self.aff_srf.add_surf(b)

	def add_aff_srf(self):
		self.aff_srf.clear_widgets()
		th_list = self.get_this_infos()
		if th_list:
			self.sc.excecute(self.proceed_to,th_list)
		else:
			self.aff_srf.add_text('Aucune donnée ne correspond à votre recherche actuelle', 
				halign = 'center')

	def get_this_infos(self):
		lis = list()
		if self.part_txt == "Menus":
			for dic in self.curent_base:
				if self.search_txt.lower() in dic.get('désignation').lower():
					lis.append(dic)
		elif self.part_txt == "Restaurants":
			for dic in self.curent_base:
				nom = f"{dic.get('nom')} {dic.get('prénom')}".strip()
				if self.search_txt.lower() in nom.lower():
					lis.append(dic)
		elif self.part_txt == "Catégories":
			for dic in self.curent_base:
				cate = dic.get('catégories')
				cate_dic = self.sc.DB.get_categories(cate) or self.sc.DB.get_categorie_by_name(cate)
				if cate_dic:
					if self.search_txt.lower() in cate_dic.get('nom').lower():
						lis.append(dic)
		return lis

	def set_curent_base(self):
		if self.part_txt == "Menus":
			self.curent_base = self.sc.DB.get_menus().values()
		elif self.part_txt == 'Restaurants':
			users = self.sc.DB.get_users().values()
			#print(list(users))
			self.curent_base = [i for i in users if 
				i.get('role').lower() == "prestataire"]
		elif self.part_txt == "Catégories":
			self.curent_base = self.sc.DB.get_menus().values()

# Gestion des actions
	def set_search_txt(self,wid,val):
		self.search_txt = val.lower()
		self.add_all()

	def set_part_txt(self,info):
		self.part_txt = info
		self.set_curent_base()
		self.add_all()

	def show_vent_surf(self,wid):
		from .panier import add_to_panier_srf
		srf = add_to_panier_srf(self)
		srf.menu_ident = wid.info
		srf.add_all()
		self.add_modal_surf(srf,radius = dp(1),
			titre = 'Détails du ménu')

	def show_menu_of(self,wid):
		srf = menu_of_this_prest(self)
		srf.add_all()
		rest_d = self.sc.DB.get_users(wid.info)
		rest_name = f"{rest_d.get('nom')} {rest_d.get('prénom')}".strip()
		self.add_modal_surf(srf,radius = dp(1),
			titre = f'Ménu du resto {rest_name}')

class menu_of_this_prest(recherche):
	def initialisation(self):
		self.padding = [dp(10),dp(10),dp(10),0]
		self.spacing = dp(10)
		self.search_txt = str()
		self.curent_base = dict()
		self.part_txt = "Menus"
		self.part_txt_list = ["Restaurants","Catégories","Menus"]
		self.set_curent_base()
		self.size_pos()

	def size_pos(self):
		h = .07
		self.clear_widgets()
		b = Get_border_surf(self,box(self,size_hint = (1,h),
			bg_color = self.sc.aff_col3,radius = dp(15),
			orientation = "horizontal"),
		self.sc.aff_col3)
		b.add_icon_but(icon = "magnify",size_hint = (.1,1),
			)
		b.add_input("recherche",size_hint = (.9,1),
			on_text = self.set_search_txt,bg_color = None,
			placeholder = "rechercher dans",
			padding = [dp(0),dp(13),0,dp(0)],
			default_text = self.search_txt)
		
		self.aff_srf = box(self,size_hint = (1,None),
			spacing = dp(10),
			)

		sc = scroll(self,size_hint = (1,.93),
			radius = [dp(15),dp(15),0,0],
			bg_color = self.sc.aff_col3)
		sc.add_surf(self.aff_srf)
		self.add_surf(sc)

	def get_this_infos(self):
		lis = list()
		for dic in self.curent_base:
			if self.search_txt.lower() in dic.get('désignation').lower():
				lis.append(dic)
	
		return lis


