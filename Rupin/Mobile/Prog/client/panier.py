#Coding:utf-8

from lib.davbuild import *

class panier(box):
	def initialisation(self):
		self.padding = [dp(0),dp(10),dp(0),0]
		self.th_over_l = (1,1,1,.5)
		self.spacing = dp(10)
		self.but_d = {
			"order": {
				"icon": "cart-check",        # valider commande
				"color": (0.13, 0.59, 0.95, 1),
				"fonc":self.set_order,
			},
			"clear": {
				"icon": "cart-remove",       # vider panier
				"color": (0.85, 0.26, 0.26, 1),
				"fonc":self.set_clear,
			}
		}
		self.size_pos()

	def size_pos(self):
		self.clear_widgets()
		h = .08
		b = box(self,size_hint = (1,h),
			bg_color = self.sc.aff_col1,radius = dp(15),
			orientation = "horizontal",
			padding_left = dp(10))

		self.add_surf(b)

		b.add_icon_but(icon = "currency-usd",size_hint = (.1,1),
			text_color = self.sc.text_col3)
		self.montant_surf = b.add_text('0',size_hint = (.5,1),
			text_color = self.sc.text_col1,bold = True,
			italic = True,font_size = "13sp")

		for txt,txt_dic in self.but_d.items():
			ico = txt_dic.get('icon')
			col = txt_dic.get('color')
			fonc = txt_dic.get('fonc')
			th_b = box(self,size_hint = (.2,1))
			th_b.add_icon_but(icon = ico,text_color = col,
				size_hint = (1,.6),on_press = fonc)
			th_b.add_button(txt,font_size = '9sp',
				bg_color = None,on_press = fonc)
			b.add_surf(th_b)

		self.aff_srf = box(self,size_hint = (1,None),
			spacing = dp(10),padding = dp(10)
			)

		sc = scroll(self,size_hint = (1,.93),
			radius = [dp(20),dp(20),0,0],
			bg_color = self.sc.aff_col3)
		sc.add_surf(self.aff_srf)
		self.add_surf(sc)

	def Foreign_surf(self):
		self.size_pos()
		self.my_panier = self.sc.get_panier()
		self.montant_surf.text = self.format_val(self.get_montant_panier())

		self.add_aff_srf()

	def get_montant_panier(self):
		m = float()
		for dic in self.my_panier.values():
			m += dic.get('montant')
		return m

	def add_aff_srf(self):
		self.aff_srf.clear_widgets()
		self.get_this_infos()
		
	def get_this_infos(self):
		menu_list = list(self.sc.get_panier().values())
		if menu_list:
			self.sc.excecute(self.proceed_to,menu_list)
		else:
			self.aff_srf.add_text("Votre panier est vide pour le moment",
				halign = 'center')

	def proceed_to(self,menu_list):
		for dic in menu_list:
			print(dic)
			Clock.schedule_once(partial(self.one_content,dic),.01)


	def one_content(self,dic,*args):
		inf = f"Qté : [b]{dic.get('qte')}[/b]     PVU : [b][i]{dic.get('PVU')}[/b][/i]     Mont : [b]{dic.get('montant')}[/b]"
		img = dic.get('img')
		if not img:
			img = 'media/logo.png'
		b = float_l(self,size_hint = (1,None),
			height = self.sc.get_this_height(.4),
			bg_color = self.sc.aff_col1,
			radius = dp(10))
		b_ = box(self,radius = dp(10),
			
			padding = [dp(5),dp(5),dp(5),0],
			)
		b_.add_image(img,radius = dp(20),
			size_hint = (1,.8))
		b_.add_text(dic.get('désignation'),
			halign = 'center',size_hint = (1,.1),
			font_size = '13sp',bold = True)
		b_.add_text(inf,strip = False,shorten = True,
			size_hint = (1,.1),halign = "center")
		b.add_surf(b_)
		b.add_button('',bg_color = None,
			on_press = self.modif_info,
			info = dic.get('N°'))
		self.aff_srf.add_surf(b)

