#Coding:utf-8
"""
	Gestion de l'interface de compte des utilisateurs
"""

from lib.davbuild import *

class compte(box):
	def initialisation(self):
		self.srf_icon_dic = {
		   "client": {
				"icon": "account",
				"color": (0.13, 0.59, 0.95, 1)   # Bleu - utilisateur / confiance
			},
			"prestataire": {
				"icon": "account-tie",
				"color": (0.18, 0.80, 0.44, 1)   # Vert - pro / service
			},
			"admin": {
				"icon": "shield-account",
				"color": (0.96, 0.26, 0.21, 1)   # Rouge - contrôle / autorité
			}
		}
		self.th_name = self.sc.Get_local("USER_IDENT")
		self.all_set = False
		
		if self.th_name:
			self.sc.define_user(self.th_name)
			self.compt_dic = dict(self.sc.DB.get_users_by_num(
				self.th_name))
			self.size_pos()

		else:
			...

	def Set_con_srf(self):
		self.clear_widgets()
		srf = Connexion_srf(self)
		srf.add_all()
		self.add_surf(srf)

	def size_pos(self):
		if not self.compt_dic:
			self.th_name = str()
			self.all_set = False
			self.sc.Save_local("USER_IDENT",str())
			self.add_all()
			return
		self.role = "admin" #self.compt_dic.get("role").lower()
		self.img_src = self.compt_dic.get("img",'media/logo.png')

		self.clear_widgets()
		self.img_srf = float_l(self,size_hint = (1,.35),
			)
		self.info_part = stack(self,size_hint = (1,.65),
			padding = [dp(10),0,dp(10),dp(10)],
			spacing = dp(10))
		self.all_set = True
		self.set_img_part()

		self.add_surf(self.img_srf)
		self.add_surf(self.info_part)

	def set_img_part(self,*args):
		self.img_srf.clear_widgets()
		self.this_img_srf = self.img_srf.add_image(self.img_src,
			radius = dp(50))
		self.img_srf.add_button('',on_press = self.show_image)
		srf_s = (.2,.15)
		srf_p = (.76,.04)
		if self.role == 'admin':
			srf_s = (.3,.15)
			srf_p = (.68,.04)
		self.th_icon_srf = box(self,size_hint = srf_s,
			pos_hint = srf_p,orientation = 'horizontal',
			spacing = dp(10))
		self.img_srf.add_surf(self.th_icon_srf)
		self.th_icon_srf.add_icon_but(icon = "camera",
			on_press = self.set_new_imag,font_size = "24sp")
		self.th_icon_srf.add_icon_but(icon = "pencil",
			on_press = self.modif_infos,font_size = "24sp")
		if self.role == "admin":
			self.th_icon_srf.add_icon_but(icon = "cog",
				on_press = self.setting,font_size = "24sp",
				text_color = (0.13, 0.59, 0.95, 1))

	def Foreign_surf(self,*args):
		self.th_name = self.sc.Get_local("USER_IDENT")
		if self.th_name:
			self.compt_dic = dict(self.sc.DB.get_users_by_num(
				self.th_name))
			if not self.all_set:
				self.size_pos()
			self.add_infos()
			
		else:
			self.Set_con_srf()

	def add_infos(self):
		h = .08
		self.info_part.clear_widgets()
		nom = self.compt_dic.get('nom','david')
		prenom = self.compt_dic.get('prénom','david')
		th_nom = f"{nom.upper()} {prenom}"

		self.info_part.add_text(th_nom,size_hint = (1,h),
			bold = True,font_size = '14sp',halign = "center",
			valign = 'top')
		th_d = {
			"NPI":self.compt_dic.get('NPI',""),
			"téléphone":self.compt_dic.get('téléphone',""),
		}
		for key,info in th_d.items():
			b = Get_border_surf(self.info_part,box(self,
				size_hint = (.5,h*1.6),bg_color = self.sc.aff_col3,
				radius = dp(10),padding = dp(5)),self.sc.aff_col3)
			b.add_text(key,size_hint = (1,.4),
				text_color = self.sc.text_col3)
			b.add_text(self.format_val_(info),size_hint = (.9,.6),
				radius = dp(10),#bg_color = self.sc.aff_col3,
				bold = True,valign = "top",
				text_color = self.sc.text_col1,pos_hint = (.07,0),
				padding_left = dp(5))

		if self.role == "client":
			role_list = list()
		elif self.role == "prestataire":
			role_list = ["client",'prestataire']
		elif self.role == "admin":
			role_list = ["client","prestataire","admin"]
		else:
			role_list = list()
		if role_list:
			self.info_part.add_text('Vos interfaces utilisateurs',
				size_hint = (1,h),halign = "center",
				bold = True)
			for txt in role_list:
				bg_col = None

				ic_dic = self.srf_icon_dic.get(txt)
				txt_col = ic_dic.get('color')

				bold = False
				if txt == self.sc.curent_interface:
					bg_col = self.sc.aff_col3
					bold = True

				b = box(self,size_hint = (.33,h),
					orientation = "horizontal",padding = dp(3),
					radius = dp(10),bg_color = bg_col,)
				b.add_icon_but(icon = ic_dic.get('icon'),
					text_color = txt_col,size_hint = (None,1),
					size = (dp(30),1),font_size = "24sp",
					info = txt,
					on_press = self.sc.th_root.change_interface)
				b.add_button(txt,
					halign = 'left',bold = bold, 
					font_size = "9sp",
					text_color = txt_col,
					on_press = self.sc.th_root.change_interface)
				self.info_part.add_surf(b)

		self.histo_surf = box(self,size_hint = (1,.5),
			bg_color = self.sc.aff_col3,
			radius = dp(20),padding = [dp(10),0,dp(10),dp(10)])

		self.this_cmd_dic = self.sc.get_my_client_cmd()
		if self.this_cmd_dic:
			self.info_part.add_surf(self.histo_surf)
			self.add_histo_surf()

	def add_histo_surf(self):
		self.histo_surf.clear_widgets()
		srf = box(self,size_hint = (1,.2),
			orientation = 'horizontal',
			)
		srf.add_text('Historique de mes commandes',
			size_hint = (.8,1),bold = True)
		if len(self.this_cmd_dic) > 2:
			srf.add_button('plus',text_color = self.sc.green,
				size_hint = (.2,1),	font_size = "9sp",
				self.show_all_cmd)
		self.histo_surf.add_surf(srf)
		sc = scroll(self,size_hint = (1,.8))
		self.histo_surf.add_surf(sc)
		self.cmd_it = box(self,size_hint = (None,1))
		sc.add_surf(self.cmd_it)
		self.add_my_histo()

	def add_my_histo(self):
		self.cmd_it.clear_widgets()
		lis = list(self.historique_list.values())
		if len(lis) > 2:
			lis = lis[-2:]
		for dic in lis:
			b = float_l(self,size_hint = (.5,1))
			b_ = box(self,padding = dp(10))
			img = self.sc.DB.get_prestataires(dic.get('prestataire')).get('img')
			b_.add_image(img,size_hint = (1,.8))
			b_.add_text(self.format_val(dic.get('montant')),
				size_hint = (1,.2),halign = 'center',
				bold = True,font_size ='13sp')
			b.add_surf(b_)
			b.add_button('',bg_color = None,
				on_press = self.show_cmd,
				info = dic.get('N°'))

			

