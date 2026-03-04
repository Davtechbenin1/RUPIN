#Coding:utf-8
"""
	Gestion des surfaces de gestion des commandes
"""
from lib.davbuild import *

class show_th_cmd(box):
	def initialisation(self):
		self.cmd_dic = dict()

		self.aff_side = stack(self,size_hint = (1,.93),
			bg_color = self.sc.aff_col1,padding = dp(10))
		self.menu_side = box(self,size_hint = (1,.07),
			bg_color = self.sc.aff_col1,
			orientation = "horizontal")

		self.add_surf(self.aff_side)
		self.add_surf(self.menu_side)
		self.size_pos()

	def size_pos(self):
		if self.cmd_dic:
			h = .07
			clt_d = self.sc.DB.get_users(self.cmd_dic.get('client'))
			presta_d = self.sc.DB.get_users(self.cmd_dic.get('prestataire'))
			liv_d = dict() #self.sc.DB.get_users(self.cmd_dic.get('livreur'))

			f = float_l(self,size_hint = (1,.25))
			f.add_image(presta_d.get("img"))
			f.add_text(f"{presta_d.get('nom')} {presta_d.get('prénom')}".strip(),
				size_hint = (1,.2),bg_color = (*self.sc.text_col1,.3),
				halign = 'center',bold = True)
			f.add_button("",on_press = self.show_th_user,
				info = presta_d.get('N°'))
			self.aff_side.add_surf(f)

			self.aff_side.add_text("Date d'émission",size_hint = (1,h),
				text_color = self.sc.text_col3,valign = 'bottom') 
			self.aff_side.add_text(f"{self.cmd_dic.get('date')} à {self.cmd_dic.get('heure')}",
				text_color = self.sc.text_col1,size_hint = (1,h))
			self.aff_side.add_text('',size_hint = (1,None),bg_color = self.sc.sep,
				height = dp(1))

			dic = {
				"montant":self.cmd_dic.get('montant'),
				'status':self.cmd_dic.get('')

			}
			for k,v in dic.items():
				b = box(self,size_hint = (.48,h*1.7))
				b.add_text(k,size_hint = (1,.45),valign = 'bottom',
					text_color = self.sc.text_col3)
				b.add_text(self.format_val(v),size_hint = (1,.55),
					text_color = self.sc.text_col1)
				b.add_text("",size_hint = (1,None),
					bg_color = self.sc.sep,height = dp(1))
				self.aff_side.add_surf(b)

			b = float_l(self,size_hint = (1,h*1.7),
				bg_color = self.sc.aff_col3,radius = dp(10),
				)
			b.add_image(clt_d.get('img'),
				size_hint = (.2,.96),pos_hint = (.05,.02))
			b_ = box(self,size_hint = (.7,96))
			b_.add_text('Client',size_hint = (1,.45),
				text_color = self.sc.text_col3)
			b_.add_text(f"{clt_d.get('nom')} {clt_d.get('prénom')}".strip(),
				text_color = self.sc.text_col1,size_hint = (1,.55))
			b.add_surf(b_)
			b.add_button("",bg_color = None,on_press = self.show_th_user,
				info = clt_d.get('N°'))
			self.aff_side.add_surf(b)

			self.aff_side.add_text("Détails des ménus",
				halign = 'center',size_hint = (1,h))
			wid_l = self.
			tab = Table(self,size_hint = (1,.2),
				)
			tab.Creat_Table()


# Gestion des actions de bouttons
	def show_th_user(self,wid):
		...


