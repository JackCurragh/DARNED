from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from admin_forms import *
from django.template import loader,RequestContext

from django.contrib.admin.views.decorators import staff_member_required

from Human.models import *

#######UCSC Tables########
###For UCSC gene, SNP and Alu#####


##########################
#from models import *
from os import system,walk

##############################################
########Thoughts for implementation##########
#Current state of update########

# Try to add information about assembly. And make it auto updatable  
def saveData(uploadedFileName):
    uploadedfile = str(uploadedFileName)

# saving input file conten
######Human update start########
def human(fl):
    infile = open(fl)
    outfile = open(fl+'.err',"w")
    for line in infile:
        data = line[:-1].split('\t')
        print data
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
                    print tissue.upper(),"Anmol"
                    tis = coor.filter(source__source = tissue.upper())
                    if len(tis) == 0:
                        try:
                            tss = HSSource.objects.get(source=tissue.upper())
                        except:
                            tss = HSSource.objects.create(source=tissue.upper())
                        for cr in coor:
                            cr.source.add(tss)
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
                    for cr in coor:
                        cr.pubid.add(pbdx)

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
                coor.alu = data[14]
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
    outfile.close()


#######Human update End######
import os
def flpath():
    print "Anmol is here"
    for flname in os.listdir('./temp'):
        print flname
        human('./temp/'+flname)