# Gestion des actions des bouttons
	def show_all_cmd(self,wid):
		...

	def show_cmd(self,wid):
		...

	def show_image(self,wid):
		srf = box(self,bg_color = self.sc.aff_col1)
		srf.add_image(self.img_src)
		self.add_modal_surf(srf,size_hint = (1,.9),
			pos_hint = {"x":0,"y":.1},
			overlay_color = (1,1,1,0),
			radius = dp(1),titre = 'Photo de profil')

	def modif_infos(self,wid):
		srf = Connexion_srf(self)
		srf.modification_part()
		self.add_modal_surf(srf,radius = dp(0),
			titre = 'Modification de compte')

	def setting(self,wid):
		srf = setting_srf(self)
		srf.add_all()
		self.add_modal_surf(srf,radius = dp(0),
			titre = 'Paramètrage générale')


	def set_new_imag(self,wid):
		self.sc.excecute(self.sc.sys_handler.pick_f,
			self.set_imag_info)

	def set_imag_info(self,path):
		if path:
			self.img_src = self.sc.DB.Save_image(path)
			self.compt_dic['img'] = self.img_src
			self.sc.DB.update_user(self.compt_dic)

		Clock.schedule_once(self.set_img_part,.01)


class setting_srf(stack):
	def initialisation(self,*args):
		self.cate_info = str()
		self.cat_list = self.sc.DB.get_categories_list()
		if self.cat_list:
			self.curent_cat = self.cat_list[0]
		else:
			self.curent_cat = str()
		
		self.size_pos()

	def size_pos(self,*args):
		h = .07
		
		self.clear_widgets()
		self.add_text("Catégorie",size_hint = (1,h*.7),
			padding_left = dp(10),valign = 'bottom',
			bg_color = self.sc.aff_col1,
			text_color = self.sc.text_col3)
		self.inp_set = self.add_input("Catégorie",size_hint = (.8,h*.9),
			padding = [dp(10),dp(15),dp(10),0],
			bg_color = self.sc.aff_col1,
			default_text = self.cate_info,placeholder = "Catégorie",
			on_text = self.trie_categorie)
		self.add_button('Ajouter',size_hint = (.2,h),
			bg_color = self.sc.aff_col3,on_press = self.add_cate)
		self.add_text('',bg_color = self.sc.sep,
			size_hint = (1,None),height = dp(1))
		self.liste_derou = liste_deroulante(self,self.curent_cat,
			self.cat_list,mother_fonc = self.set_categorie,
			size_hint = (1,.7))
		self.add_surf(self.liste_derou)



