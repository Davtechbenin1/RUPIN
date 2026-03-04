#Coding:utf-8
from jnius import PythonJavaClass, java_method

class ResultDispatcher:
	def __init__(self, activity):
		self.activity = activity
		self._callbacks = {}
		self._hook_activity_result()

	def register(self, request_code, callback):
		self._callbacks[request_code] = callback

	def _hook_activity_result(self):
		activity = self.activity
		manager = self

		class ActivityResultListener(PythonJavaClass):
			__javainterfaces__ = ['org/kivy/android/PythonActivity$ActivityResultListener']
			__javacontext__ = 'app'

			def __init__(self):
				super().__init__()

			@java_method('(IILandroid/content/Intent;)Z')
			def onActivityResult(self, requestCode, resultCode, data):
				callback = manager._callbacks.get(requestCode, None)
				if callback:
					callback(data)
					del manager._callbacks[requestCode]
					return True
				return False

		self.listener = ActivityResultListener()
		activity.bind(on_activity_result=self.listener.onActivityResult)
