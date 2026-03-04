#Coding:utf-8
"""
	Gestion des apis ANDROID
"""
from jnius import autoclass

from .permission import PermissionManager
from .camera import CameraManager
from .files import FileManager
from .gps_hand import GPSManager
from .result_dispatcher import ResultDispatcher

class g_android(PermissionManager,CameraManager,FileManager,
	GPSManager):
	def __init__(self):

		self._load_core()
		self._load_storage()
		self._load_permissions()

		self.result_dispatcher = ResultDispatcher(self.activity)

		PermissionManager.__init__(self)
		CameraManager.__init__(self)
		FileManager.__init__(self)
		GPSManager.__init__(self)

	def _load_core(self):
		self.my_activity = autoclass("org.kivy.android.PythonActivity")
		self.activity = self.my_activity.mActivity
		self.my_intent = autoclass("android.content.Intent")
		self.my_media_store = autoclass("android.provider.MediaStore")
		self.my_uri_hand = autoclass("android.net.Uri")

	def _load_storage(self):
		self.my_file_hand = autoclass("java.io.File")
		self.my_file_provider = autoclass("androidx.core.content.FileProvider")

	def _load_permissions(self):
		self.my_context_compat = autoclass("androidx.core.content.ContextCompat")
		self.my_activity_compat = autoclass("androidx.core.app.ActivityCompat")
		self.my_package_manager = autoclass("android.content.pm.PackageManager")


# Gestion ds permissions
	def camera_permission(self,callback):
		perm = "android.permission.CAMERA"
		ret = self._permission_hand(perm, callback)
		return ret,

	def stockage_permission(self,callback):
		perm1 = 'android.permission.READ_EXTERNAL_STORAGE'
		perm2 = 'android.permission.WRITE_EXTERNAL_STORAGE'
		ret1 = self._permission_hand(perm1,callback)
		ret2 = self._permission_hand(perm2,callback)
		return ret1,ret2

	def gps_permission(self,callback):
		perm1 = "android.permission.ACCESS_FINE_LOCATION"
		perm2 = "android.permission.ACCESS_COARSE_LOCATION"
		ret1 = self._permission_hand(perm1,callback)
		ret2 = self._permission_hand(perm2,callback)
		return ret1, ret2

	def micro_permission(self,callback):
		perm = "android.permission.RECORD_AUDIO"
		ret = self._permission_hand(perm,callback)
		return ret

	def notification_permission(self,callback):
		perm = "android.permission.POST_NOTIFICATIONS"
		ret = self._permission_hand(perm,callback)
		return ret

	def internet_permission(self,callback):
		perm = "android.permission.INTERNET"
		ret = self._permission_hand(perm,callback)
		return ret

	def media_permission(self,callback):
		perm1 = "android.permission.READ_MEDIA_IMAGES"
		perm2 = "android.permission.READ_MEDIA_VIDEO"
		perm3 = "android.permission.READ_MEDIA_AUDIO"
		ret1 = self._permission_hand(perm1,callback)
		ret2 = self._permission_hand(perm2,callback)
		ret3 = self._permission_hand(perm3,callback)
		return ret1,ret2,ret3

	def _permission_hand(self,perm,callback):
		if self.check_permission(perm):
			return True
		else:
			self.request_permission(perm,callback)
			return False

# Autres
	def tacke_picture(self,fonc):
		self.file_url = None
		def pic(result):
			if not result:
				self.file_url = None
			else:
				self.file_url = result.getPath()

			fonc(self.file_url)

		self.open_camera(pic)

	def pick_f(self,fonc):
		self.file_url = None
		def pic(result):
			if not result:
				self.file_url = None
			else:
				self.file_url = result.getPath()
			fonc(self.file_url)

		self.pick_file(pic)

	def get_th_loc(self,fonc):
		self.gps_pos = None
		def loc(result):
			if not result:
				self.gps_pos = None
			else:
				self.gps_pos = result

			fonc(self.gps_pos)

		self.get_location(loc)