# Gestion des actions
	def add_cate(self,wid):
		if self.cate_info not in self.sc.DB.get_categories_list():
			dic = {
				"nom":self.cate_info
			}
			self.sc.DB.save_categorie(dic)
			Clock.schedule_once(self.initialisation,3)
		else:
			self.sc.add_refused_error("Cette catégorie d'article existe déjà",
				text_color = self.sc.red)

		

	def trie_categorie(self,wid,val):
		self.cate_info = val
		liste = [i for i in self.cat_list if val.lower() in i.lower()]

		self.liste_derou.list_info = self.liste_derou.normal_list(liste)
		self.liste_derou.add_all()

	def set_categorie(self,info):
		self.curent_cat = info
		self.cate_info = info
		self.inp_set.text = info


		

class Connexion_srf(stack):
	def initialisation(self):
		self.th_h = .13
		self.curent_code = "225"
		self.code_list = ["225","228",'229']

		self.tel_num = str()
		self.inf_dic = {
			"Nom":str(),
			"Prénom":str(),
			"N° de téléphone":str()
		}
		self.size_pos()

	def size_pos(self):
		self.add_text("",size_hint = (1,.1))
		self.add_padd((.02,.1))
		self.aff_srf = stack(self,size_hint = (.96,.4),
			radius = dp(20),padding = dp(2),
			bg_color = self.sc.aff_col3)
		self.add_surf(self.aff_srf)

	def Foreign_surf(self):
		self.connexion_part()

	def connexion_part(self,*args):
		h = .2
		self.aff_srf.size_hint = (.96,.35)
		self.aff_srf.clear_widgets()
		self.aff_srf.add_button("Connexion",size_hint = (.5,h),
			radius = [dp(20),dp(20),0,0],halign = 'center',
			bg_color = self.sc.aff_col3,
			on_press = self.connexion_part)
		self.aff_srf.add_button("Inscription",size_hint = (.5,h),
			halign = 'center',
			radius = [dp(0),dp(20),0,0],
			bg_color = self.sc.aff_col1,
			on_press = self.inscription_part)

		self.aff_srf.add_text("N° de téléphone",
			size_hint = (1,h*.7),text_color = self.sc.text_col3,
			padding = [dp(13),dp(0),dp(10),dp(0)])
		self.aff_srf.add_surf(liste_set(self,self.curent_code,
			self.code_list,mother_fonc = self.set_curent_code,
			add_null_text = False,size_hint = (.2,h),
			padding = [dp(10),dp(0),dp(10),dp(0)]
			))
		self.aff_srf.add_input('tel',size_hint = (.8,h),
			on_text = self.set_num,bg_color = self.sc.aff_col3,
			focus = True,padding = [dp(0),dp(15),dp(10),0], 
			default_text = self.tel_num,placeholder = 'XXX XXX XXX XX')
		self.aff_srf.add_padd((.05,.001))
		self.aff_srf.add_text('',size_hint = (.9,None),
			height = dp(1),bg_color = self.sc.sep)
		self.aff_srf.add_padd((.05,.001))
		self.aff_srf.add_text("",size_hint = (1,h*.3))
		self.aff_srf.add_padd((.25,h))
		self.aff_srf.add_button("Continuer",
			bg_color = self.sc.aff_col1,
			text_color = self.sc.text_col1,
			on_press = self.set_confirm,
			size_hint = (.5,h))

	def modification_part(self,*args):
		h = .13
		self.this_part = ["nom","prénom","téléphone","NPI"]
		self.th_inf_dic = self.sc.get_this_user()
		self.aff_srf.size_hint = (.96,.6)
		self.aff_srf.clear_widgets()
		
		for txt in self.this_part:
			val = self.th_inf_dic.get(txt,str())
			if txt == "téléphone":
				code,val = val.split(' ')
				self.th_inf_dic['téléphone'] = val
				self.curent_code = code

				self.aff_srf.add_text(txt,
					size_hint = (1,h*.7),
					text_color = self.sc.text_col3,
					padding = [dp(13),dp(0),dp(10),dp(0)])
				self.aff_srf.add_surf(liste_set(self,
					self.curent_code,self.code_list,
					mother_fonc = self.set_curent_code,
					size_hint = (.25,h*.8),add_null_text = False,
					padding = [dp(10),dp(0),dp(10),dp(0)]
					))
				self.aff_srf.add_input(txt,
					size_hint = (.75,h*.8),
					on_text = self.set_this_infos,
					bg_color = self.sc.aff_col3,
					padding = [dp(0),dp(13),dp(10),0], 
					default_text = val,
					placeholder = 'XXX XXX XXX XX')

			else:
				self.aff_srf.add_text(txt,
					text_color = self.sc.text_col3,
					valign = 'bottom',size_hint = (1,h*.7),
					padding = [dp(13),dp(0),dp(10),dp(0)])
				
				self.aff_srf.add_input(txt,size_hint = (1,h*.8),
					on_text = self.set_this_infos,bg_color = self.sc.aff_col3,
					focus = True,padding = [dp(14),dp(13),dp(10),0],
					placeholder = txt,default_text = val)
			self.aff_srf.add_padd((.05,.001))
			self.aff_srf.add_text('',size_hint = (.9,None),
				height = dp(1),bg_color = self.sc.sep)
			self.aff_srf.add_padd((.05,.001))

		self.aff_srf.add_padd((1,h*.4))

		self.aff_srf.add_padd((.25,h))
		self.aff_srf.add_button("Valider",
			bg_color = self.sc.aff_col1,
			text_color = self.sc.text_col1,
			on_press = self.update_compt,
			size_hint = (.5,h))

	def inscription_part(self,*args):
		h = .13
		self.aff_srf.size_hint = (.96,.5)
		self.aff_srf.clear_widgets()
		self.aff_srf.add_button("Connexion",size_hint = (.5,h),
			halign = 'center',
			radius =  [dp(20),dp(0),0,0],
			bg_color = self.sc.aff_col1,
			on_press = self.connexion_part)
		self.aff_srf.add_button("Inscription",size_hint = (.5,h),
			halign = 'center',
			radius = [dp(20),dp(20),0,0],
			bg_color = self.sc.aff_col3,
			on_press = self.inscription_part)

		for txt,val in self.inf_dic.items():
			if txt == "N° de téléphone":
				self.aff_srf.add_text(txt,
					size_hint = (1,h*.7),
					text_color = self.sc.text_col3,
					padding = [dp(13),dp(0),dp(10),dp(0)])
				self.aff_srf.add_surf(liste_set(self,
					self.curent_code,self.code_list,
					mother_fonc = self.set_curent_code,
					size_hint = (.2,h),add_null_text = False,
					padding = [dp(10),dp(0),dp(10),dp(0)]
					))
				self.aff_srf.add_input(txt,
					size_hint = (.8,h),
					on_text = self.set_infos,
					bg_color = self.sc.aff_col3,
					padding = [dp(0),dp(13),dp(10),0], 
					default_text = val,
					placeholder = 'XXX XXX XXX XX')

			else:
				self.aff_srf.add_text(txt,
					text_color = self.sc.text_col3,
					valign = 'bottom',size_hint = (1,h*.7),
					padding = [dp(13),dp(0),dp(10),dp(0)])
				
				self.aff_srf.add_input(txt,size_hint = (1,h*.8),
					on_text = self.set_infos,bg_color = self.sc.aff_col3,
					focus = True,padding = [dp(14),dp(10),dp(10),0],
					placeholder = txt,default_text = val)
			self.aff_srf.add_padd((.05,.001))
			self.aff_srf.add_text('',size_hint = (.9,None),
				height = dp(1),bg_color = self.sc.sep)
			self.aff_srf.add_padd((.05,.001))

		self.aff_srf.add_padd((1,h*.4))

		self.aff_srf.add_padd((.25,h))
		self.aff_srf.add_button("Continuer",
			bg_color = self.sc.aff_col1,
			text_color = self.sc.text_col1,
			on_press = self.set_inscription,
			size_hint = (.5,h))

