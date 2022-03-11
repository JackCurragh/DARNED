from sys import argv

infile = open(argv[1])
for line in infile:
	data = line.split()
	if len(data)<18:
		continue
	print "%s\t%s\t%s\t%s\t%s\tA\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],data[17])
infile.close()
