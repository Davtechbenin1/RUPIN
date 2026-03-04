#Coding:utf-8
"""
	Cette classe consiste à une réécriture de la 
	classe Thread pour obtenir la sortie de la
	fonction
"""
from threading import Thread

class My_Thread(Thread):
	def __init__(self,target,args = ()):
		#args ici doit être un tuple
		Thread.__init__(self,target = target,args = args)

		self.Ret_obj = None
		self.target = target
		self.args = args

	def run(self):
		self.Ret_obj = self.target(*self.args)

	def Run(self):
		return self.run()

	def T_join(self):
		if self.is_alive():
			self.join()
		return self.Ret_obj

class Mult_Thread:
	def __init__(self,targets,argss):
		'''
			Ici, il s'agit d'un racourcis qui permet de
			gérer en un seul instant un nombre définie 
			de Thread en même temps.

			targets doit être une liste
			argss doit être une liste contenant des listes
		'''
		self.T_L = [My_Thread(target = t,args = a) for 
		t,a in zip(targets,argss)]

	def start(self):
		"""
			Permet de démarer les Tread sans attendre
			la fin de l'éxécution
		"""
		[T.start() for T in self.T_L]

	def T_join(self):
		[T.T_join() for T in self.T_L]

	def join(self):
		"""
			Cette méthode permet d'attendre la fin de
			chaque thread et retourne chacune de leur
			retour.
		"""
		for T in self.T_L:
			T.start()
		Ret_list = [T.T_join() for T in self.T_L]
		return Ret_list

	def join_all(self):
		return self.join()

	def join_ind(self):
		"""
			Cette méthode permet de retourner le premier
			Thread qui a terminer et possède un retour
			de donné
		"""
		self.start()
		for i in self.T_L:
			ret = i.T_join()
			if ret:
				return ret
		return None
