#Coding:utf-8
from jnius import autoclass
import time

class CameraManager:
	def __init__(self):
		self.REQUEST_CODE_CAMERA = 2000  # code unique pour la caméra

	def open_camera(self, callback):
		"""Ouvre la caméra et récupère le résultat via callback"""
		# vérifier la permission avant tout
		def permission_cb(granted):
			if granted:
				self._launch_camera(callback)
			else:
				print("Permission CAMERA refusée")

		self.camera_permission(permission_cb)

	def _launch_camera(self, callback):
		"""Lance l'intent de la caméra"""
		intent = self.my_intent(self.my_media_store.ACTION_IMAGE_CAPTURE)

		# créer un fichier temporaire pour sauvegarder la photo
		photo_file = self._create_image_file()
		photo_uri = self.my_file_provider.getUriForFile(
			self.activity,
			f"{self.activity.getPackageName()}.provider",
			photo_file
		)

		intent.putExtra(self.my_media_store.EXTRA_OUTPUT, photo_uri)
		intent.addFlags(self.my_intent.FLAG_GRANT_WRITE_URI_PERMISSION)
		intent.addFlags(self.my_intent.FLAG_GRANT_READ_URI_PERMISSION)
		self.activity.startActivityForResult(intent, self.REQUEST_CODE_CAMERA)

		# enregistrer le callback pour le dispatcher
		self.result_dispatcher.register(self.REQUEST_CODE_CAMERA, callback)

	def _create_image_file(self):
		"""Crée un fichier temporaire dans le storage externe"""
		File = self.my_file_hand
		storage_dir = self.activity.getExternalFilesDir(None)
		filename = f"photo_{int(time.time())}.jpg"
		return File(storage_dir, filename)
		