from jnius import autoclass

class GPSManager:
	def __init__(self):
		self.location_manager = self.my_activity.getSystemService(
			self.my_activity.LOCATION_SERVICE
		)
		# Callback pour retourner la position
		self._current_callback = None

	def get_location(self, callback):
		"""
		Récupère la position GPS actuelle.
		callback(position) sera appelé avec un dictionnaire {"lat": ..., "lon": ...}
		"""
		# enregistrer callback
		self._current_callback = callback

		# demander permissions runtime
		def perm_cb(granted):
			if granted:
				self._request_location()
			else:
				print("Permission GPS refusée")
				self._current_callback(None)

		self.gps_permission(perm_cb)

	def _request_location(self):
		# LocationListener Java
		LocationListener = autoclass('android.location.LocationListener')

		class Listener(LocationListener):
			def onLocationChanged(inner_self, location):
				lat = location.getLatitude()
				lon = location.getLongitude()
				# appeler le callback Python
				self._current_callback({"lat": lat, "lon": lon})
				# désenregistrer après le premier résultat
				self.location_manager.removeUpdates(inner_self)

			def onStatusChanged(inner_self, provider, status, extras):
				pass

			def onProviderEnabled(inner_self, provider):
				pass

			def onProviderDisabled(inner_self, provider):
				pass

		listener = Listener()
		# choisir le provider GPS
		provider = self.location_manager.GPS_PROVIDER

		if not self.location_manager.isProviderEnabled(provider):
			provider = self.location_manager.NETWORK_PROVIDER

		# vérifier à nouveau les permissions avant la requête (sécurité Android)
		if self.check_permission("android.permission.ACCESS_FINE_LOCATION"):
			self.location_manager.requestLocationUpdates(
				provider,
				1000,   # intervalle temps minimum entre maj (ms)
				1,      # distance min (m)
				listener
			)
			