# Gestion des actions
	def set_order(self,wid):
		self.sc.add_refused_error("Commandes en cours d'envoie")
		self.sc.excecute(self._begin_order_)

	def _begin_order_(self):
		all_dic = dict()
		for dic in self.my_panier.values():
			prest_id = dic.get('prestataire')

			th_pres_d = all_dic.setdefault(prest_id,{
					"client":self.sc.get_this_user().get('N°'),
					"prestataire":prest_id,
					"montant":int(),
					'menus':dict()
				})
			th_pres_d['montant'] += float(dic.get('montant'))
			th_pres_d['menus'][dic.get('N°')] = dic
			all_dic[prest_id] = th_pres_d
		for cmd in all_dic.values():
			self.sc.DB.save_commande(cmd)

		self.sc.clear_panier()
		Clock.schedule_once(self._end_order_)

	def _end_order_(self,*args):
		self.add_all()
		try:
			self.close_modal()
		except:
			...

	def set_clear(self,wid):
		self.sc.clear_panier()
		self.add_all()

	def _add_to_panier_(self,dic):
		self.sc.add_to_panier(dic)
		self.close_modal()
		self.add_all()

	def modif_info(self,wid):
		srf = _th_panier_srf(self)
		srf.my_ident = wid.info
		srf.confirme_fonc = self._add_to_panier_
		srf.add_all()
		self.add_modal_surf(srf,size_hint = (.94,.4),
			pos_hint = {"x":.03,"y":.35},
			titre = "Quantité",overlay_color = self.th_over_l)

class add_to_panier_srf(stack):
	def initialisation(self):
		self.menu_ident = str()
		self.padding = dp(10)

		self.th_over_l = (1,1,1,.5)

	def Foreign_surf(self):
		if self.menu_ident:
			h = .065
			self.article_dic = self.sc.DB.get_menus(self.menu_ident)
			if self.article_dic:
				f = float_l(self,size_hint = (1,.3))
				f.add_image(self.article_dic.get('img'),
					)
				f.add_text("x x x x x",text_color = self.sc.text_col3,
					size_hint = (1,.2),padding_left = dp(10))
				self.add_surf(f)

				prest = self.article_dic.get('prestataire')
				self.prest_dic = self.sc.DB.get_users(prest)

				dic = {
					"Localité":self.prest_dic.get('adresse',"Non définie"),
					"Prestataire":self.prest_dic.get('nom') + ' ' + self.prest_dic.get('prénom'),
				}
				dic2 = {
					"Prix":self.format_val(self.article_dic.get('prix')),
					"Cuisson":self.article_dic.get('temps de cuisson')
				}
				self.add_text(self.article_dic.get('désignation'),
					text_color = self.sc.text_col1,halign = 'center',
					font_size = "13sp",bold = True,size_hint = (1,h))
				for key,val in dic.items():
					self.add_text(key,size_hint = (1,h*.8),
						padding_left = dp(10),
						valign = "bottom",
						text_color = self.sc.text_col3)
					self.add_text(val,size_hint = (1,h*.9),
						padding_left = dp(10),
						padding_bottom = dp(5),
						text_color = self.sc.text_col1,
						valign = "bottom")
					self.add_text("",size_hint = (1,None),
						height = dp(1),bg_color = self.sc.sep)
				for key,val in dic2.items():
					b = box(self,size_hint = (.48,h*1.7))
					b.add_text(key,size_hint = (1,.45),
						padding_left = dp(10),
						valign = "bottom",
						text_color = self.sc.text_col3)
					b.add_text(val,size_hint = (1,.55),
						padding_left = dp(10),
						padding_bottom = dp(5),
						text_color = self.sc.text_col1,
						valign = "bottom")
					b.add_text("",size_hint = (1,None),
						height = dp(1),bg_color = self.sc.sep)
					self.add_surf(b)
					self.add_padd((.02,h))

				self.add_padd((1,h*.8))
				but_d = {
					"Panier":('plus',self.add_panier,self.sc.text_col1),
					"Achat":("cart-check",self.buy_menu,self.sc.vert)
				}
				for txt,tup in but_d.items():
					ico,fonc,col = tup
					b1 = box(self,size_hint = (.48,h),
						orientation = 'horizontal',
						bg_color = self.sc.aff_col3,
						radius = dp(20),
						padding_left = dp(10))
					b1.add_icon_but(icon = ico,
						size_hint = (.2,1),info = txt,
						text_color = col,font_size = "22sp",
						on_press = fonc)
					b1.add_button(txt,size_hint = (.8,1),
						info = txt,on_press = fonc,
						font_size = "13sp",
						halign = 'left',text_color = col)
					self.add_surf(b1)
					self.add_padd((.02,h))

# Gestion des actions des bouttons
	def add_panier(self,wid):
		srf = panier_srf(self)
		srf.my_ident = self.article_dic.get('N°')
		srf.confirme_fonc = self._add_to_panier
		srf.add_all()
		self.add_modal_surf(srf,size_hint = (.94,.4),
			pos_hint = {"x":.03,"y":.35},
			titre = "Quantité",overlay_color = self.th_over_l)

	def buy_menu(self,wid):
		srf = panier_srf(self)
		srf.my_ident = self.article_dic.get('N°')
		srf.confirme_fonc = self._save_cmds
		srf.add_all()
		self.add_modal_surf(srf,size_hint = (.94,.4),
			pos_hint = {"x":.03,"y":.35},
			titre = "Quantité",overlay_color = self.th_over_l)


	def _add_to_panier(self,dic):
		self.sc.add_to_panier(dic)

	def _save_cmds(self,dic):
		user_dic = self.sc.get_this_user()
		cmd_dic = {
			'client': user_dic.get('N°'),
			"prestataire":self.prest_dic.get('N°'),
			'menus':{dic.get('N°'):dic},
			"montant":dic.get('montant')
		}
		#print(cmd_dic)
		self.sc.DB.save_commande(cmd_dic)

