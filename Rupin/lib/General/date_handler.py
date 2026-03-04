#Coding:utf-8
"""
	Définition des fonctions et méthodes pour la gestion de la
	date
"""
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

def calcule_date(date_str,valeur,unite = 'j',operation = "+"):
	# format de la date_str: J-M-Y
	# unite in 'jmy'
	date_str = date_str.replace('/','-')
	j,m,y = date_str.split('-')
	if len(y) == 1:
		y = "2"+y
	elif len(y) == 2:
		y = "20"+y
	elif len(y) == 3:
		y = "202"+y
	else:
		y = '2025'
	if not int(m):
		m = '06'
	if not int(j):
		j = "01"
	date_str = f"{j}-{m}-{y}"
	date_obj = datetime.strptime(date_str,"%d-%m-%Y")

	if unite.upper() == "J":
		delta = relativedelta(days = valeur)
	elif unite.upper() == "M":
		delta = relativedelta(months = valeur)
	elif unite.upper() == "Y":
		delta = relativedelta(years = valeur)
	else:
		delta = relativedelta(days = valeur)

	if operation == "+":
		new_date = date_obj + delta
	elif operation == "-":
		new_date = date_obj - delta
	else:
		new_date = date_obj + delta
	return new_date.strftime("%d-%m-%Y")
