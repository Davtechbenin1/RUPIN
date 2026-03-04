#Coding:utf-8
"""
	Gestion du module de windows
"""
import cv2
from tkinter import filedialog
from tkinter import Tk
from win10toast import ToastNotifier
import geocoder, time

class g_windows:
	def __init__(self):
		self.file_url = None
		self.gps_pos = None

	def tacke_picture(self,fonc):
		cap = cv2.VideoCapture(0)

		ret, frame = cap.read()
		if ret:
			filename = f"photo_{int(time.time())}.jpg"
			cv2.imwrite(filename, frame)
			self.file_url = filename
		else:
			self.file_url = None

		fonc(self.file_url)

		cap.release()

	def pick_f(self,fonc):
		root = Tk()
		root.update()
		root.withdraw()
		root.attributes('-topmost',True)

		file_path = filedialog.askopenfilename()
		self.file_url = file_path if file_path else None

		fonc(self.file_url)

	def get_th_loc(self,fonc):
		g = geocoder.ip('me')
		if g.ok:
			self.gps_pos = {
				"lat": g.latlng[0],
				"lon": g.latlng[1]
			}
		else:
			self.gps_pos = None

		fonc(self.gps_pos)

	def notify(self, title, message):
		toaster = ToastNotifier()
		toaster.show_toast(title, message, duration = 5,
			threaded = True)