class panier_srf(stack):
	def initialisation(self):
		self.spacing = dp(10)
		self.padding = dp(10)
		self.qte = 1
		self.confirme_fonc = None
		"""
			confirme_fonc doit accepter le dict du ménu
		"""
		self.my_ident = str()

	def Foreign_surf(self):
		self.clear_widgets()
		h = .2
		if self.my_ident:
			self.article_dic = self.sc.DB.get_menus(self.my_ident)
			self.PVU = float(self.article_dic.get('prix'))
			if self.article_dic:
				b1 = box(self,size_hint = (.5,h*1.7),
					#bg_color = self.sc.aff_col3,
					radius = dp(10),padding_left = dp(10))
				b1.add_text('PVU',text_color = self.sc.text_col3,
					size_hint = (1,.45))
				b1.add_text(self.format_val(self.PVU),
					text_color = self.sc.text_col1,
					size_hint = (1,.55))

				self.add_surf(b1)

				b2 = box(self,size_hint = (.5,h*2),
					bg_color = self.sc.aff_col3,
					radius = dp(10),padding_left = dp(10))
				b2.add_text('Montant',text_color = self.sc.text_col3,
					size_hint = (1,.45))
				self.montant_srf = b2.add_text(self.format_val(self.PVU),
					text_color = self.sc.text_col1,
					size_hint = (1,.55))

				self.add_surf(b2)

				b = box(self,size_hint = (1,h),
					radius = dp(10),bg_color = self.sc.aff_col3,
					orientation = "horizontal",
					padding_left = dp(10),
					padding_right = dp(10))

				self.inp_srf = b.add_input('qte',
					text_color = self.sc.text_col1,
					size_hint = (.7,1),padding_left = dp(10),
					on_text = self.set_qte,
					bg_color = self.sc.aff_col3,
					placeholder = '0',
					padding_top = dp(13),
					default_text = str(self.qte))

				b.add_icon_but(icon = 'minus',size_hint = (.15,1),
					text_color = self.sc.red,on_press = self.sub_from,
					font_size = "23sp")

				b.add_icon_but(icon = 'plus',size_hint = (.15,1),
					text_color = self.sc.vert,on_press = self.add_to,
					font_size = "23sp")
				self.add_surf(b)

				self.add_padd((.25,h))
				self.add_button('Confirmer',
					text_color = self.sc.vert,
					bg_color = self.sc.aff_col3,
					on_press = self.valide_info,
					size_hint = (.5,h))
				self.add_padd((.25,h))

# Gestion des actions des bouttons
	def set_qte(self,wid,val):
		wid.text = self.regul_input(wid.text)
		self.qte = int(wid.text)

		self.montant_srf.text = self.format_val(self.qte * self.PVU)

	def add_to(self,wid):
		txt = int(self.regul_input(self.inp_srf.text))
		txt += 1
		self.inp_srf.text = str(txt)

	def sub_from(self,wid):
		txt = int(self.regul_input(self.inp_srf.text))
		txt -= 1
		if txt < 0:
			txt = 0
		self.inp_srf.text = str(txt)


	def valide_info(self,wid):
		inf_dic = {
			"N°":self.article_dic.get("N°"),
			"qte":self.qte,
			"PVU":self.PVU,
			"désignation":self.article_dic.get('désignation'),
			"img":self.article_dic.get('img'),
			"montant":float(self.regul_input(self.montant_srf.text)),
			"prestataire":self.article_dic.get('prestataire')
		}
		if self.confirme_fonc:
			self.confirme_fonc(inf_dic)

		self.mother.close_modal()
		self.mother.mother.close_modal()
		#self.sc.add_refused_error("Opération réussi!")

				
class _th_panier_srf(panier_srf):
	def valide_info(self,wid):
		inf_dic = {
			"N°":self.article_dic.get("N°"),
			"qte":self.qte,
			"PVU":self.PVU,
			"désignation":self.article_dic.get('désignation'),
			"img":self.article_dic.get('img'),
			"montant":float(self.regul_input(self.montant_srf.text)),
			"prestataire":self.article_dic.get('prestataire')
		}
		if self.confirme_fonc:
			self.confirme_fonc(inf_dic)

		self.mother.close_modal()



