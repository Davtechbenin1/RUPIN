import os, sys
import os.path
import platform
from pathlib import Path

from kivy.uix.modalview import ModalView
import traceback
from datetime import datetime
import subprocess

class Android_file_manager:
	def __init__(self):
		from jnius import autoclass

		self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
		self.context = self.PythonActivity.mActivity

		self.MiniFileAccess = autoclass('org.zoecorp.MiniFileAccess')

	def get_file_path(self,file_name):
		file_path = self.MiniFileAccess.getFilePath(self.context, file_name)
		return file_path

	def write_file(self,file_name,content):
		result = self.MiniFileAccess.writeToFile(self.context, file_name, content)
		return result

	def append_to(self,file_name,content):
		result_append = self.MiniFileAccess.appendToFile(self.context, file_name, content)
		return result_append

	def open_file(self,file_name):
		self.MiniFileAccess.openFile(self.context, file_name, "application/pdf")

	def share_file(self,file_name):
		self.MiniFileAccess.shareFile(self.context, file_name, "application/pdf")

def error_log(message):
	from datetime import datetime
	now = datetime.now()
	fic_name = now.strftime("%H-%M.txt")
	date_dir = now.strftime('%Y-%m-%d')

	if "android" in sys.modules:
		manager = Android_file_manager()
		path = manager.get_file_path(f"Log/{date_dir}/{fic_name}")
		manager.append_to(f"Log/{date_dir}/{fic_name}", message + '\n\n')
	else:
		log_pat = Path("Log") / date_dir
		os.makedirs(log_pat, exist_ok=True)
		with open(log_pat / fic_name, 'a', encoding='utf-8') as fic:
			fic.write(message)
			fic.write('\n\n')
	print(message)


def GET_FILE_DIRECTORY(fic):
    if "android" in sys.modules:
        manager = Android_file_manager()
        return manager.get_file_path(fic)
    else:
        base_dir = Path.home() / "Documents" / "ZoeCorp"
        os.makedirs(base_dir, exist_ok=True)
        return str(base_dir / fic)


def open_pdf(file_name):
	import os, subprocess, platform
	if "android" in sys.modules:
		manager = Android_file_manager()
		manager.open_file(file_name)
	else:
		file_path = GET_FILE_DIRECTORY(file_name)
		if platform.system().lower() == 'windows':
			os.startfile(file_path)
		elif platform.system().lower() == "darwin":
			subprocess.run(["open", file_path])
		elif platform.system().lower() == "linux":
			subprocess.run(['xdg-open', file_path])
		else:
			raise OSError('Type de system non reconnu')

def add_intent_error(E):
	error_log(f"{E}\n{traceback.format_exc()}")
