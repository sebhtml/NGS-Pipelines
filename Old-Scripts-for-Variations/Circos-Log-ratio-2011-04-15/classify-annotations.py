import sys

files={}

for line in sys.stdin:
	tokens=line.split()
	if len(tokens)<3:
		continue
	tag=tokens[2].strip()
	if tag not in files:
		files[tag]=open(tag+".gff","w+")
	files[tag].write(line+"\n")

for i in files.items():
	i[1].close()
