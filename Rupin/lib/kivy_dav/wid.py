#Coding:utf-8
"""
	Ici, il est question de définir un layout
	afin de l'utiliser pour définir n'import quel autre
	objet. Nous allons prendre comme exemple le 
	widget de base pour définir les attributs.

	Cette parti du layout regorgera de simple widget
	issue de kivy.

	Le Layout sera pour la combinaison de ses widget
	pour créer des ensembles de widget avancé.
"""
try:
	from .Surf import surf
	from .text import text
	from .button import but,icon_but
	from .text_input import text_input
	from .image import imag
	from .metrics import dp,sp
except ImportError:
	from Surf import surf
	from text import text
	from button import but,icon_but
	from text_input import text_input
	from image import imag
	from metrics import dp,sp

import calendar,sys
from operator import itemgetter
import datetime

import platform, os
from plyer import notification
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
if platform.system() == 'Windows':
	try:
		from plyer.platforms.win.notification import WindowsNotification
		notification.notify = WindowsNotification().notify
	except Exception as e:
		print(f"Erreur !!! {e}")

	from tkinter import Tk
	from tkinter.filedialog import askopenfilename

class wid(surf):
	def __init__(self,mother,**kwargs):
		surf.__init__(self,**kwargs)
		self.access_liste = "all"
		self.access_dic = "all"
		self.date_format = "%d-%m-%Y"
		self.SC = False
		self.mother = mother
		self.sc = self.SCREEN = mother.SCREEN
		self.day1 = self.sc.get_today()
		self.day2 = self.sc.get_today()
		self.MENU_SURF = False
		self.layout = True
		self.PRIORITY_LAY = None
		self.CLOSE_LAY = None
		self.th_image_srf = None
		self.file_link = "media/logo.png"
		font_dic = {
			"Roboto":'Roboto',
			"Lexend":'static/Lexend.ttf',
			"Segoe":'static/segoe.ttf',
			"Sfpro":"static/Sfpro.otf",
			"Inter":"static/Inter-Bold.ttf"
		}
		try:
			self.defaut_font = font_dic.get(self.sc.DB.Get_font())
		except:
			self.defaut_font = font_dic.get("Roboto")
		self.Error_text = str()
		self.error_text = str()
		self.Succes_text = str()
		self.succes_text = str()
		self.init_list()
		self.initialisation()
