from django.template import loader, RequestContext,Context


############File ojects###########
#from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
##################################

#########HTML responses###################
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
#########################################

#######Form modules###############
from forms import * # by Anmol
from django import forms
##################################

######## Models and choices ########
#from choices import * #by Anmol
from models import *
####################################

#######General Python Modules#######
from re import split # move it admin_view
from os import system
from xml.dom import minidom
###################################i
### For tissue autocomplete##
from django.utils import simplejson
#####


import MySQLdb
conn = MySQLdb.connect(user='Anmol')
cursor=conn.cursor()


def visitors(request,page):
    ip = request.META['REMOTE_ADDR']
    ipt = Visitors(ip=ip,page=page,time=datetime.now())
    ipt.save()



def lookup(request):
#    result = ['Brain','Liver']
    if request.method == "GET":
        if request.GET.has_key('query'):
            value = request.GET['query']
            if len(value)>2:
                model_result = Tissue.objects.filter(tissue_icontains=value)
                result = [x.tissue for x in model_result]
                json = simplejson.dumps(result)
    return HttpResponse(json,mimetype='application/json')




def seqBased(request):
    #def visitors(request,'Sequence Based Search')
    if request.method == 'POST':
        form = SequenceBased(request.POST)
        if form.is_valid():
            assembly = form.cleaned_data['assembly']
            countfile = open("/home/DATA/Anmol/DARNED/static/count")
            count = int(countfile.read())
            countfile.close()
            countfile = open("/home/DATA/Anmol/DARNED/static/count",'w')
            countfile.write("%d"%(count+1))
            countfile.close()
            seqfile = open("/home/DATA/Anmol/DARNED/temp/seq%d.fa"%(count%50), "w")
            seqfile.write(">seq%d\n%s"%(count%50,form.cleaned_data['sequence']))
            seqfile.close()
            system("/home/DATA/Anmol/DARNED/executables/blastn -max_target_seqs 1 -evalue 10 -word_size 50 -outfmt 5 -dust no -db /home/DATA/Anmol/DARNED/blast_databases/Hsapiens/hg%s/hg%s -query /home/DATA/Anmol/DARNED/temp/seq%d.fa -out /home/DATA/Anmol/DARNED/temp/seq%d.xml"%(assembly,assembly,count%50,count%50))
            xmldoc = minidom.parse("/home/DATA/Anmol/DARNED/temp/seq%d.xml"%(count%50))
            hits = xmldoc.getElementsByTagName('Hit')
            data = []
            for hit in hits:
                chrom = hit.getElementsByTagName('Hit_def')[0].firstChild.data
                hit_hsps = hit.getElementsByTagName('Hit_hsps')
                for hit_hsp in hit_hsps:
                    hsps = hit_hsp.getElementsByTagName('Hsp')
                    for hsp in hsps:
                        tstart = int(hsp.getElementsByTagName('Hsp_hit-from')[0].firstChild.data)
                        tend = int(hsp.getElementsByTagName('Hsp_hit-to')[0].firstChild.data)
                        qstart = int(hsp.getElementsByTagName('Hsp_query-from')[0].firstChild.data)
                        strnd = hsp.getElementsByTagName('Hsp_hit-frame')[0].firstChild.data
                        qseq = hsp.getElementsByTagName('Hsp_qseq')[0].firstChild.data
                        tseq = hsp.getElementsByTagName('Hsp_hseq')[0].firstChild.data
                        match = hsp.getElementsByTagName('Hsp_midline')[0].firstChild.data
                        if strnd == '1':
                            strand = '+'
                        else:
                            strand = '-'
                            tstart,tend = tend,tstart

                        data.append([chrom[3:],tstart,tend,strand,[],assembly])
                        arraylen = len(data)
                        coord = []
                        editings = Main.objects.filter(assembly=assembly,chrom=chrom[3:], coordinate__gte = tstart, coordinate__lte= tend, strand = strand)
                        for editing in editings:
                            if strand == '+':
                                coord.append(editing.coordinate)
                            else:
                                coord.append(editing.coordinate)
                        coord.sort()
                        print coord
                        trealpos = tstart
                        qrealpos = qstart
                        startbl = spl = nml = 0
                        qseqt = tseqt = matcht = ""
                        virtualSeqLen = len(tseq)
                        for j in range(virtualSeqLen):
                            if (j != 0 and j%50 == 0) or j == virtualSeqLen-1:
                                tseqt += "</b></td>"
                                qseqt += "</b></td>"
                                matcht += "</pre></b></td>"
                                if strand == '+':
                                    data[arraylen-1][4].append([qstartpos,tstartpos,qseqt,matcht,tseqt,qrealpos-1,trealpos-1])
                                else:
                                    data[arraylen-1][4].append([qstartpos,tend-tstartpos+tstart,qseqt,matcht,tseqt,qrealpos-1,tend+tstart-trealpos+1])
                                startbl = spl = nml = 0
                                qseqt = tseqt = matcht = ""
                            if startbl == 0:
                                qstartpos = qrealpos
                                tstartpos = trealpos
                                startbl = 1
                            if tseq[j] != '-':
                                trealpos += 1
                            if qseq[j] != '-':
                                qrealpos += 1
                            if trealpos-1 in coord:
                                    if spl == 0 :
                                        tseqt += "<td><b>"
                                        qseqt += "<td><b>"
                                        matcht += "<td><b><pre>"
                                        spl = nml = 1
                                    tseqt += "<font style='background-color:#BDBDBD'>%s</font>"%tseq[j]
                                    qseqt += "<font style='background-color:#BDBDBD'>%s</font>"%qseq[j]
                                    matcht += "<font style='background-color:#BDBDBD'>%s</font>"%match[j]
                            else:
                                if nml == 0:
                                    tseqt += "<td><b>%s"%tseq[j]
                                    qseqt += "<td><b>%s"%qseq[j]
                                    matcht += "<td><b><pre>%s"%match[j]
                                    nml = spl = 1
                                else:
                                    tseqt += tseq[j]
                                    qseqt += qseq[j]
                                    matcht += match[j]

            tmplt = loader.get_template("common/blast.html")
            return HttpResponse(tmplt.render(RequestContext(request,{'datas':data})))


