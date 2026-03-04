#Coding:utf-8

from lib.davbuild import *

class menus(box):
	def initialisation(self):
		self.padding = [dp(10),dp(10),dp(10),0]
		self.spacing = dp(10)
		self.search_txt = str()
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
			placeholder = "recherche ...", 
			padding = [dp(10),dp(12),dp(10),0],
			default_text = self.search_txt)
		b.add_icon_but(icon = "plus-box",size_hint = (.1,1),
			on_press = self.aff_new_menu)
		b.add_button('Ajouter',size_hint = (.2,1),
			on_press = self.aff_new_menu,
			halign = "left",text_color = self.sc.text_col3)

		self.aff_srf = stack(self,size_hint = (1,None),
			spacing = dp(10),padding = dp(10)
			)

		sc = scroll(self,size_hint = (1,.93),
			radius = [dp(15),dp(15),0,0],
			bg_color = self.sc.aff_col1)
		sc.add_surf(self.aff_srf)
		self.add_surf(sc)

	def Foreign_surf(self):
		self.add_aff_srf()

	def add_aff_srf(self):
		self.aff_srf.clear_widgets()
		all_menu = self.sc.get_menu_of_this_prest().values()
		menu_list = list((i for i in all_menu if self.search_txt.lower() 
			in i.get('désignation').lower()))

		if menu_list:
			self.sc.excecute(self.proceed_to,menu_list)
		else:
			#"""
			if self.search_txt:
				self.aff_srf.add_text(f"Aucuns ménus ne correspond à votre recherche \n'{self.search_txt}'",
					halign = 'center',
					size_hint = (1,None),
					height = dp(100))
			else:
				self.aff_srf.add_text(f"Vous ne proposez rien encore sur la plateforme [b]<{self.sc.app_name}>[/b]",
					halign = 'center',
					size_hint = (1,None),
					height = dp(100))
			#"""

	def proceed_to(self,menu_list):
		for dic in menu_list:
			Clock.schedule_once(partial(self.one_content,dic),.01)


	def one_content(self,dic,*args):
		inf = f"Prix : [b]{dic.get('prix')}[/b]     dispo : [b][i]{dic.get('temps de cuisson')}[/b][/i]"
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
			on_press = self.show_art,
			info = dic.get('N°'))
		self.aff_srf.add_surf(b)



# Gestion des actions
	def set_search_txt(self,wid,val):
		self.search_txt = val.lower()
		self.add_all()

	def aff_new_menu(self,*args):
		srf = new_menu(self)
		srf.add_all()
		self.add_modal_surf(srf,radius = dp(0),
			titre = "Nouveau ménu")

	def show_art(self,wid):
		srf = show_th_menu(self)
		men_d = self.sc.DB.get_menus(wid.info)
		srf.menu_dic = men_d
		srf.add_all()
		self.add_modal_surf(srf,radius = dp(1),
			titre = f"Détails du menu {men_d.get('N°')}")

