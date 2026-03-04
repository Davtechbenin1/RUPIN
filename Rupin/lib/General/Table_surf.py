#Coding:utf-8
from lib.davbuild import *

class th_recycle_item(MyItem):
	def __init__(self,mother, **kwargs):
		kwargs['bg_color'] = mother.sc.sep
		super().__init__(mother,**kwargs)
		self.orientation = "horizontal"
		self.height = dp(50)
		self.padding = [dp(1),dp(0),dp(1),dp(1)]
		self._data_index = -1
		self.recycle_surf_dict = dict()
		#self.spacing = dp(1)

	def Foreign_surf(self,data_dict):
		self.clear_widgets()
		entetes = data_dict.get("entetes")
		data_in = data_dict.get('data')
		wid_l = data_dict.get('wid_l')
		but_fonc = data_dict.get('fonc')
		but_key = data_dict.get('key')
		curent_col = data_dict.get('my_col')

		apply_fonc = data_dict.get('_color_info_')

	#
		if but_fonc:
			for ent,w in zip(entetes,wid_l):
				val = self.format_val(data_in.get(ent))
				info = data_in.get(but_key,str())
				halign = 'left'
				srf = self.recycle_surf_dict.get(ent)
				col = self.sc.text_col1
				if apply_fonc:
					col = apply_fonc(data_in,ent)

				if not srf:
					srf = self.add_button(val,size_hint = (w,1),
						text_color = col,padding_left = dp(5),
						halign = halign,bg_color = curent_col,
						info = info,
						on_press = but_fonc,radius = 0)
					#self.recycle_surf_dict[ent] = srf
				else:
					srf.text = val
					srf.info = info
				
		else:
			for ent,w in zip(entetes,wid_l):
				val = self.format_val(data_in.get(ent))
				halign = 'left'
				srf = self.recycle_surf_dict.get(ent)
				if not srf:
					srf = self.add_text(self.format_val(data_in.get(ent)),size_hint = (w,1),
						text_color = self.sc.text_col1,padding_left = dp(5),
						bg_color = curent_col,halign = halign)
					#self.recycle_surf_dict[ent] = srf
				else:
					srf.text = val
				if apply_fonc:
					srf.color = apply_fonc(data_in,ent)
		
class Table(box):
	def __init__(self,mother,exec_fonc = None,
		exec_key = '',show_ent = True,**kwargs):
		"""
			L'exec_fonc permet de définir une méthode pour
			controler le clique sur les éléments du tableau
		"""
		kwargs['spacing'] = 0
		kwargs['padding'] = dp(1)
		kwargs['radius'] = dp(5)
		kwargs['bg_color'] =None
		box.__init__(self,mother,**kwargs)
		self.exec_fonc = exec_fonc
		self.exec_key = exec_key
		
		self.show_ent = show_ent
		self.select_ed_ecrit = str()

		self.icon_dict = {} 
		self.icon_surf_dict = {}

	def action_but(self,wid):
		pass

	def Get_real_list(self,liste):
		L = liste
		if len(liste)>15:
			L = liste[:15]
		return L

	def this_list(self,This_l,width_liste):
		This_l = self.Sort_infos(This_l)
		num_ord = 1
		for th_obj in This_l:
			th_obj['No'] = str(num_ord)
			num_ord += 1
		my_data_list = list()
		ind = 1
		for dic in This_l:
			bg_col = self.sc.tab1
			if ind == 2:
				bg_col = self.sc.tab2
				ind = 1
			else:
				ind = 2
			#bg_col = self.sc.aff_col1
			th_dic = dict()
			th_dic['entetes'] = self.ent_
			th_dic['data'] = dic
			th_dic['wid_l'] = width_liste
			th_dic['fonc'] = self.exec_fonc
			th_dic['key'] = self.exec_key
			th_dic['my_col'] = bg_col
			th_dic["_color_info_"] = (self.apply_col_fonc)

			my_data_list.append(th_dic)
		return my_data_list

	def Sort_infos(self,liste):
		if self.curent_entete:
			icon = self.icon_dict.get(self.curent_entete)
			if "up" in icon:
				revers = False
			else:
				revers = True
			if liste:
				th_list = list()
				obj = liste[0]
				val = obj.get(self.curent_entete)
				if isinstance(val,str):
					sort_key = "my sort"
					for th_obj in liste:
						th_obj[sort_key] = th_obj.get(self.curent_entete,str()).lower()
				else:
					sort_key = self.curent_entete

				try:
					liste.sort(key = itemgetter(sort_key),reverse = revers)
				except:
					...
		return liste
