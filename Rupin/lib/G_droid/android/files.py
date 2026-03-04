#Coding:utf-8
from jnius import autoclass

class FileManager:
	def __init__(self):
		self.REQUEST_CODE_FILE = 3000

	def pick_file(self, callback, mime_type="*/*"):
		"""Ouvre le sélecteur de fichiers"""
		def permission_cb(granted):
			if granted:
				self._launch_file_picker(callback, mime_type)
			else:
				print("Permission stockage refusée")

		# demander toutes les permissions nécessaires pour lire
		self.stockage_permission(permission_cb)

	def _launch_file_picker(self, callback, mime_type):
		intent = self.my_intent(self.my_intent.ACTION_GET_CONTENT)
		intent.setType(mime_type)
		intent.addCategory(self.my_intent.CATEGORY_OPENABLE)

		self.activity.startActivityForResult(intent, self.REQUEST_CODE_FILE)
		self.result_dispatcher.register(self.REQUEST_CODE_FILE, callback)
		