class new_menu(box):
	def initialisation(self):
		self.info = {
			"img":'media/logo.png',
			"Désignation":str(),
			"Prix":str(),
			"Durée de cuisson":str(),
		}
		self.cate_info = str()
		self.cat_list = self.sc.DB.get_categories_list()
		self.curent_cat = ""
		
		self.size_pos()

	def size_pos(self):
		self.clear_widgets()
		self.img_srf = float_l(self,size_hint = (1,.3))
		

		self.add_surf(self.img_srf)
		self.aff_side = stack(self,size_hint = (1,.7),
			padding = dp(10),bg_color = self.sc.aff_col1)
		self.set_img_part()
		self.add_surf(self.aff_side)

	def set_img_part(self,*args):
		self.img_srf.clear_widgets()
		self.img_srf.add_image(self.info.get('img'),
			)
		self.img_srf.add_button("",on_press = self.set_image,
			bg_color = None)

	def Foreign_surf(self):
		h = .1
		self.aff_side.clear_widgets()
		parts = ["Désignation","Prix","Durée de cuisson"]
		for txt in parts:
			val = self.info.get(txt,str())
			self.aff_side.add_text(txt,size_hint = (1,h*.7),
				padding_left = dp(10),valign = 'bottom',
				bg_color = self.sc.aff_col1,
				text_color = self.sc.text_col3)
			self.aff_side.add_input(txt,size_hint = (1,h*.9),
				padding = [dp(10),dp(9),dp(10),0],
				bg_color = self.sc.aff_col1,
				default_text = val,placeholder = txt,
				on_text = self.set_info_part)
			self.aff_side.add_text('',bg_color = self.sc.sep,
				size_hint = (1,None),height = dp(1))

		self.aff_side.add_padd((1,.04))

		self.aff_side.add_padd((.25,h))
		self.aff_side.add_button('Suivant',size_hint = (.5,h),
			bg_color = self.sc.aff_col3,on_press = self.categorie_set)

	def categorie_set(self,*args):
		h = .1
		if not self.check(self.info):
			self.sc.add_refused_error("Toutes les informations sont obligatoires!")
			self.add_all()
			return
		self.aff_side.clear_widgets()
		self.aff_side.add_text("Catégorie",size_hint = (1,h*.7),
			padding_left = dp(10),valign = 'bottom',
			bg_color = self.sc.aff_col1,
			text_color = self.sc.text_col3)
		self.inp_set = self.aff_side.add_input("Catégorie",size_hint = (1,h*.9),
			padding = [dp(10),dp(9),dp(10),0],
			bg_color = self.sc.aff_col1,
			default_text = self.curent_cat,placeholder = "Catégorie",
			on_text = self.trie_categorie)
		self.aff_side.add_text('',bg_color = self.sc.sep,
			size_hint = (1,None),height = dp(1))
		self.liste_derou = liste_deroulante(self,self.curent_cat,
			self.cat_list,mother_fonc = self.set_categorie,
			size_hint = (1,.6))
		self.aff_side.add_surf(self.liste_derou)

		self.aff_side.add_padd((1,.04))
		self.aff_side.add_padd((.25,h))
		self.aff_side.add_button('Terminer',size_hint = (.5,h),
			bg_color = self.sc.aff_col3,on_press = self.th_save_menu)

# Gestion des actions des bouttons
	def set_info_part(self,wid,val):
		if wid.info.lower() == "prix":
			wid.text = self.regul_input(wid.text)
		self.info[wid.info] = wid.text

	def set_image(self,wid):
		self.sc.excecute(self.sc.sys_handler.pick_f,
			self.set_imag_info)

	def set_imag_info(self,path):
		if path:
			self.info['img'] = path
			Clock.schedule_once(self.set_img_part,.1)

	def th_save_menu(self,wid):
		dic = {
			"désignation":self.info['Désignation'],
			"img":self.info['img'],
			"catégorie":self.curent_cat,
			"prix":float(self.info['Prix']),
			"temps de cuisson":self.info['Durée de cuisson'],
			"prestataire":self.sc.get_this_user().get('N°'),
		}
		if self.check(dic):
			self.mother.close_modal()
			self.sc.add_refused_error("Menu ajouter")
			self.sc.excecute(self._th_save_menu,dic)
			
		else:
			self.sc.add_refused_error('Toutes les informations sont obligatoires',
				text_color = self.sc.red)

	def _th_save_menu(self,dic):
		cate_dic = self.sc.DB.get_categorie_by_name(self.curent_cat)
		img_p = self.sc.DB.Save_image(self.info.get('img'))
		dic['catégorie'] = cate_dic.get('N°')
		dic['img'] = img_p
		self.sc.DB.save_menu(dic)
		
		Clock.schedule_once(self.mother.add_all,2)

	def trie_categorie(self,wid,val):
		self.cate_info = val
		liste = [i for i in self.cat_list if val.lower() in i.lower()]

		self.liste_derou.list_info = self.liste_derou.normal_list(liste)
		self.liste_derou.add_all()

	def set_categorie(self,info):
		self.curent_cat = info
		self.inp_set.text = info


