#Coding:utf-8
"""
	Module de définition des décorateurs de fonction pour 
	ajouter des fonctionalités aux surfaces
"""

def Wid_Updater(wid):
	"""
		Cette décorateur doit être appliquée sur les 
		méthodes qui commence la définition des éléments
		d'une partie de surface.
	"""
	wid.clear_widgets()
	def update(func):
		def wrapper(*args,**kwargs):
			func(*args,**kwargs)
		return wrapper
	return update
