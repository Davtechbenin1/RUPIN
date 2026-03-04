#Coding:utf-8
from lib.davbuild import *

from .compte import compte
from .Prog.client.accueil import accueil
from .Prog.client.recherche import recherche
from .Prog.client.panier import panier

from .Prog.presta.accueil import accueil as presta_acceuil
from .Prog.presta.menus import menus as presta_menus
from .Prog.presta.commandes import commandes as presta_commandes

from .Prog.admin.accueil import accueil as admin_accueil
from .Prog.admin.prestataires import prestataires as admin_prestataires
from .Prog.admin.commandes import commandes as admin_commandes
from .Prog.admin.clients import clients as admin_clients


def clt_part_def(self):
	self.dic = {
		"Accueil":"home",
		"Recherche":"magnify",
		"Panier":"cart",
		"Compte":"account-circle",
	}

	self.surf_def_dic = {
		"Accueil":accueil(self),
		"Recherche":recherche(self),
		"Panier":panier(self),
		"Compte":compte(self),
	}
	return self.dic

def presta_part_def(self):
	self.dic = {
		"Accueil":"home",
		"Vos menus":"briefcase-check",
		"Commandes":"cart-outline",
		"Compte":"account-circle",
	}

	self.surf_def_dic = {
		"Accueil":presta_acceuil(self),
		"Vos menus":presta_menus(self),
		"Commandes":presta_commandes(self),
		"Compte":compte(self),
	}
	return self.dic

def admin_part_def(self):
	self.dic = {
		"Accueil":"home",
		"Prestataires":"account-group",
		"Clients":"account-multiple",
		"Commandes":"cart",
		"Compte":"account-circle",
	}

	self.surf_def_dic = {
		"Accueil":admin_accueil(self),
		"Prestataires":admin_prestataires(self),
		"Clients":admin_clients(self),
		"Commandes":admin_commandes(self),
		"Compte":compte(self),
	}
	return self.dic

def _set_inf_(self):
	self.menu_part.clear_widgets()
	self.menu_but_obj = {}
	self.menu_icon_obj = {}
	if self.sc.curent_interface.lower() == "client":
		part_def = self.clt_part_def()
	elif self.sc.curent_interface.lower() == "prestataire":
		part_def = self.presta_part_def()
	elif self.sc.curent_interface.lower() == "admin":
		part_def = self.admin_part_def()

	for menu,icon in part_def.items():
		b = box(self)
		icon_srf = b.add_icon_but(icon = icon,on_press = self.change_surf,
			info = menu,font_size = "22sp",
			text_color = self.sc.text_col3)
		srf = b.add_button(menu,on_press = self.change_surf,
			info = menu,bg_color = None,
			font_size = "9sp")
		self.menu_but_obj[menu] = srf
		self.menu_icon_obj[menu] = icon_srf
		self.menu_part.add_surf(b)

	self._change_surf(self.curent_show)