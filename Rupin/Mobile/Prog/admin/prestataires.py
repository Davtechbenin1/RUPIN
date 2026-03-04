#Coding:utf-8

from lib.davbuild import *

class prestataires(box):
	def initialisation(self):
		self.padding = [dp(10),dp(10),dp(10),0]
		self.spacing = dp(10)
		self.search_txt = str()
		self.part_txt = "En attentes"
		self.part_txt_list = ["Actifs","Non actifs","En attentes"]
		self.size_pos()

	def size_pos(self):
		h = .07
		b = Get_border_surf(self,box(self,size_hint = (1,h),
			bg_color = self.sc.aff_col3,radius = dp(15),
			orientation = "horizontal"),
		self.sc.aff_col3)
		b.add_icon_but(icon = "magnify",size_hint = (.1,1),
			)
		b.add_input("recherche",size_hint = (.5,1),
			on_text = self.set_search_txt,bg_color = None,
			placeholder = "rechercher dans", 
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

	def add_aff_srf(self):
		self.aff_srf.clear_widgets()
		th_list = self.get_this_infos()
		for dic in th_list :
			b = float_l(self,size_hint = (.5,None),
				height = self.sc.get_this_height(.2))
			b_ = box(self)
			b_.add_image(dic.get('img'),
				size_hint = (1,.7))
			b_.add_text(dic.get('info'),
				size_hint = (1,.3))
			b.add_surf(b_)
			self.aff_srf.add_surf(b)

		if not th_list:
			self.aff_srf.add_text(f"Aucune donnée ne correspond à \n'{self.search_txt}' dans [b]{self.part_txt}[/b]",
				halign = 'center',)


	def get_this_infos(self):
		"""
			Recherche et renvoie les informations en fonction
			du trie de recherche
		"""
		return list()



# Gestion des actions
	def set_search_txt(self,wid,val):
		self.search_txt = val.lower()
		self.add_all()

	def set_part_txt(self,info):
		self.part_txt = info
		self.add_all()