#
	def Creat_Table(self,width_liste,entete,
		liste_donner,ent_size = (1,.1),force_tire = True,
		not_seen_texte = 'Aucune donnée pour la sélection actuelle',
		ligne_h = None,pos_but_1 = (.95,.9),pos_but_2 = (.95,.005),
		trie_entete = list(),mult = .25,set_num = True,
		apply_col_fonc = None):
		"""
			Méthode à appeler pour le création du tableau. il met à 
			jour les données du tableau de façon automatique après la
			création de l'objet du tableau

			apply_col_fonc doit être une méthode qui prend en 
			compte le dictionnaire et la clé correspondant

			color_key doit être une liste afin de personalisez
			les partis à mettre en couleur
		"""
		self.apply_col_fonc = apply_col_fonc
		
		trie_entete = list(trie_entete)
		th_lllll = ("nom","chargé d'affaire","affiliation",
			"lien d'affiliation","solde","solde actuel",
			"montant ttc","montant payé","montant restant",
			"nombre de jour restant","pénalité","montant réel",
			"auteur","status","Nom du client","montant dû",
			"nombre d'impayé","échéance échus non payé",
			"total à payer ce jours","nom client",)
		for inf in th_lllll:
			if inf in entete:
				trie_entete.append(inf)
		if self.sc.mobile:
			trie_entete = list()
#		
		if entete and isinstance(entete,(list,tuple)):
			entete = list(entete)
			if set_num:
				entete.insert(0,"No")
		if width_liste and isinstance(width_liste,(list,tuple)):
			if "N° d'ordre" in entete:
				entete.remove("N° d'ordre")
			elif set_num:
				width_liste = list(width_liste)
				f_width = width_liste[0]
				num_id = f_width*mult
				f_width = f_width-num_id
				width_liste[0] = f_width
				width_liste.insert(0,num_id)

		self.curent_entete = str()
		self.up_trie_entete(trie_entete)
		if not ligne_h:
			ligne_h = ent_size[1]
		self.wid_l = width_liste
		self.ent_ = entete
		self.ent_size = ent_size
		self.not_seen_texte = not_seen_texte

		self.clear_widgets()

		w_liste = width_liste#
		self.width_liste = width_liste

		WW,HH = ent_size
		det_size = WW,1-HH
		ent_b = box(self,size_hint = ent_size,
			orientation = 'horizontal',bg_color = self.sc.sep,
			padding = dp(1),)#spacing = dp(1))
		This_l = list(liste_donner)
		#if force_tire:
		#	This_l = self.Sort_infos(liste_donner,entete[0])
#
		my_data_list = list()
		ind = 1
		for dic in This_l:
			bg_col = self.sc.tab1
			if ind == 2:
				bg_col = self.sc.tab2
				ind = 1
			else:
				ind = 2
			th_dic = dict()
			th_dic['entetes'] = self.ent_
			th_dic['data'] = dic
			th_dic['wid_l'] = width_liste
			th_dic['fonc'] = self.exec_fonc
			th_dic['key'] = self.exec_key
			th_dic['my_col'] = bg_col
			th_dic["_color_info_"] = (self.apply_col_fonc)

			my_data_list.append(th_dic)

		self.This_l = This_l
		self.decompt = 0
		if not isinstance(trie_entete,(list,tuple)):
			trie_entete = list()
		
		for ent,w in zip(entete,w_liste):
			if ent in trie_entete:
				col = self.sc.black
				if ent == self.curent_entete:
					col = self.sc.red
				b=box(self,orientation= 'horizontal',size_hint=(w,1),
					bg_color = self.sc.aff_col2,)
				obj = b.add_icon_but(icon = self.icon_dict.get(ent), 
					text_color = col,size = (dp(20),dp(20)),
					size_hint = (None,1),on_press = self.trie_info,
					info = ent,
					font_size = '13sp')
				self.icon_surf_dict[ent] = obj
				b.add_text(ent,text_color = self.sc.text_col1,
					)
				ent_b.add_surf(b)
			else:
				ent_b.add_text(ent,size_hint = (w,1),text_color = self.sc.text_col1,
					padding_left = dp(5),strip = True,shorten = False,
					bg_color = self.sc.aff_col2,
					)

		if self.show_ent:
			self.add_surf(ent_b)

		my_data_list = self.this_list(self.This_l,width_liste)
		self.detail_surf = vscroll(self,size_hint = (1,1))
		self.detail_surf.set_viewclass(th_recycle_item)
		
		self.detail_surf.set_data(my_data_list)
		
		if This_l:
			self.add_surf(self.detail_surf)

		if not This_l:
			st_w = stack(self)
			st_w.add_text(not_seen_texte,
				halign = 'center',font_size = '12sp',
				text_color = self.sc.text_col1,italic = True,
				bg_color = self.sc.aff_col1)
			self.add_surf(st_w)

	def trie_info(self,wid):
		if self.curent_entete == wid.info:
			last = self.icon_dict.get(wid.info,"arrow-up")
			obj = self.icon_surf_dict.get(wid.info)
			if last == "arrow-down":
				last = "arrow-up"
			else:
				last = "arrow-down"
			obj.icon = last
			self.icon_dict[wid.info] = last
		else:
			self.curent_entete = wid.info
			for ent,obj in self.icon_surf_dict.items():
				if ent == self.curent_entete:
					obj.color = self.sc.red
				else:
					obj.color = self.sc.black

		my_data_list = self.this_list(self.This_l,self.width_liste)
		self.detail_surf.set_data(my_data_list)

	def up_trie_entete(self,trie_entete):
		for ent in trie_entete:
			if not self.curent_entete:
				self.curent_entete = ent
			last = self.icon_dict.get(ent,"arrow-down")
			if last == "arrow-down":
				last = "arrow-up"
			else:
				last = "arrow-down"
			self.icon_dict[ent] = last