class show_th_menu(stack):
	def initialisation(self):
		self.menu_dic = dict()
		self.padding = dp(10)

	def Foreign_surf(self):
		self.clear_widgets()
		h = .07
		if self.menu_dic:
			img = self.menu_dic.get('img')
			if not img:
				img = "media/logo.png"
			f = float_l(self,size_hint = (1,.3))
			f.add_image(img)
			f.add_icon_but(icon = 'pencil',size_hint = (.1,None),
				size = [dp(1),dp(45)],pos_hint = (.8,.1),
				on_press = self.modify_info)
			self.add_surf(f)
			self.add_text(self.menu_dic.get('désignation'),
				text_color = self.sc.text_col1,font_size = '13sp',
				halign = "center",bold = True,size_hint = (1,h))
			self.add_text('Catégorie',text_color = self.sc.text_col3,
				padding_left = dp(10),size_hint = (1,h),valign = 'bottom')
			cate = self.menu_dic.get('catégorie')
			cate_name = self.sc.get_cat_name(cate)
			self.add_text(cate_name,padding_left = dp(10),
				size_hint = (1,h),text_color = self.sc.text_col1,)
			self.add_text('',size_hint = (1,None),height = dp(1),
				bg_color = self.sc.sep)
			dic = {
				"PVU":self.menu_dic.get('prix'),
				"Cuisson":self.menu_dic.get('temps de cuisson')
			}
			for k,v in dic.items():
				b = box(self,size_hint = (.48,h*2),
					padding_left = dp(10))
				b.add_text(k,size_hint = (1,.45),
					text_color = self.sc.text_col3,
					valign = 'bottom')
				b.add_text(v,size_hint = (1,.55),
					text_color = self.sc.text_col1,)
				b.add_text('',size_hint = (1,None),
					height = dp(1),bg_color = self.sc.sep)
				self.add_surf(b)
				self.add_padd((.02,h))

			self.add_text(f"Commandes totals : [size=14sp][b][i]{len(self.menu_dic.get('commandes'))}[/i] cmds[/b][/size]",
				size_hint = (1,h))
			self.add_text('',size_hint = (1,None),height = dp(1),
				bg_color = self.sc.sep)




# Gestion des actions
	def modify_info(self,wid):
		srf = modif_menu(self)
		srf.menu_dic = self.menu_dic
		srf.size_pos()
		srf.add_all()
		self.add_modal_surf(srf,radius = dp(1),
			titre = f"Modification de l'article {self.menu_dic.get('N°')}")


class modif_menu(new_menu):
	def initialisation(self):
		self.info = dict()
		self.menu_dic = dict()

	def size_pos(self):
		self.clear_widgets()
		if self.menu_dic:
			cat_name = self.sc.get_cat_name(self.info.get('catégorie'))
			self.cate_info = str()
			self.cat_list = self.sc.DB.get_categories_list()
			self.curent_cat = cat_name
			self.info = {
				"img":self.menu_dic.get('img'),
				"Désignation":self.menu_dic.get('désignation'),
				"Prix":str(self.menu_dic.get('prix')),
				"Durée de cuisson":self.menu_dic.get("temps de cuisson"),
			}
			self.img_srf = float_l(self,size_hint = (1,.3))
			self.add_surf(self.img_srf)
			self.aff_side = stack(self,size_hint = (1,.7),
				padding = dp(10),bg_color = self.sc.aff_col1)
			self.set_img_part()
			self.add_surf(self.aff_side)

# Gestion des actions des bouttons
	def set_info_part(self,wid,val):
		if wid.info.lower() == "prix":
			wid.text = self.regul_input(wid.text)
		self.info[wid.info] = wid.text

	def set_image(self,wid):
		self.sc.excecute(self.sc.sys_handler.pick_f,
			self.set_imag_info)

	def set_imag_info(self,path):
		if path:
			self.info['img'] = path
			Clock.schedule_once(self.set_img_part,.1)

	def th_save_menu(self,wid):
		dic = {
			"désignation":self.info['Désignation'],
			"img":self.info['img'],
			"catégorie":self.curent_cat,
			"prix":float(self.info['Prix']),
			"temps de cuisson":self.info['Durée de cuisson'],
			"prestataire":self.sc.get_this_user().get('N°'),
		}
		if self.check(dic):
			self.menu_dic.update(dic)
			self.mother.close_modal()
			self.sc.add_refused_error("Menu ajouter")
			self.sc.excecute(self._th_save_menu,self.menu_dic)
			
		else:
			self.sc.add_refused_error('Toutes les informations sont obligatoires',
				text_color = self.sc.red)

	def _th_save_menu(self,dic):
		cate_dic = self.sc.DB.get_categorie_by_name(self.curent_cat)
		img_p = self.sc.DB.Save_image(self.info.get('img'))
		dic['catégorie'] = cate_dic.get('N°')
		dic['img'] = img_p
		self.sc.DB.update_menu(dic)
		
		Clock.schedule_once(self.mother.add_all,2)

	def trie_categorie(self,wid,val):
		self.cate_info = val
		liste = [i for i in self.cat_list if val.lower() in i.lower()]

		self.liste_derou.list_info = self.liste_derou.normal_list(liste)
		self.liste_derou.add_all()

	def set_categorie(self,info):
		self.curent_cat = info
		self.inp_set.text = info


			




