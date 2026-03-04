#Coding:utf-8
"""
	Permet de créer un tableau de façon dynamique depuis l'interface du
	logiciel
"""
from lib.davbuild import *
class dynamique_tab(box):
	def __init__(self,mother,**kwargs):
		kwargs['bg_color'] = mother.sc.text_col1
		kwargs['padding'] = dp(1)
		kwargs['spacing'] = dp(1)
		box.__init__(self,mother,**kwargs)

	def initialisation(self):
		self.entete_surf = box(self,size_hint = (1,None),
			height = dp(35),orientation = 'horizontal',
			bg_color = self.sc.aff_col1)
		self.infos_surf = scroll(self,bg_color = self.sc.aff_col1)

		self.def_surf = box(self,size_hint = (1,None),
			height = dp(35),orientation = 'horizontal',
			bg_color = self.sc.aff_col1)

		self.add_surf(self.entete_surf)
		self.add_surf(self.infos_surf)
		self.add_surf(self.def_surf)

		self.infos_list = list()#list de dict
		self.curent_dict = dict()

	def Creat_Table(self,wid_l,entete,mother_fonc = None):
		self.wid_l = wid_l
		self.entete = entete
		self.mother_fonc = mother_fonc
		self.add_all()

	def Foreign_surf(self):
		self.add_entete()
		self.add_infos_surf()
		self.add_set_infos()

	def add_entete(self):
		self.entete_surf.clear_widgets()
		for w,ent in zip(self.wid_l,self.entete):
			self.entete_surf.add_text('',size_hint = (None,1),
				bg_color = self.sc.text_col1,width = dp(1))
			self.entete_surf.add_text(ent,size_hint = (w,1),
				text_color = self.sc.text_col1,padding_left = dp(5))
		self.entete_surf.add_text('',size_hint = (None,1),
				bg_color = self.sc.text_col1,width = dp(1))
	
	def add_infos_surf(self):
		self.infos_surf.clear_widgets()
		h = dp(30)
		H = len(self.infos_list) * (h+dp(10))
		H += dp(10)
		stw = stack(self,size_hint = (1,None),height = H,
			bg_color = self.sc.text_col1,
			spacing = dp(1))
		for dic in self.infos_list:
			b =  box(self,size_hint = (1,None),
				height = h,orientation = "horizontal",
				bg_color = self.sc.aff_col1)
			for w,ent in zip(self.wid_l,self.entete):
				b.add_text('',size_hint = (None,1),
					bg_color = self.sc.text_col1,width = dp(1))
				b.add_button(dic.get(ent),size_hint = (w,1),
					text_color = self.sc.text_col1,bg_color = None,
					halign = 'left',info = dic.get(self.entete[0]),
					on_press = self.modif_part,padding_left = dp(5))
			b.add_text('',size_hint = (None,1),
				bg_color = self.sc.text_col1,width = dp(1))
			stw.add_surf(b)
		self.infos_surf.add_surf(stw)

	def add_set_infos(self):
		self.def_surf.clear_widgets()
		for w,ent in zip(self.wid_l,self.entete):
			dic = self.curent_dict
			if not dic:
				dic = dict()
				self.curent_dict = dict()
			self.def_surf.add_text('',size_hint = (None,1),
				bg_color = self.sc.text_col1,width = dp(1))
			self.def_surf.add_input(ent,size_hint = (w,1),
				text_color = self.sc.text_col1,bg_color = self.sc.aff_col3,
				default_text = dic.get(ent,str()),
				placeholder = ent,
				on_text = self.set_curent_info)
		b = box(self,size_hint = (None,None),height = dp(35),width = dp(35))
		b.add_icon_but(icon = 'plus',text_color = self.sc.green,
			size_hint = (1,1),font_size = '34sp',on_press = self.valide_curent_d,)
		self.def_surf.add_surf(b)
		#add_button("",size_hint = (None,None),
		#	height = dp(35),width = dp(35),on_press = self.valide_curent_d,
		#	bg_color = self.sc.green,text_color = self.sc.text_col3,
		#	font_size = "25sp",radius = dp(20))

	def Get_this_info(self,info):
		for d in self.infos_list:
			if f"{d.get(self.entete[0])}" == f"{info}":
				self.infos_list.remove(d)
				return d

	def check(self):
		for ent in self.entete:
			if not self.curent_dict.get(ent):
				return False
		return True

# Gestion des actions des buttons
	def modif_part(self,wid):
		info = wid.info
		self.curent_dict = self.Get_this_info(info)
		self.add_infos_surf()
		self.add_set_infos()

	def set_curent_info(self,wid,val):
		self.curent_dict[wid.info] = val

	def valide_curent_d(self,wid):
		if self.check():
			dic = self.curent_dict
			old_d = self.Get_this_info(dic.get(self.entete[0]))
			self.infos_list.append(self.curent_dict)
			ret = True
			if self.mother_fonc:
				ret = self.mother_fonc(self.infos_list)
			if ret in (None,True):
				self.curent_dict = dict()
				self.add_infos_surf()
				self.add_set_infos()
			else:
				self.infos_list.remove(self.curent_dict)




