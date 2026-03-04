#Coding:utf-8

"""
	Réécriture de dp et sp
"""

import kivy.metrics as MET
import sys


def dp(val):
	if type(val) == str:
		val = int(val.split("dp")[0])
	th_val = MET.dp(val)
	if not th_val:
		return th_val
	elif th_val:
		th_val = round(th_val,0)
		if not th_val:
			th_val = 1
		return th_val

def sp(val):
	if type(val) == str:
		val = int(val.split("sp")[0])
	th_val = MET.sp(val)
	if not th_val:
		return th_val
	elif th_val:
		th_val = round(th_val,0)
		if not th_val:
			th_val = 1
		return th_val

