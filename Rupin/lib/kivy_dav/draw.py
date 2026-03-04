
import matplotlib
matplotlib.use("Agg")  # indispensable pour génération sans UI

import matplotlib.pyplot as plt
import re,sys
import numpy as np

def get_fig_plot_of(data_list, dates, title, xlabel, ylabel, labels,
	dpi=150, figsize=(8, 5),col_dict = dict()):
	safe_title = re.sub(r"[^\w\-_. ]", "_", title)
	fic_name = f"{safe_title}.jpg"

	plt.figure(figsize=figsize, dpi=dpi)

	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.grid(True, alpha=0.3)
	ind = -1
	for data in data_list:
		th_data = [data.get(j, 0) for j in dates]
		ind += 1
		th_lab = labels[ind]
		col = col_dict.get(th_lab,'black')
		plt.plot(
			dates,
			th_data,
			marker='o',
			solid_joinstyle='round',
			solid_capstyle='round',
			label = th_lab,color = col
		)
		for x,y in zip(dates,th_data):
			plt.text(x,y+10,f'{y}',ha = "center",va = 'bottom',
				fontsize=11,color = col)
	plt.legend()

	plt.tight_layout()
	plt.savefig(fic_name, dpi=dpi)
	plt.close()

	return fic_name

def get_fig_hist_of(
	data_list,
	dates,
	title,
	xlabel,
	ylabel,
	label=str(),
	dpi=150,
	figsize=(8, 5)
):
	dates = list(dates)
	safe_title = re.sub(r"[^\w\-_. ]", "_", title)
	fic_name = f"{safe_title}.jpg"

	plt.figure(figsize=figsize, dpi=dpi)

	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.grid(axis='y', alpha=0.3)

	cmap = plt.cm.get_cmap("tab20")

	for idx, data in enumerate(data_list):
		th_data = [data.get(j, 0) for j in dates]

		# positions X numériques
		x_pos = range(len(dates))

		bars = plt.bar(
			x_pos,
			th_data,
			alpha=0.85,
			label=label,
		)

		# 🎨 couleur + texte par barre
		for i, bar in enumerate(bars):
			bar.set_facecolor(cmap(i % cmap.N))

			height = bar.get_height()
			if height > 0:
				x = bar.get_x() + bar.get_width() / 2
				y = height+10

				txt = f"{height}"

				plt.text(
					x, y,
					txt,
					ha="center",
					va="center",
					fontsize=11,
					color="black",
				)

	# X personnalisés = dates
	plt.xticks(range(len(dates)), dates)

	plt.legend()
	plt.tight_layout()
	plt.savefig(fic_name, dpi=dpi)
	plt.close()

	return fic_name