def regionBased(request):
    #visitors(request,'Region Based Search')
    if request.method == 'GET':
        chrom = request.GET.get('chrom','')
        start = request.GET.get('start','')
        end = request.GET.get('end','')
        assembly = request.GET.get('assembly','')
        seqtype = request.GET.get('seqtype','A')
        exoreg = request.GET.get('exoType','A')
        source = request.GET.get('source','')
        flank = request.GET.get('flank','0')
        author = request.GET.get('author','')
        gene = request.GET.get('gene','')


    else:
        assembly = request.POST['assembly']
        chrom = request.POST['chrom']
        start = request.POST['start']
        end = request.POST['end']
        seqtype = request.POST['seqType']
        exotype = request.POST['exoType']
        flank = request.POST['flank']
        source = request.POST['source']
        author = ''
        gene = ''

    editings = Main.objects.filter(assembly = assembly,chrom = chrom).extra(select={'gstart':'coordinate-%d'%int(flank),'gend':'coordinate+%d'%int(flank)})
    if int(end) != 0:
        editings = editings.filter(coordinate__gte = start,coordinate__lte=end)

    if seqtype != 'A':
        editings = editings.filter(seqtype = seqtype)
        if seqtype == 'E':
            if exotype != 'A':
                editings = editings.filter(exotype = exotype)
    if len(source) !=0:
        editings = editings.filter(tissue__tissue=source.upper)
    if len(author) != 0:
        editings = editings.filter(pubid__pubid=author)
    if len(gene) != 0:
        editings = editings.filter(gene__gene=gene)
    countfile = open("/home/DATA/Anmol/DARNED/static/count")
    count = int(countfile.read())
    countfile.close()
    countfile = open("/home/DATA/Anmol/DARNED/static/count","w")
    countfile.write("%d"%(count+1))
    countfile.close()
    bedfile = open("/home/DATA/Anmol/DARNED/static/bedfile/bedfile%d.bed"%(count%50),"w")
    searchedData = open("/home/DATA/Anmol/DARNED/static/searched/res%d.txt"%(count%50),'w')
    bedfile.write('''browser dense\ntrack name="Human RNA editing" description="EDITING LOCATIONS" visibility=2 itemRgb="On"\n''')
    searchedData.write("chr\tcoordinate\tstrand\tinchr\tinrna\tgene\tseqreg\texreg\n")
    for editing in editings:
        if editing.seqtype=='E':
            if editing.exotype=="C":
                color = "0,0,255"
            elif editing.exotype=="5":
                color = "0,100,0"
            else:
                color = "255,20,147"
        elif editing.seqtype=="I":
            color = "255,0,0"
        else:
            color = "0,0,0"
        if editing.gene:
            gen = editing.gene.gene
        else:
            gen = '-'
        if editing.exotype:
            exo = editing.exotype
        else:
            exo = '-'
        bedfile.write("chr%s\t%d\t%d\tchr%s.%d\t1000\t%s\t%d\t%d\t%s\n"%(editing.chrom,editing.coordinate-1,editing.coordinate,editing.chrom,editing.coordinate,editing.strand,editing.coordinate-1,editing.coordinate,color))
        searchedData.write("%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n"%(editing.chrom,editing.coordinate,editing.strand,editing.dnanuc,editing.rnanuc,gen,editing.seqtype,exo))
    
    
    bedfile.close()
    searchedData.close()
    if end=='0':
        end = 10000000000
    displaydata = {
                   'total':len(editings),
                   'editings':editings,
                   'chrom':chrom,
                   'start':start,
                   'end':end,
                   'assembly':assembly,
                   'count':count%50,
                }
    tmplt = loader.get_template('common/result.html')
    return HttpResponse(tmplt.render(RequestContext(request,displaydata)))

