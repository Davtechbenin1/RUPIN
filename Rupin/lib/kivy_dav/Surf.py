#Coding:utf-8
"""
	Ce module permet la définition d'une surface
	en partant du kv lang
"""
try:
	from .metrics import dp,sp
except:
	from metrics import dp,sp
from time import time
from kivy.graphics import*
from kivy.graphics.vertex_instructions import*
from operator import itemgetter
from datetime import datetime

class surf:
	def __init__(self,bg_color = None,
		shadow = 0,shadow_color = (0,0,0),
		shadow_inset = False,
		Id = str(),
		shadow_offset = (0,0),
		alpha = .99,padding_left = 0,
		padding_top = 0,spacing = 0,
		padding_bottom = 0,size_hint = (1,1),
		pos_hint = (0,0),
		padding_right = 0,top_left_radius = 0,
		top_right_radius = 0,
		bottom_left_radius = 0,
		bottom_right_radius = 0,
		padding = None,
		radius = None,height = None,
		width = None,border_top = 0,
		border_left = 0,border_bottom = 0,
		border_right = 0,border = None,
		border_color = (0,0,0),
		img_border = False):
	#
		self.img_border = img_border
		self.layout = False
		self.border_color = border_color
		self.bg_color = bg_color
		self.ident = Id
		self.shadow = shadow
		self.shadow_color = shadow_color
		self.shadow_inset = shadow_inset
		self.alpha = alpha
		self.shadow_offset = shadow_offset
		self.padding_left = padding_left
		self.padding_top = padding_top
		self.spacing = spacing
		self.padding_bottom = padding_bottom
		self.size_hint = size_hint
		self.add_pos_hint(*pos_hint)
		self.padding_right = padding_right
		self.top_left_radius = top_left_radius
		self.top_right_radius = top_right_radius
		self.bottom_left_radius = bottom_left_radius
		self.bottom_right_radius = bottom_right_radius
		if not radius:
			radius = [top_left_radius,
			top_right_radius,bottom_right_radius,
			bottom_left_radius]
		elif type(radius) in (int,float):
			radius = [radius]*4
		self.radius = radius

		if not padding:
			padding = [padding_left,padding_top,
			padding_right,padding_bottom]
		elif type(padding) in (int,float):
			padding = [padding]*4
		self.padding = padding

		if width:
			self.width = self.Get_with(width)
		if height:
			self.height = self.Get_height(height)

		if not border:
			border = [border_left,border_top,
			border_right,border_bottom]
		self.border = border
		self.border_set = False
		if sum(self.border)>0:
			self.border_set = True

		self.add_box_shadow()
		self.add_bg_color()
		self.bind(pos = self.draw_bg,
			size = self.draw_bg)

	def Get_with(self,width):
		return round(width,0)

	def Get_height(self,height):
		return round(height,0)
		
	def add_size_hint(self,w,h):
		self.size_hint = (w,h)

	def add_size(self,w,h):
		self.add_width(w)
		self.add_height(h)
		self.add_size_hint(None,None)

	def add_width(self,w):
		self.width = self.Get_with(w)

	def add_height(self,h):
		self.height = self.Get_height(h)

	def add_pos_hint(self,x,y):
		dic = {"x":x,'y':y}
		self.pos_hint = dic

	def add_pos(self,x,y):
		self.pos = x,y

	def add_bg_color(self):
		self.bg_color_obj = None
		if self.bg_color:
			if len(self.bg_color) == 4:
				col = self.bg_color
			else:
				r,g,b = self.bg_color
				col = r,g,b,self.alpha
			with self.canvas.before:
				Color(*col)
				self.bg_color_obj = RoundedRectangle(pos = self.pos,
					size = self.size,radius =self.radius)
		
	def	add_box_shadow(self):
		self.shadow_obj = None
		if self.shadow:
			r,g,b = self.shadow_color
			col = r,g,b,self.alpha
			with self.canvas.before:
				Color(*col)
				self.shadow_obj = BoxShadow(
					inset = self.shadow_inset,
					size = self.size,pos = self.pos,
					border_radius= self.radius,
					blur_radius = self.shadow,
					offset = self.shadow_offset)

	def draw_bg(self,*value):
		if self.shadow_obj:
			self.shadow_obj.pos = self.pos
			self.shadow_obj.size = self.size
		if self.bg_color_obj:
			self.bg_color_obj.pos = self.pos
			self.bg_color_obj.size = self.size

		self.Another_event(value)

	def Another_event(self,value):
		"""
			Cette méthode définie les autres
			partie de la surface à mettre a jour
			en fonction de la taille et de la
			position de la surface
		"""
		pass

	def format_val_(self,val):
		val = str(val)
		if val:
			pref = str()
			if val[0] == '-':
				pref = "-"
				val = val[1:]
			V = val.split('.')
			if len(V)==2:
				val = V[0]
				if int(V[-1]):
					V = "."+V[-1]
				else:
					V = str()
			else:
				val = V[0]
				V = str()
			lenf = len(val)
			ind = 3
			fr = []
			part = ['']*3
			for i in range(lenf-1,-1,-1):
				ind -= 1
				part.insert(ind,val[i])
				if ind == 0:
					fr.append(''.join(part))
					part = ['']*3
					ind = 3
			P = get_prt(part)
			if P:
				fr.append(P)
			fr.reverse()
			return pref+" ".join(fr)+V
		return val

	
	def format_val(self,val,virgule:int = 1):
		try:
			float(val)
			val = round(val,virgule)
		except:
			if not val:
				val = str()
			return val
		else:
			return self.format_val_(val)

	def Run(self):
		return self

	def Execution(self):
		return self.Run()

	def Sort_infos(self,liste,part,reverse = False):
		key_s = "SORTING_INDFFF"
		th_l = list()
		for dic in liste:
			info = dic.get(part)
			try:
				inf = datetime.strptime(info,self.date_format)
			except Exception as e:
				try:
					inf = float(info)
				except:
					if info:
						inf = info.lower()
					else:
						inf = "None"
			dic["SORTING_INDFFF"] = inf
			th_l.append(dic)
		try:
			th_l.sort(key = itemgetter(key_s),reverse = reverse)
		except Exception as e:
			...
			#self.notify('error')
		for k in th_l:
			if key_s in k:
				k.pop(key_s)
		return th_l

def get_prt(part):
	P = str()
	for i in part:
		if i:
			P += i
	return P