#
	def initialisation(self):
		"""
			A réécrire pour définir les valeurs à initialiser
		"""
		pass

	def get_text_width(self, text, font_size, font_name):
		label = CoreLabel(text=text, font_size=sp(font_size), font_name=font_name)
		label.refresh()  # calcule la texture
		return label.texture.size[0]+self.redo(35)

	def redo(self,val):
		ref = 1920
		i = 1
		real = Window.width
		try:
			i = real/ref
			return round(val/i,0)
		except:
			i = 1
			return round(val/i,0)

	def add_priority_lay(self,priority_wid):
		self.PRIORITY_LAY = priority_wid

	def init_list(self):
		self.Input_dic = dict()
		self.clear_widgets()

	def add_surf(self,srf,index = 0):
		try:
			self.Input_dic.update(srf.Input_dic)
			if not self.th_image_srf and srf.th_image_srf:
				self.th_image_srf = srf.th_image_srf
		except AttributeError:
			pass
		self.add_widget(srf,index = index)
		return srf

	def add_new_surf(self,srf):
		return self.add_surf(srf.Run())

	def add_text(self,txt,info = str(),**kwargs):
		txt = str(txt)
		f_n = kwargs.get('font_name',self.defaut_font)
		kwargs["font_name"] = f_n
		taille = kwargs.get('font_size')
		if not taille:
			taille = self.sc.default_font_size
		kwargs['font_size'],ta = self.redo_taille(taille)

		if kwargs.get('width') and txt:
			kwargs['width'] = self.get_text_width(txt,ta,f_n)
		if not kwargs.get('text_color'):
			kwargs["text_color"] = self.sc.text_col1
		T = text(txt,**kwargs)
		
		T.info = info
		return self.add_surf(T.Run())

	def add_icon_but(self,info = str(),on_press = None,
		on_release = None,on_motion = None,**kwargs):
		if not kwargs.get('text_color'):
			kwargs["text_color"] = self.sc.text_col1
		
		obj = icon_but(on_press = on_press,on_release = on_release,
			on_motion = on_motion,**kwargs)
		obj.info = info
		self.sc.actions_wids.append(obj)
		return self.add_surf(obj)

	def add_close_but(self,fonc,size_hint = (None,None),
		size = (dp(35),dp(35)),font_size = "15sp",text_color = (.9,0,.3)):
		self.add_icon_but(icon = "close",size_hint = size_hint,
			size = size,text_color = text_color,font_size = font_size,
			on_press = fonc)

	def redo_taille(self,taille):
		T_deduce = 2
		if type(taille)in (int,float):
			taille = self.Get_from_resolution(taille)
			taille += T_deduce
		else:
			taille = int(taille.split("sp")[0])
			taille = self.Get_from_resolution(taille)
			taille += T_deduce
		return f"{sp(taille)}",sp(taille)

	def Get_from_resolution(self,taille):
		return taille

	def set_alpha_of(self,color,alpha):
		lis = color
		if len(lis) == 4:
			r,g,b,a = lis
			col = r,g,b,alpha
		elif len(lis) == 3:
			r,g,b = lis
			col = r,g,b,alpha
		else:
			if not alpha:
				alpha = 1
			col = 1,1,1,alpha
		return col

	def add_h_ligne(self,color,size = (1,.0001)):
		self.add_text('',size_hint = size,
			bg_color = color)

	def add_button(self,txt,info = str(),**kwargs):
		txt = str(txt)
		f_n = kwargs.get('font_name',self.defaut_font)
		kwargs["font_name"] = f_n
		taille = kwargs.get('font_size')
		if not taille:
			taille = self.sc.default_font_size
		kwargs['font_size'],ta = self.redo_taille(taille)
		if kwargs.get('width') and txt:
			kwargs['width'] = self.get_text_width(txt,ta,f_n)
		if not kwargs.get('text_color'):
			kwargs["text_color"] = self.sc.text_col1
		if not kwargs.get('bg_color'):
			kwargs["bg_color"] = None

		if kwargs['bg_color'] == self.sc.green:
			if kwargs['text_color'] == self.sc.text_col1:
				kwargs['text_color'] = self.sc.white
		
		B = but(txt,**kwargs)
		if not info:
			info = txt
		B.info = info
		self.sc.actions_wids.append(B)
		return self.add_surf(B.Run())

	def add_input(self,info = str(),on_text = None,
		focus = False,**kwargs):
	#
		f_n = kwargs.get('font_name',self.defaut_font)
		kwargs["font_name"] = f_n
		d_t = kwargs.get('default_text',str())
		kwargs['default_text'] = d_t
		self.Input_dic[info] = kwargs.get("default_text",str())
		ident = kwargs.get("Id",info)
		kwargs["Id"] = ident
		taille = kwargs.get('font_size')
		if not taille:
			taille = self.sc.default_font_size
		kwargs['font_size'],ta = self.redo_taille(taille)
		if not kwargs.get('text_color'):
			kwargs["text_color"] = self.sc.text_col1
		if not kwargs.get('bg_color'):
			kwargs["bg_color"] = self.sc.aff_col3
		T = text_input(**kwargs)
		T.focus = focus
		if on_text:
			T.bind(text = on_text)
		T.info = info
		self.sc.actions_wids.append(T)
		return self.add_surf(T.Run())

	def add_text_input(self,text,text_size,input_size,
		txt_color,inp_info = str(),text_halign = "left",
		text_valign = "middle",
		text_font_size = None,txt_pad = dp(0),readonly = False,
		text_text_color = None,**input_args):
		if not inp_info:
			inp_info = text
		if not text_font_size:
			text_font_size = self.sc.default_font_size
		self.add_text(text,text_color = txt_color,
			halign = text_halign,size_hint = text_size,
			font_size = text_font_size,padding = txt_pad,
			bg_color = text_text_color,valign = text_valign,
			)
		if not readonly:
			return self.add_input(inp_info,size_hint = input_size,
				**input_args)
		else:
			if 'on_text' in input_args:
				input_args.pop("on_text")
			if "default_text" in input_args:
				txt = input_args.pop('default_text')
			else:
				txt = str()
			input_args['padding_left'] = dp(10)
			if "placeholder" in input_args:
				input_args.pop('placeholder')
			return self.add_text(txt,size_hint = input_size,
				**input_args)

	def add_text_multi_input(self,text,text_size,input_size,
		txt_color,inp_dic,text_halign = "left",
		text_font_size = None,sep = "au",sep_w = (.04),
		sep_txt_col = None,
		**input_args):
		if not text_font_size:
			text_font_size = self.sc.default_font_size
		sep_size = sep_w,input_size[1]
		if not sep_txt_col:
			sep_txt_col = txt_color
		self.add_text(text,text_color = txt_color,
			halign = text_halign,size_hint = text_size,
			font_size = text_font_size)
		f = True
		for k,val in inp_dic.items():
			input_args['placeholder'] = k
			input_args['default_text'] = str(val)
			self.add_input(k,size_hint = input_size,
				**input_args)
			if f:
				self.add_text(sep,size_hint = sep_size,
					text_color = sep_txt_col,halign = 'center' )
				f= False

	def on_text(self,widget,value):
		self.Input_dic[widget.ident] =  value

	def add_image(self,source,info = str(),
		bg_color = None,radius = dp(1),**kwargs):
	#
		kwargs['bg_color'] = bg_color
		kwargs["radius"] = radius
		kwargs['image_color'] = self.sc.aff_col1

		img = imag(source,**kwargs)
		img.info = info
		self.th_image_srf = self.add_surf(img.Run())
		return self.th_image_srf

	def affiche_info(self):
		pass

	def date_handler(self,d,m,y):
		pass

	def replace(self,wid1,wid2):
		self.remove_widget(wid1)
		return self.add_surf(wid2)
	
	def Update_wid(self,wid):
		self.replace(wid,wid)

	def Foreign_surf(self):
		pass
	
	def add_all(self,*args):
		#self.sc.loading_srf.show()
		#Clock.schedule_once(self._add_all_,.0001)
		self._add_all_()
		
	def _add_all_(self,*args):
		if self.PRIORITY_LAY:
			self.clear_widgets()
			return self.add_surf(self.PRIORITY_LAY)
		else:
			self._Foreign_surf()
		#self.sc.loading_srf.hide()

	def _Foreign_surf(self,*args):
		self.Foreign_surf()
	
	def check_input(self):
		dic = self.Input_dic
		return self.check_dic(dic)
		
	def check_dic(self,dic):
		for key,val in dic.items():
			if not val:
				return False
		return True

	def Convert_date(self,date):
		day,m,y = date.split('-')
		dic = {
			"1":"Janvier",
			"2":"Février",
			"3":"Mars",
			"4":"Avril",
			"5":"Mai",
			"6":"Juin",
			"7":"Juillet",
			"8":"Août",
			"9":"Septembre",
			"10":"Octobre",
			"11":"Novembre",
			"12":"Décembre",
		}
		m = dic[m]
		return f'{day} {m} {y}'

	def get_ind_jour(self,date,
		ind_l = ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim']):
	#
		d,m,y = date.split('-')
		m = int(m)
		y = int(y)
		d = int(d)
		indice = calendar.weekday(y,m,d)
		day = ind_l[int(str(indice))]
		return day

	def get_days_ind(self):
		return ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim']

# Gestion des surfaces modale
	def add_modal_surf(self,surf,titre = "Alerte système",
		auto_dismiss = True,show_close = True,bg_color = "None",
		radius = dp(10),overlay_color = None,**kwargs):
		
		if bg_color == "None":
			bg_color = self.sc.aff_col3
		if not overlay_color:
			overlay_color = self.sc.overlay_color
		
		th_surf = self.sc.get_modal_surf(surf,titre,show_close,self.close_modal, 
			bg_color,radius = radius)
		self.modal = ModalView(auto_dismiss = auto_dismiss,
			overlay_color = overlay_color,**kwargs)
		self.modal.add_widget(th_surf)
		self.modal.open()
		self.sc.add_to_modal(self.modal)

	def close_modal(self,*args):
		self.add_all()
		self.sc.sup_from_modal(self.modal)
		self.modal.dismiss()

# Gestion de la récupération de la liste de date
	def get_date_list(self,day1,day2):
		"""
			Permet d'obtenir la liste de date d'un jour 1
			à un jour 2
		"""
		d1,m1,y1 = day1.split("-")
		d2,m2,y2 = day2.split('-')

		month_list = self._month_from_years(y1,y2)
		m_y1 = f"{m1}-{y1}"
		m_y2 = f"{m2}-{y2}"
		real_month_list = self._get_month_list(m_y1,m_y2,month_list)

		all_days_liste = self._get_all_days(real_month_list)
		real_days_liste = self._get_real_days(day1,day2,all_days_liste)
		return real_days_liste

	def _month_from_years(self,y1,y2):
		y1 = int(y1)
		y2 = int(y2)
		info_liste = list()
		for y in range(y1,y2+1):
			for m in range(1,13):
				m = str(m)
				if len(m) < 2:
					m = "0"+m
				inf = f'{m}-{y}'
				info_liste.append(inf)
		return info_liste

	def _get_month_list(self,m_y1,m_y2,info_liste):
		try:
			if info_liste:
				ind1 = info_liste.index(m_y1)
				ind2 = info_liste.index(m_y2)
				month_list = info_liste[ind1:ind2+1]
				return month_list
		except:
			pass
		return list()

	def days_from_month(self,m,y):
		G_liste = calendar.monthcalendar(y,m)
		real_liste = list()
		for liste in G_liste:
			for d in liste:
				if d != 0:
					if len(str(d)) < 2:
						d = '0' + str(d)
					if len(str(m)) < 2:
						m = '0' + str(m)
					inf = f"{d}-{m}-{y}"
					real_liste.append(inf)
		return real_liste

	def _get_all_days(self,month_list):
		gene_liste = list()
		for m_y in month_list:
			m,y = m_y.split('-')
			m = int(m)
			y = int(y)
			gene_liste.extend(self.days_from_month(m,y))
		return gene_liste

	def _get_real_days(self,date1,date2,gene_days_liste):
		try:
			if gene_days_liste:
				ind1 = gene_days_liste.index(date1)
				ind2 = gene_days_liste.index(date2)
				days_liste = gene_days_liste[ind1:ind2+1]
				return days_liste
			else:
				return list()
		except:
			return list()

	def get_datetime(self,date):
		forma_str = "%d-%m-%Y"
		date_obj = datetime.datetime.strptime(date,forma_str)
		return date_obj

# Gestion de triage des dates
	def Sort_date(self,liste):
		if type(liste)== dict:
			liste = [i for i in liste.keys()]
		re_done = list()
		for k in liste:
			date = self.re_do_date(k)
			d = {'date':date}
			re_done.append(d)
		re_done.sort(key = itemgetter('date'),reverse = True)
		re_done = [self.get_normal_date(i.get('date')) for i in re_done]
		return re_done

	def Get_mois_ind(self,mois):
		dic = {
			"Janvier":1,
			"Février":2,
			"Mars":3,
			"Avril":4,
			"Mai":5,
			"Juin":6,
			"Juillet":7,
			"Août":8,
			"Septembre":9,
			"Octobre":10,
			"Novembre":11,
			"Décembre":12,
		}
		for k,v in dic.items():
			if mois.lower() in k.lower():
				return self.get_mois(v)

	def Get_mois_IND(self,ind):
		if type(ind) == int:
			ind = str(ind)
		dic = {
			"1":"Janvier",
			"2":"Février",
			"3":"Mars",
			"4":"Avril",
			"5":"Mai",
			"6":"Juin",
			"7":"Juillet",
			"8":"Août",
			"9":"Septembre",
			"10":"Octobre",
			"11":"Novembre",
			"12":"Décembre",
		}
		return dic[str(int(ind))]

	def get_mois(self,v):
		v = str(v)
		if len(v)==1:
			v = '0'+v
		return v

	def get_normal_date(self,date):
		y = date[:4]
		m = date[4:6]
		j = date[6:8]
		return f"{j}-{m}-{y}"
	
	def re_do_date(self,date):
		j,m,y = date.split('-')
		if len(m)==1:
			m = "0"+m
		if len(j)==1:
			j = "0"+j
		date = y+m+j
		return date

	def check(self,dic):
		for k,v in dic.items():
			if not v:
				return False
		return True

# Gestion de choix de fichier
	def get_img_from(self,wid):
		self.file_chooser(self.fonc)

	def get_file_from(self,wid):
		self.file_chooser(self.fonc)

	def fonc(self,fic):
		self.file_link = fic
		self.th_image_srf.source = fic

	def file_chooser(self,fonc = None):
		root = Tk()
		root.withdraw()
		fichier = askopenfilename(
			title = "Choix de fichier",
			filetypes = [("Tous les fichier","*.*")]
		)
		if not fonc:
			fonc = self.upload_fic
		fonc(fichier)

	def upload_fic(self,selection):
		self.file_selected = selection

# Gestion de notification
	def notify(self,message,title = "Alerte"):
		try:
			notification.notify(title,message,timeout = 2)
		except:
			print(message)

# Gestion automatique des données
	def UPdate_info(self):
		"""
			cette méthode est utilisé pour permettre
			une mise à jour des données et une mise à
			jour de l'écran aussi. il est préférable 

		"""
		pass

# Autres
	def check_access(self,access):
		if self.access_liste == "all":
			return True
		else:
			if access in self.access_liste:
				return True
			else:
				return False

	def get_date_first_ech(self,dic):
		if dic:
			dates = [datetime.datetime.strptime(i,self.date_format) for i in dic.keys()]
			dates.sort()
			if len(dates)>1:
				return dates[1].strftime(self.date_format),dates
		return self.sc.get_today(),list()

	def regul_input(self,text):
		text = str(text)
		txt = str()
		inf = '0123456789.-'
		if text == '-':
			return "-0"
		for i in text:
			if i in inf:
				txt+= i
		txt = txt.replace('--','-')
		if txt.endswith('-'):
			txt = txt[:-1]
		if not txt:
			txt = str(0)
		try:
			float(txt)
		except:
			txt = str(0)
		return txt

	def get_pourc(self,dic):
		t = len(dic)
		th = int()
		for i in dic.values():
			if i:
				th += 1
		return str(round(th*100/t))+"%"

	def Get_qts_str(self,liste):
		th_qte = dict()
		for d in liste:
			q_unit = d.get('qté_uni')
			u_unit = d.get('uni_uni')
			qte = d.get('qté')
			uni = d.get('unité')
			if qte:
				th_q = th_qte.get(q_unit)
				if not th_q:
					th_q = float()
				th_q += float(qte)
				th_qte[q_unit] = th_q
			if uni:
				th_u = th_qte.get(u_unit)
				if not th_u:
					th_u = float()
				if qte:
					th_u += float(qte)
				th_qte[u_unit] = th_u
		qtr = str()
		for k,v in th_qte.items():
			qtr += f" {v}{k},"
		qtr = qtr[:-1]
		return qtr

	def get_autre_m(self,dic):
		M = float()
		for i,m in dic.items():
			M += float(m)
		return M

	def Get_format_val(self,val):
		try:
			float(val)
		except:
			return val
		else:
			return self.format_val(val)

	def Get_real_num(self,num):
		if num:
			try:
				date,num = num.split('N°')[-1].split('_')
				d,m,y = date.split('-')
				N = f"{y}{m}{d}_{num}"
				return N
			except:
				return 0
		return 0

	def apply_num_ordre(self,liste,key = "Num"):
		for th_key,val in enumerate(liste):
			val[key] = th_key+1
		return liste

	def excecute(self,fonc,*args):
		#fonc(*args)
		self.sc.executor.submit(fonc,*args)

# Méthode de gestion d'action universel
	def open_link(self,lien):
		try:
			Window.set_system_cursor('wait')
			if lien and type(lien) == str:
				os.startfile(lien)
			Window.set_system_cursor('arrow')
		except FileNotFoundError:
			self.notify('Le chemin vers le fichier est introuvable!')

	def Popup_impression(self,class_imp):
		class_imp(self)

	def _save_file_(self):
		# Dossier public Download
		path = "/sdcard/ZoeCorp"
		if not os.path.exists(path):
			os.makedirs(path)