def geneBased(request):# Remove EST from Hereford
    #visitors(request,'Gene Based Search')
    form = GeneBased(request.POST)
    if form.is_valid():
        assembly = form.cleaned_data['assembly']
        seqtype = form.cleaned_data['nametype']
        seqName = form.cleaned_data['seqname']
        #return HttpResponse(type(assembly))
        bl = 0
        if seqtype == "refgene":
            editings = Main.objects.filter(assembly=assembly,gene__gene=seqName.upper())
            if len(editings)>0:
                bl = 1
        elif seqtype == "refseq":
                if cursor.execute("SELECT name2 from HG%s.refGene WHERE name='%s' LIMIT 1"%(assembly,seqName)):
                    gene = cursor.fetchone()[0]
                    editings = Main.objects.filter(assembly=assembly,gene__gene=gene)
                    if len(editings)>0:
                        bl = 1
        if bl==1:
            countfile = open("/home/DATA/Anmol/DARNED/static/count")
            count = int(countfile.read())
            countfile.close()
            countfile = open("/home/DATA/Anmol/DARNED/static/count","w")
            countfile.write("%d"%(count+1))
            countfile.close()
            tmplt = loader.get_template("common/generes.html")
            return HttpResponse(tmplt.render(RequestContext(request,{'editings':editings,'assembly':assembly})))
#            coors = []
#            for row in rows:
#                coors.append([row[0][3:],row[1],row[2]])
#            data = {'assembly':assembly,'coors':coors}
#            tmplt = loader.get_template("common/blastOut.html")
#            return HttpResponse(tmplt.render(RequestContext(request,data)))
            #return HttpResponseRedirect("/hrb/?assembly=%s&chrom=%s&start=%d&end=%d"%(assembly,row[0][3:],row[1],row[2]))
        else:
            return HttpResponse("No Result Found.")
    return HttpResponse("Sequence Name Is Empty.")

