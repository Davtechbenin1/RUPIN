#Coding:utf-8
"""
	Gestion de l'interface de l'accueil
"""
from lib.davbuild import *

from .menus import new_menu

class accueil(box):
	def __init__(self,mother,**kwargs):
		kwargs['bg_color'] = mother.sc.aff_col1
		kwargs['size_hint'] = (1,None)
		box.__init__(self,mother,**kwargs)

	def initialisation(self):
		self.User_dict = self.sc.get_this_user()
		self.logo = 'media/logo.png'
		self.where = self.User_dict.get('addresse',"Non définie")
		
		self.commandes = {
			"Commandes en cours":self.get_cmds_list(
				self.sc.get_my_presta_cmd_encoure().values()),
		}

		self.accroch_text = f"""Vos plats sont apprécié et valorisé ici..."""

	def get_cmds_list(self,ident_list):
		return ident_list

	def Foreign_surf(self):
		self.clear_widgets()
		self.add_image(self.logo,size_hint = (1,None),
			height = self.sc.get_this_height(.35))
		bo = box(self,size_hint = (.9,None),
			height = self.sc.get_this_height(.06),
			bg_color = self.sc.aff_col3,
			pos_hint = (.05,0),
			radius = dp(20),orientation = "horizontal")
		bo.add_icon_but(icon = "plus-box",
			on_press = self.show_search,
			size_hint = (None,1),size = (dp(30),1))
		bo.add_button("Ajouter un ménu à votre liste",
			on_press = self.show_search,
			text_color = self.sc.text_col3,
			halign = 'left')
		self.add_surf(bo)

		b = box(self,size_hint = (.9,None),
			height = self.sc.get_this_height(.06),
			orientation = 'horizontal',
			pos_hint = (.05,0))
		b.add_icon_but(icon = "map-marker",
			on_press = self.show_where,
			size_hint = (None,1),size = (dp(30),1))
		b.add_button(f"Je suis à {self.where}",
			on_press = self.show_where,
			text_color = self.sc.text_col3,
			halign = 'left')
		self.add_surf(b)

		self.add_text('',size_hint = (.9,None),
			height = dp(1),bg_color = self.sc.sep,
			pos_hint = (.05,0))

		self.add_text(self.accroch_text,
			text_color = self.sc.text_col1,
			bold = True,size_hint = (1,None),
			height = self.sc.get_this_height(.06),
			halign = 'center')
		self.add_text('',size_hint = (1,None),
			height = dp(1),bg_color = self.sc.sep)

		#self.sc.excecute(self.add_all_menu_cat)
		self.add_all_menu_cat()

	def add_all_menu_cat(self):
		for cate,liste in self.commandes.items():
			#time.sleep(.5)
			#Clock.schedule_once(partial(self.add_one_menu_cat,cate,liste),1)
			self.add_one_menu_cat(cate,list(liste))
			
	def add_one_menu_cat(self,cate,liste,*args):
		all_b = box(self,size_hint = (.95,None),
			height = self.sc.get_this_height(.27),
			padding = dp(5),
			pos_hint = (.025,0),radius = dp(10),
			bg_color = self.sc.aff_col3)
		self.add_text("",size_hint = (1,None),
			height = dp(10))
		self.add_surf(all_b)
		txt_part = box(self,size_hint = (1,.15),
			orientation = 'horizontal',
			)
		txt_part.add_text(cate,size_hint = (.75,1))
		th_b_ = txt_part.add_button('plus',size_hint = (.25,1),
			on_press = self.show_search_by,
			text_color = self.sc.green,
			)
		th_b_.categorie = cate
		all_b.add_surf(txt_part)

		b = stack(self,size_hint = (1,.85),
			)
		all_b.add_surf(b)
		if liste:
			if len(liste) >2:
				liste = liste[:2]
			for dic in liste:
				th_b = box(self,)
				th_b.add_image(dic.get('img'),
					size_hint = (1,.7))
				inf = f"""[b]{dic.get('date')}\n[size=14sp]{self.format_val(dic.get('montant'))}[/b][/size]"""
				th_b.add_text(inf,size_hint = (1,.3),
					halign = 'center')

				tt_f = float_l(self,size_hint = (.5,1),
					)
				tt_f.add_surf(th_b)
				bb = tt_f.add_button('',on_press = self.show_vent_surf,
					bg_color = None)
				bb.categorie = cate
				bb.provenance = dic.get('client',str())
				b.add_surf(tt_f)

# Gestion des actions
	def show_search(self,wid):
		srf = new_menu(self)
		srf.add_all()
		self.add_modal_surf(srf,radius = dp(0),
			titre = "Nouveau ménu")

	def show_search_by(self,wid):
		...

	def show_where(self,wid):
		...

	def show_vent_surf(self,wid):
		...


