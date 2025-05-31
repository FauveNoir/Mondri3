#!/usr/bin/env python3

#  __  __                 _      _ ____
# |  \/  |               | |    (_)___ \
# | \  / | ___  _ __   __| |_ __ _  __) |
# | |\/| |/ _ \| '_ \ / _` | '__| ||__ <
# | |  | | (_) | | | | (_| | |  | |___) |
# |_|  |_|\___/|_| |_|\__,_|_|  |_|____/


# fre
# Ce script écoute l'ouverture de nouvelles fenêtres dans i3
# et choisit automatiquement le mode de division (split horizontal ou vertical)
# en fonction du ratio largeur/hauteur de la fenêtre.
# Avec --log, il affiche une trace horodatée des splits effectués.
# Le nom provient de https://fr.wikipedia.org/wiki/Piet_Mondrian

# ara
# يقوم هذا البرنامج بمراقبة النوافذ الجديدة في مدير النوافذ i3،
# ويختار تلقائيًا طريقة التقسيم (أفقي أو عمودي) حسب أبعاد النافذة.
# إذا تم تشغيله باستخدام --log، فإنه يعرض سجلًا زمنيًا لكل عملية تقسيم.
# ال إسم مشتاق من https://ar.wikipedia.org/wiki/%D8%A8%D9%8A%D8%AA_%D9%85%D9%88%D9%86%D8%AF%D8%B1%D9%8A%D8%A7%D9%86

# lat
# Hic scriptum fenestras novas in i3 spectat,
# ac secundum proportionem latitudinis et altitudinis directionem divisionis eligit.
# Cum argumento --log, actiones divisionis cum tempore monstrantur.
# Nomen venit de https://la.wikipedia.org/wiki/Petrus_Mondrian

# en
# This script listens for new windows in the i3 window manager
# and automatically selects a split direction (horizontal or vertical)
# based on the window's width-to-height ratio.
# If run with --log, it prints a timestamped record of each split action.
# The name come from https://en.wikipedia.org/wiki/Piet_Mondrian


import argparse
from datetime import datetime
import i3ipc


def parse_args():
	parser = argparse.ArgumentParser(description="i3 split selector")
	parser.add_argument(
		'--log',
		action='store_true',
		help='Afficher les actions de split dans la sortie standard'
	)
	return parser.parse_args()


def log_split(log_enabled: bool, window_name: str, orientation: str):
	if log_enabled:
		timestamp = datetime.now().isoformat()
		print(f"[i3splitSelector][{timestamp}][{window_name}]Split {orientation} demandé.")


def on_new_window(i3conn, event, log_enabled: bool):
	con = event.container
	width = con.rect.width
	height = con.rect.height
	window_name = con.name or "UnknownWindow"

	if width > height:
		# Fenêtre plus large => split vertical (i3 = split horizontal)
		i3conn.command('split horizontal')
		log_split(log_enabled, window_name, 'vertical')
	else:
		# Fenêtre plus haute => split horizontal (i3 = split vertical)
		i3conn.command('split vertical')
		log_split(log_enabled, window_name, 'horizontal')


def main():
	args = parse_args()
	i3 = i3ipc.Connection()

	# Wrapper pour injecter le flag log_enabled
	def handler(i3conn, event):
		on_new_window(i3conn, event, args.log)

	i3.on('window::new', handler)
	i3.main()


if __name__ == '__main__':
	main()

