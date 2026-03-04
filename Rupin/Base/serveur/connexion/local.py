#Coding:utf-8
"""
	Gestion de la base Local sqlite
"""
import sqlite3
from pathlib import Path
import json, sys
from datetime import datetime
import threading
import string
import traceback

def success_response(self,data,where,id,action):
	if self.cur:
		self.cur.close()
		self.cur = self.conn.cursor()
	return {
		"status":'ok',
		"data":data,
		"message":f'{action} {where} at {id} went successfully',
		"action":action,
		"where":where
	}
def failed_response(self,data,where,id,action,E = None):
	if not E:
		E = traceback.format_exc()
	if self.cur:
		self.cur.close()
		self.cur = self.conn.cursor()
	return {
		"status":'error',
		"data":data,
		"message":f'{action} {where} at {id} went wrong. \n this is what goes wrong:\n{E}',
		"action":action,
		"where":where
	}

def open_local_connexion(self):
	Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

	# check_same_thread=False si tu comptes accéder depuis plusieurs threads (Kivy)
	self.conn = sqlite3.connect(self.db_path, timeout=5.0, check_same_thread=False)
	self.conn.row_factory = sqlite3.Row  # accès par noms de colonnes
	self.cur = self.conn.cursor()

	# PRAGMAs conseillés pour mobile
	self.cur.execute("PRAGMA journal_mode=WAL;")
	self.cur.execute("PRAGMA synchronous=NORMAL;")
	self.cur.execute("PRAGMA foreign_keys=ON;")
	self.cur.execute("PRAGMA busy_timeout=5000;")  # ms
	self.cur.close()
	
def close_local_connexion(self):
	"""Ferme proprement la base."""
	if self.cur:
		self.cur.close()
		self.cur = None
	if self.conn:
		self.conn.close()
		self.conn = None

