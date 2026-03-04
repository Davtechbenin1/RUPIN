#Coding:utf-8
import platform
import os

if "ANDROID_ARGUMENT" in os.environ:
	from .android import g_android as G_droid

elif platform.system().lower() == "windows":
	from .windows import g_windows as G_droid


