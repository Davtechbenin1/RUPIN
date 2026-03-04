#Coding:utf-8
"""
	Module de définition de tableau avec le float_l
"""
try:
	from .davbuild import *
except ImportError:
	from davbuild import *

from color import *

class table(float_l):
	def __init__(self,mother,entete_liste,entete_col_liste,
		contenue_liste,contenue_color_liste,part_size,
		part_ws,dec_bg_col,ent_halign = 'center',
		cont_halign = 'center',**kwargs):
		float_l.__init__(self,mother,**kwargs)

		self.entete_liste = entete_liste
		self.entete_col_liste = entete_col_liste
		self.contenue_liste = contenue_liste
		self.contenue_color_liste = contenue_color_liste
		self.part_size = part_size
		self.part_ws = part_ws
		self.dec_bg_col = dec_bg_col

		if type(ent_halign)==str:
			ent_halign = [ent_halign]*len(entete_liste)

		if type(cont_halign)==str:
			cont_halign = [cont_halign]*len(entete_liste)
		
		self.ent_halign = ent_halign
		self.cont_halign = cont_halign

		self.add_all()

	def Foreign_surf(self):
		#pass
		self.trace_cadre()
		self.add_entete()
		self.add_cont()

	def add_entete(self):
		y = 1-self.part_size[1]
		B = box(self,size_hint = self.part_size,pos_hint = (0,y),
			orientation = 'horizontal')
		for entete,w,col,hal in zip(self.entete_liste,self.part_ws
			,self.entete_col_liste,self.ent_halign):
			B.add_text(entete,text_color = col,size_hint = (w,1),
				halign = hal)
		self.add_surf(B)
		self.add_text("",size_hint = (1,.001),pos_hint = (0,y),
			bg_color = self.dec_bg_col)

	def add_cont(self):
		y = 1-(self.part_size[1]*2)
		for liste in self.contenue_liste:
			B = box(self,size_hint = self.part_size,pos_hint = (0,y),
			orientation = 'horizontal')
			for cont,w,col,hal in zip(liste,self.part_ws
				,self.contenue_color_liste,self.cont_halign):
				B.add_text(cont,text_color = col,size_hint = (w,1),
					halign = hal)
			self.add_surf(B)
			self.add_text("",size_hint = (1,.001),pos_hint = (0,y),
				bg_color = self.dec_bg_col)
			y-=self.part_size[1]

	def trace_cadre(self):
		X = 0
		for w in self.part_ws[:-1]:
			X += w
			self.add_text("",size_hint = (.0009,1),
				bg_color = self.dec_bg_col,
				pos_hint = (X,0))





