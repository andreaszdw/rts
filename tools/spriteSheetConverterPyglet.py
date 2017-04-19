#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string
import pyglet
import os

'''infoString = """Gebrauch: 

	1. und letztes Argument: Dateiname (mit Endung 'txt') angeben
	Die Datei muss mit 'Sprite Sheet Packer' erstellt worden sein.

	Aus der txt-Datei wird eine json-Datei erstellt, die mit pyglet importiert wird.
	hierbei muss beachtet werden, das y von unten nach oben geht.

	Die ssp Textdatei und die dazugehörige png-datei muss im gleichen Verzeichnis sein,
	damit die Umrechnung der y-Koordinate erfolgen kann.
	"""
if len(sys.argv) < 2:

	print infoString

	sys.exit(0)

filename = sys.argv[1]'''

filename = "infantry.txt"

f=open(filename, "r")

imageName = os.path.splitext(filename)[0] + ".png"

image = pyglet.image.load(imageName)

imageHeight = image.height


result = "{"

data = []
lines = f.readlines()
for line in lines:	
	data.append(line.split())

# check for first time iter, because of the correct comma setting
tmpFirstTime = True

for i in data:

	if tmpFirstTime:
		result += "\n\t\"" + i[0] + "\"" + ":\n"
	else:
		result += ",\n\t" + "\"" + i[0] + "\"" + ":\n"
	result += "\t{\n"
	result += "\t\t\"" + "x" + "\": " +  i[2] + ",\n"

	# do y conversion to opengl coordinates
	tmpY = imageHeight - int(i[3]) - int(i[5])
	result += "\t\t\"" + "y" + "\": " + str(tmpY) + ",\n"

	result += "\t\t\"" + "w" + "\": " + i[4] + ",\n"
	result += "\t\t\"" + "h" + "\": " + i[5] + "\n"
	result += "\t}"

	tmpFirstTime = False

result += "\n}"

print result

newfilename = string.replace(filename, "txt", "json")
of = open(newfilename, "w")
of.write(result)
of.close()