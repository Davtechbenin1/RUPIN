#Coding:utf-8
"""
	Surface de définition d'une surface de dessins
"""
try:
	from .davbuild import *
except ImportError:
	from davbuild import *

from kivy.graphics import*
from kivy.graphics.vertex_instructions import*


class draw_surf(layout):
	def __init__(self,mother,info,**kwargs):
		"""
			Les tailles et position doivent être relatif à la
			surface
		"""
		layout.__init__(self,mother,**kwargs)

		self.info_dic = {}
		self.draw_dic = dict()
		self.indice = 1
		self.add_text('',info = info)

	def add_line(self,points,width,color,close = True):
		self.info_dic[self.indice] = ["Line",points]
		with self.canvas.before:
			Color(*color)
			obj = Line(points = points,width = width,
				close = close)
			self.draw_dic[self.indice] = obj
		self.indice += 1

	def add_rect(self,size,pos,radius,color):
		if type(radius) != list:
			radius = [radius] * 4
		self.info_dic[self.indice] = ["Rect",[size,pos,radius,color]]
		with self.canvas.before:
			Color(*color)
			obj = RoundedRectangle(pos = pos,
				size = size,radius = radius,)
			self.draw_dic[self.indice] = obj
		self.indice += 1

	def add_triangle(self,points,color):
		"""
			Les points doivent être relative
		"""
		self.info_dic[self.indice] = ["Triangle",points]
		with self.canvas.before:
			Color(*color)
			obj = Triangle(points = points)
			self.draw_dic[self.indice] = obj
		self.indice += 1

	def Update(self):
		for ind in self.info_dic:
			typ,infos = self.info_dic[ind]
			obj = self.draw_dic[ind]
			if typ in ('Line',"Triangle"):
				Point = list()
				for p in infos:
					if type(p) in (list,tuple):
						x,y = p
						x = x*self.size[0]+self.pos[0]
						y = y*self.size[1]+self.pos[1]
						Point.append(x)
						Point.append(y)
				obj.points = Point
			elif typ == 'Rect':
				size,pos,radius,color = infos
				w,h = size
				w = w*self.size[0]
				h = h*self.size[1]
				obj.size = (w,h)
				x,y = pos
				x = x*self.size[0]+self.pos[0]
				y = y*self.size[1]+self.pos[1]
				obj.pos = (x,y)

	def Another_event(self,value):
		self.Update()

