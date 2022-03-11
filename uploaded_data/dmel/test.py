from sys import argv

infile = open(argv[1])
for line in infile:
	data = line.split('\t')
#2L	10311991	-	CG5385	E	C	-	21179090	Graveley	2011
	print "3\t%s\t%s\t%s\tA\tA\tI\t%s\t0\t%s\t%s\t%s\t%s\t%s\t%s"%(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9][:-1])
infile.close()
