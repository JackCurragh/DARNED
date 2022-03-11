from Human.models import *
from sys import argv
import settings
##############################################
########Thoughts for implementation##########
#Current state of update########

def human(flname):
    infile = open(flname)
    for line in infile:
        data = line[:-1].split('\t')
        if len(data) != 19:
            #tmplt = loader.
            print "Send Error that it is no related to humans"
        coor = HSCoordinate.objects.filter(assembly=int(data[0]),chrom=data[1],coordinate=int(data[2]),strand=data[3],indna = data[4],inref = data[5], inrna = data[6])#add nucleotide info
        if len(coor) != 0:
            if data[15] != '-':
                tissues = data[15].split(',')
                for tissue in tissues:
                    if len(tissue)<2:
                        continue
                    tis = coor.filter(source__source = tissue.upper())
                    if len(tis) == 0:
                        try:
                            tss = HSSource.objects.get(tissue=tissue.upper())
                        except:
                            tss = HSSource.objects.create(tissue=tissue.upper())
                        coor.tissue.add(tss)
            pubids = data[16].split(':')
            authors = data[17].split(':')
            years = data[18].split(':')
            pubnum = len(pubids)
            for j in range(pubnum):
                pbd = coor.filter(pubid__pubid=pubids[j])
                if len(pbd) == 0:
                    try:
                        pbdx = HSPubMed.objects.get(pubid=pubids[j])
                    except:
                        pbdx = HSPubMed.objects.create(pubid = pubids[j],author=authors[j],year=years[j])
                    coor.pubid.add(pbdx)

        else:
            coor = HSCoordinate.objects.create(assembly=int(data[0]),chrom=data[1],coordinate=int(data[2]),strand=data[3], indna=data[4],inref=data[5],inrna=data[6],seqtype = data[12])
            if data[7] != '-':
                coor.snp =  data[7]
                if data[8]=='+':
                    coor.snpunvalid = 1
                else:
                    coor.snpunvalid = 0
                validations = data[9].split(',')
                for validation in validations:
                    try:
                        vld = HSSnpValidation.objects.get(validation=validation)
                    except:
                        vld = HSSnpValidation.objects.create(validation=validation)
                    coor.snpvalidation.add(vld)
            print data[11]
            if data[10] != '-':
                if data[12] == 'E':
                    coor.exotype = data[13]
                try:
                    gene = HSGene.objects.get(gene=data[10])
                except:
                    print data[10],data[11],data[12],data[13]
                    gene = HSGene.objects.create(gene=data[10],geneid=int(data[11]))
                coor.gene = gene
            if data[14] != '-':
                coor.alu = data[13]
            if data[15] != '-':
                sources = data[15].split(',')
                for source in sources:
                    if len(source) <2:
                        continue
                    try:
                        src = HSSource.objects.get(source = source.upper())
                    except:
                        src = HSSource.objects.create(source = source.upper())
                    coor.source.add(src)
            pubmeds = data[16].split(':')
            authors = data[17].split(':')
            years = data[18].split(':')
            pubnum = len(pubmeds)
            for j in range(pubnum):
                try:
                    pbd = HSPubMed.objects.get(pubid=pubmeds[j])
                except:
                    pbd = HSPubMed.objects.create(pubid = pubmeds[j],author = authors[j],year=years[j])
                coor.pubid.add(pbd)
            coor.save()

    infile.close()

if __name__=='__main__':
    human(argv[1])
