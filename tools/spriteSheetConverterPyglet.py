import sys
import string

'''infoString = """Gebrauch: 

	1. und letztes Argument: Dateiname (mit Endung 'txt') angeben
	Die Datei muss mit 'Sprite Sheet Packer' erstellt worden sein.

	Aus der txt-Datei wird eine json-Datei erstellt, die mit pyglet importiert wird.
	hierbei muss beachtet werden, das y von unten nach oben geht.
	"""
if len(sys.argv) < 2:

	print infoString

	sys.exit(0)

filename = sys.argv[1]'''

f=open("infantry.txt", "r")

result = "{\n"

data = []
lines = f.readlines()
for line in lines:
	#tmpData = []
	#tmpData.append(line.split())
	data.append(line.split())

print data

'''for i in range(len(data)):
	result += "\t\t{\n"
	result += "\t\t\t-- " + data[i][0] + "\n"
	result += "\t\t\tx=" + data[i][2] + ",\n"
	result += "\t\t\ty=" + data[i][3] + ",\n"
	result += "\t\t\twidth=" + data[i][4] + ",\n"
	result += "\t\t\theight=" + data[i][5] + ",\n"
	result += "\t\t},\n"

result += "\t},\n"
result += "}\n"

result += "\nSheetInfo.frameIndex =\n"
result += "{\n"

for i in range(len(data)):
    
    result += "\t" + "[\"" + data[i][0] + "\"]" + " = " + str(i+1) + ",\n"

result +="}\n"

result += """
function SheetInfo:getSheet()
    return self.sheet;
end

function SheetInfo:getFrameIndex(name)
    return self.frameIndex[name];
end

return SheetInfo"""
'''

result += "}\n"
'''newfilename = string.replace(filename, "txt", "lua")
of = open(newfilename, "w")
of.write(result)
of.close()'''