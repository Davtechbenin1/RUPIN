#Coding:utf-8

from jnius import java_method, PythonJavaClass

class PermissionManager:
	def __init__(self):
		self._callbacks = {}
		self._request_code_counter = 1000

		self._hook_activity_result()


	def check_permission(self, perm):
		result = self.my_context_compat.checkSelfPermission(
			self.activity.getApplicationContext(),
			perm
		)
		return result == self.my_package_manager.PERMISSION_GRANTED

	def request_permission(self, perm, callback):
		request_code = self._generate_request_code()
		self._callbacks[request_code] = callback
		self.my_activity_compat.requestPermissions(
			self.activity,[perm],request_code)

	def _generate_request_code(self):
		self._request_code_counter += 1
		return self._request_code_counter

	def _hook_activity_result(self):
		activity = self.activity

		class PermissionListener(PythonJavaClass):
			__javainterfaces__ = ['androidx/core/app/ActivityCompat$OnRequestPermissionsResultCallback']
			__javacontext__ = 'app'

			def __init__(self, manager):
				super().__init__()
				self.manager = manager

			@java_method('(I[Ljava/lang/String;[I)V')
			def onRequestPermissionsResult(self, request_code, perms, grant_results):
				callback = self.manager._callbacks.get(request_code, None)
				if callback:
					granted = grant_results[0] == self.manager.my_package_manager.PERMISSION_GRANTED
					callback(granted)

					del self.manager._callbacks[request_code]

		self.listener = PermissionListener(self)
		self.activity.addOnRequestPermissionsResultListener(self.listener)
		