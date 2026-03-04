#Coding:utf-8

from lib.davbuild import *

class commandes(box):
	def initialisation(self):
		self.padding = [dp(0),dp(10),dp(0),0]
		self.spacing = dp(10)
		self.search_txt = str()

		self.order_status_icons = {
			"livree": {
				"icon": "check-circle",
				"color": (0.18, 0.80, 0.44, 1),
				"montant":0,
			},
			"en_cours": {
				"icon": "progress-clock",
				"color": (1.00, 0.76, 0.03, 1),
				"montant":0,
			},
			"rejetee": {
				"icon": "close-circle",
				"color": (0.85, 0.26, 0.26, 1),
				"montant":0,
			}
		}

		self.menu = {
			'Commandes en cours':self.sc.get_my_presta_cmd_encoure(),
			"Commandes livrées":self.sc.get_my_presta_cmd_livree(),
			"Commandes rejetées":self.sc.get_my_presta_cmd_rejetee(),
		}

		self.size_pos()

	def size_pos(self):
		h = .08
		b = box(self,size_hint = (1,h),
			padding_left = dp(10),
			orientation = "horizontal")
		self.add_surf(b)
		b.add_text('Liste des commandes',size_hint = (.55,1))

		for dic in self.order_status_icons.values():
			ico = dic.get('icon')
			col = dic.get('color')
			mon = dic.get('montant')
			b_ = box(self,size_hint = (.15,1))
			b_.add_icon_but(icon = ico, text_color = col,
				size_hint = (1,.6))
			b_.add_text(self.format_val(mon),size_hint = (1,.4),
				text_color = col,font_size = "9sp",
				halign = 'center')
			b.add_surf(b_)

		self.aff_srf = box(self,size_hint = (1,None),
			spacing = dp(10))

		sc = scroll(self,size_hint = (1,.93),
			radius = [dp(15),dp(15),0,0],
			bg_color = self.sc.aff_col1)
		sc.add_surf(self.aff_srf)
		self.add_surf(sc)

	def Foreign_surf(self):
		self.sc.excecute(self.add_all_menu_cat)

	def add_all_menu_cat(self):
		for cate,liste in self.menu.items():
			#time.sleep(.5)
			Clock.schedule_once(partial(self.add_one_menu_cat,cate,liste),1)
			#self.add_one_menu_cat(cate,liste)
			
	def add_one_menu_cat(self,cate,liste,*args):
		all_b = box(self,size_hint = (.95,None),
			height = self.sc.get_this_height(.27),
			padding = dp(5),
			pos_hint = (.025,0),radius = dp(10),
			bg_color = self.sc.aff_col3)
		self.aff_srf.add_text("",size_hint = (1,None),
			height = dp(10))
		self.aff_srf.add_surf(all_b)
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
		if len(liste) >2:
			liste = liste[:2]
		for dic in liste:
			th_b = box(self,)
			th_b.add_image(dic.get('img'),
				size_hint = (1,.7))
			inf = f"""[b]{dic.get('Désignation')}\n[size=14sp]{self.format_val(dic.get('prix'))}[/b][/size]"""
			th_b.add_text(inf,size_hint = (1,.3),
				halign = 'center')

			tt_f = float_l(self,size_hint = (.5,1),
				)
			tt_f.add_surf(th_b)
			bb = tt_f.add_button('',on_press = self.show_vent_surf,
				bg_color = None)
			bb.categorie = cate
			bb.provenance = dic.get('auteur',str())
			b.add_surf(tt_f)

# Gestion des actions
	def set_search_txt(self,wid,val):
		self.search_txt = val.lower()
		self.add_all()


	def show_search_by(self,wid):
		...