# Gestion des actions
	def set_this_infos(self,wid,val):
		self.th_inf_dic[wid.info] = val

	def update_compt(self,wid):
		num = self.curent_code+' '+self.th_inf_dic.get('téléphone')
		dic = dict(self.th_inf_dic)
		dic['téléphone'] = num
		#print(dic)
		self.sc.DB.update_user(dic)
		self.sc.Save_local('USER_IDENT',num)
		self.mother.close_modal()

		self.sc.excecute(self.aff_compte_surf)


	def set_curent_code(self,info):
		self.curent_code = info

	def set_num(self,wid,num):
		wid.text = self.regul_input(num)
		self.tel_num = wid.text

	def set_confirm(self,wid):
		num = self.curent_code + ' ' + self.tel_num
		num = num.strip()
		user = self.sc.DB.get_users_by_num(num)
		if user:
			self.sc.define_user(num)
			self.mother.Foreign_surf()
			self.sc.Save_local("USER_IDENT",num)
		else:
			self.sc.add_refused_error("Votre numéro de téléphone n'est pas reconnu!!\n Il faut vous inscrire sur la plateforme!")
			self.inscription_part()

	def set_infos(self,wid,info):
		self.inf_dic[wid.info] = info

	def set_inscription(self,wid):
		if self.check(self.inf_dic):
			num = self.curent_code + ' ' + self.inf_dic.get('N° de téléphone')
			num = num.strip()
			dic = {
				"role":'client',
				"nom":self.inf_dic.get('Nom'),
				"prénom":self.inf_dic.get('Prénom'),
				"téléphone":num
			}
			user = self.sc.DB.get_users_by_num(num)
			if user:
				self.aff_compte_surf()
			#print(dic)
			else:
				self.sc.DB.save_user(dic)
				self.sc.Save_local('USER_IDENT',num)

				self.sc.excecute(self.aff_compte_surf)

		else:
			self.sc.add_refused_error("Toutes les informations sont obligatoires!")

	def aff_compte_surf(self):
		user = dict()
		num = self.sc.Get_local("USER_IDENT")
		while not user:
			time.sleep(1)
			user = self.sc.DB.get_users_by_num(num)

		self.sc.define_user(num)

		Clock.schedule_once(self.mother.Foreign_surf,.1)




