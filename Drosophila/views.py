# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext,loader
from time import time
import MySQLdb
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from DARNED.forms import *
from models import *
from os import system
from xml.dom import minidom


dbpth = "/home/DATA/Anmol/DARNED" #'/home/common_share/DARNED'
sttc = dbpth+"/staticfiles" #'/home/common_share/DARNED/staticfiles'
blstdb = dbpth+"/blast_databases/Drosophila" #"/home/common_share/DARNED/blast_databases/Drosophila"


def range_based(request):
    assembly = request.GET['dm_assembly']
    chrom = request.GET['dm_chrom']
    seqtype = request.GET['dm_seqtype']
    exotype = request.GET['dm_exotype']
    flank = request.GET['dm_flank']
    gene = request.GET.get('gene','')
    pubid = request.GET.get('pubid','')
    end = request.GET.get('dm_end','0')
    start = request.GET.get('dm_start','0')
    try:
        start = int(start)
        end = int(end)
        flank = int(flank)
    except:
        tmplt = loader.get_template("message.html")
        return HttpResponse(tmplt.render(RequestContext(request,{'message':'Start, end and/or flank are/is either empty or not a number)'})))
    coors = DMCoordinate.objects.filter(assembly = assembly,chrom=chrom,coordinate__gte=start,coordinate__lte=end).select_related(depth=2).extra(select={'gstart':'coordinate-%d'%int(flank),'gend':'coordinate+%d'%int(flank)}).order_by('coordinate')
    if seqtype !='A':
        if seqtype == 'E':
            if exotype == 'A':
                coors = coors.filter(seqtype='E')
            if exotype == 'C':
                coors = coors.filter(exotype='C')
            elif exotype == '5':
                coors = coors.filter(exotype='5')
            elif exotype == '3':
                coors = coors.filter(exotype='3')
        elif seqtype == 'I':
            coors = coors.filter(seqtype='I')
        else:
            coors = coors.filter(seqtype='O')
    if pubid != '':
        coors = coors.filter(pubid__pubid=pubid)
    if gene != '':
        coors = coors.filter(gene__gene=gene)
    if len(coors) ==0:
        tmplt = loader.get_template("message.html")
        return HttpResponse(tmplt.render(RequestContext(request,{'message':'No result found for your query'})))
#############Bed File Part##########
    countfile = open(dbpth+"/count")
    count = int(countfile.read())
    countfile.close()
    countfile = open(dbpth+"/count",'w')
    countfile.write("%d"%((count+1)%200))
    countfile.close()
    bedfile = open("%s/bed/bed_%d.bed"%(sttc,count),"w")
    resultFile = open("%s/res/results%d.txt"%(sttc,count),'w')
    bedfile.write('browser dense\ntrack name="Drosophila RNA Editing" description="EDITING LOCATIONS" visibility=2 itemRgb="On"\n')
    resultFile.write("chrom\tcoordinate\tstrand\tinchr\tinrna\tgene\tseqReg\texReg\tPubMed ID\n")
    for coor in coors:#need coloring here
        barcolor=""
        tpub=""
        tgene = ""
        tseq = "O"
        texo = ""
        if coor.gene != None:
            tgene=coor.gene.gene
            if coor.exotype != None:
                tseq = "E"
                texo = coor.exotype
            else:
                tseq="I"
        for pbd in coor.pubid.all():
            tpub += ",%d"%pbd.pubid
        resultFile.write("%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(coor.chrom,coor.coordinate,coor.strand,coor.indna,coor.inrna,tgene,tseq,texo,tpub[1:]))
	#Other Black 0-0-0
        #Intron Red  255-0-0
        #CDS Blue    0-0-255
        #5UTR Dark Green 0-100-0
        #3UTR Deep Pink	255-20-147
        if coor.seqtype=='O':
            barcolor = '0,0,0'
        elif coor.seqtype=='I':
            barcolor='255,0,0'
        else:
            if coor.exotype=='C':
                barcolor='0,0,255'
            elif coor.exotype=='5':
                barcolor='0,100,0'
            else:
                barcolor='255,20,147'
        bedfile.write("chr%s\t%d\t%d\tchr%s.%d\t1000\t%s\t%d\t%d\t%s\n"%(coor.chrom,coor.coordinate-1,coor.coordinate,coor.chrom,coor.coordinate,coor.strand,coor.coordinate-1,coor.coordinate,barcolor))
    bedfile.close()
    resultFile.close()
###################################
    genesearch = "dm_assembly=%s&dm_chrom=%s&dm_seqtype=%s&dm_exotype=%s&dm_flank=%s&pubid=%s&dm_start=%s&dm_end=%s&gene="%(assembly,chrom,seqtype,exotype,flank,pubid,start,end)
    authorsearch = "dm_assembly=%s&dm_chrom=%s&dm_seqtype=%s&dm_exotype=%s&dm_flank=%s&gene=%s&dm_start=%s&dm_end=%s&pubid="%(assembly,chrom,seqtype,exotype,flank,gene,start,end)
    exonsearch = "dm_assembly=%s&dm_chrom=%s&dm_seqtype=%s&dm_flank=%s&gene=%s&pubid=%s&dm_start=%s&dm_end=%s&dm_exotype="%(assembly,chrom,seqtype,flank,gene,pubid,start,end)
    seqsearch = "dm_assembly=%s&dm_chrom=%s&dm_exotype=%s&dm_flank=%s&gene=%s&pubid=%s&dm_start=%s&dm_end=%s&dm_seqtype="%(assembly,chrom,exotype,flank,gene,pubid,start,end)

    searchRes = {'coors':coors,
                'genesearch':genesearch,
                'authorsearch':authorsearch,
                'exonsearch':exonsearch,
                'seqsearch':seqsearch,
                'chrom':chrom,
                'start':start,
                'end':end,
                'seqtype':seqtype,
                'exotype':exotype,
                'gene':gene,
                'assembly':assembly,
                'bed':count,
                'flank':flank,
		'assembly':assembly,
		'rescount':len(coors)
                }
    tmplt = loader.get_template('Drosophila/result.html')
    rendred = tmplt.render(RequestContext(request,searchRes))
    return HttpResponse(rendred)
#############################################################################
#############################################################################
#######For sequence based analysis###########################################

###########Checking nucleotide sequence######################################
def nucleotide_check(seq):#
    nuc = set()
    nucl_bool = 0
    for line in seq:
        nuc |= set([c for c in line if c not in ' \n'])
    print nuc
    for n in nuc:
        if n.upper() not in ('ACGTRYKMSWBDHVNU'):#Replace if it gives error
            nucl_bool = 1
            break
    return nucl_bool
###########################Checking fasta file format########################
def fasta_nucleotide_check(fl):
    infile = open(fl)
    lines = infile.readlines()
    fasta_bool = 0
    if lines[0][0] == '>':
        fasta_bool = 1
    if fasta_bool == 1:
        dna_bool = nucleotide_check(lines[1:])
    else:
        dna_bool = nucleotide_check(lines)
    return fasta_bool,dna_bool

def seq_based(request):
    if request.method == 'POST':
        assembly = request.POST['dm_assembly']
        countfile = open(dbpth+"/count")
        count = int(countfile.read())
        countfile.close()
        countfile = open(dbpth+"/count",'w')
        countfile.write("%d"%((count+1)%200))
        countfile.close()
	fl = "%s/tmp/seq%d.fa"%(dbpth,count)#make changes from here on
        seqfile = open(fl, "w")
        seq = request.POST['dm_seq']
        if len(seq)==0:
            tmplt = loader.get_template('message.html')
            return HttpResponse(tmplt.render(RequestContext(request,{'message':'You did not provide the sequence'})))
        seqfile.write(seq)
        seqfile.close()
	fasta_bool,dna_bool = fasta_nucleotide_check(fl)
	if not fasta_bool:
	    infile = open("%s/tmp/seq%d.fa"%(dbpth,count))
	    seq = infile.read()
	    infile.close()
	    outfile = open("%s/tmp/seq%d.fa"%(dbpth,count), "w")
	    outfile.write(">userseq\n"+seq)
	    outfile.close()
        #print "Anmol","%s/exe/blastn -max_target_seqs 1 -evalue 10 -word_size 50 -outfmt 5 -dust no -db /home/devil/Desktop/Dmel/dm3 -query %s/tmp/seq%d.fa -out %s/tmp/seq%d.xml"%(pth,pth,count%50,pth,count%50)
			
        system("%s/exe/blastn -max_target_seqs 1 -evalue 10 -word_size 50 -outfmt 5 -dust no -db %s/dm%s/dm%s -query %s/tmp/seq%d.fa -out %s/tmp/seq%d.xml"%(dbpth,blstdb,assembly,assembly,dbpth,count,dbpth,count))
        xmldoc = minidom.parse("%s/tmp/seq%d.xml"%(dbpth,count))
        hits = xmldoc.getElementsByTagName('Hit')
        if len(hits)==0:
            tmplt = loader.get_template('message.html')
            return HttpResponse(tmplt.render(RequestContext(request,{'message':'No hit found for your sequence.'})))
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
                    #print tstart,tend,chrom
                    data.append([chrom[3:],tstart,tend,strand,[]])
                    arraylen = len(data)
                    coord = []
                    editings = DMCoordinate.objects.filter(assembly=assembly,chrom=chrom[3:], coordinate__gte = tstart, coordinate__lte= tend, strand = strand)
                    for editing in editings:
                        if strand == '+':
                            coord.append(editing.coordinate)
                        else:
                            coord.append(editing.coordinate)
                    coord.sort()
                    #print coord
                    trealpos = tstart
                    qrealpos = qstart
                    startbl =0
                    spl = 0 
                    nml = 0
                    qseqt = ''
                    tseqt = ''
                    matcht = ""
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
                            startbl =0
                            spl = 0 
                            nml = 0
                            qseqt = ""
                            tseqt = ""
                            matcht = ""
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

            tmplt = loader.get_template("Drosophila/blast.html")
            return HttpResponse(tmplt.render(RequestContext(request,{'datas':data,'assembly':assembly})))
    else:
        tmplt = loader.get_template("message.html")
        return HttpResponse(tmplt.render(RequestContext(request,{'message':'Please go to search page to submit your query'})))



####################Gene Based Searches##############################

def geneBased(request):# Remove EST from Hereford
    if request.method == 'POST':
	seqname = request.POST['dm_seqid']
	assembly = request.POST['dm_assembly']
	if len(seqname) == 0:
            tmplt = loader.get_template("message.html")
            return HttpResponse(tmplt.render(RequestContext(request, {'message':"Please go back to serach page and provide query RefGene or RefSeq ID."})))
        seqtype = request.POST['dm_seqname']
        bl = 0
	gene = ''
        if seqtype == "refGene":
	    gene = seqname.upper()
            coors = DMCoordinate.objects.filter(assembly=assembly,gene__gene=seqname.upper()).select_related(depth=2).extra(select={'gstart':'coordinate-1','gend':'coordinate+1'}).order_by('coordinate')
            if len(coors)>0:
                bl = 1
        elif seqtype == "refSeq":
            conn = MySQLdb.connect(db='darned_dm%s'%assembly,user="Anmol")#Change db on working server
            cursor = conn.cursor()
            if cursor.execute("SELECT name2 from refGene WHERE name='%s' LIMIT 1"%(seqname)):
                gene = cursor.fetchone()[0]
                coors = DMCoordinate.objects.filter(assembly=assembly,gene__gene=gene).select_related(depth=2).extra(select={'gstart':'coordinate-1','gend':'coordinate+1'}).order_by('coordinate')
                if len(coors)>0:
                    bl = 1
            cursor.close()
            conn.close()
        if bl==1:
	#############Bed File Part##########
	    countfile = open(dbpth+"/count")
	    count = int(countfile.read())
	    countfile.close()
	    countfile = open(dbpth+"/count",'w')
	    countfile.write("%d"%((count+1)%200))
	    countfile.close()
	    bedfile = open("%s/bed/bed_%d.bed"%(sttc,count),"w")
	    resultFile = open("%s/res/results%d.txt"%(sttc,count),'w')
	    bedfile.write('browser dense\ntrack name="Drosophila RNA Editing" description="EDITING LOCATIONS" visibility=2 itemRgb="On"\n')
	    resultFile.write("chrom\tcoordinate\tstrand\tinchr\tinrna\tgene\tseqReg\texReg\tPubMed ID\n")
	    for coor in coors:#need coloring here
		barcolor=""
		tpub=""
                tgene=""
                tseq = ""
                texo = ""
                if coor.gene != None:
                    tgene = coor.gene.gene
                    if coor.exotype != None:
                        tseq = 'E'
                        texo = coor.exotype
                    else:
                        tseq = 'I'
		for pbd in coor.pubid.all():
		    tpub += ",%d"%pbd.pubid
		resultFile.write("%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(coor.chrom,coor.coordinate,coor.strand,coor.indna,coor.inrna,tgene,tseq,texo,tpub[1:]))
		#Other Black 0-0-0
		#Intron Red  255-0-0
		#CDS Blue    0-0-255
		#5UTR Dark Green 0-100-0
		#3UTR Deep Pink	255-20-147
		if coor.seqtype=='O':
		    barcolor = '0,0,0'
		elif coor.seqtype=='I':
		    barcolor='255,0,0'
		else:
		    if coor.exotype=='C':
		        barcolor='0,0,255'
		    elif coor.exotype=='5':
		        barcolor='0,100,0'
		    else:
		        barcolor='255,20,147'
		bedfile.write("chr%s\t%d\t%d\tchr%s.%d\t1000\t%s\t%d\t%d\t%s\n"%(coor.chrom,coor.coordinate-1,coor.coordinate,coor.chrom,coor.coordinate,coor.strand,coor.coordinate-1,coor.coordinate,barcolor))
	    bedfile.close()
	    resultFile.close()
	###################################
            coordinate = []
            chrom = ''
            for coor in coors:
                coordinate.append(coor.coordinate)
                chrom = coor.chrom
	    seqtype = 'A'
	    exotype = 'A'
	    flank = '1'
	    pubid = ''
	    source = ''
	    end = max(coordinate)+1
	    start = min(coordinate)-1
	    genesearch = "dm_assembly=%s&dm_chrom=%s&dm_seqtype=%s&dm_exotype=%s&dm_flank=%s&pubid=%s&dm_start=%s&dm_end=%s&gene="%(assembly,chrom,seqtype,exotype,flank,pubid,start,end)
	    authorsearch = "dm_assembly=%s&dm_chrom=%s&dm_seqtype=%s&dm_exotype=%s&dm_flank=%s&gene=%s&dm_start=%s&dm_end=%s&pubid="%(assembly,chrom,seqtype,exotype,flank,gene,start,end)
	    exonsearch = "dm_assembly=%s&dm_chrom=%s&dm_seqtype=%s&dm_flank=%s&gene=%s&pubid=%s&dm_start=%s&dm_end=%s&dm_exotype="%(assembly,chrom,seqtype,flank,gene,pubid,start,end)
	    seqsearch = "dm_assembly=%s&dm_chrom=%s&dm_exotype=%s&dm_flank=%s&gene=%s&pubid=%s&dm_start=%s&dm_end=%s&dm_seqtype="%(assembly,chrom,exotype,flank,gene,pubid,start,end)
	    searchRes = {'coors':coors,
			'genesearch':genesearch,
			'authorsearch':authorsearch,
			'exonsearch':exonsearch,
			'seqsearch':seqsearch,
			'chrom':chrom,
			'start':start,
			'end':end,
			'seqtype':seqtype,
			'exotype':exotype,
			'gene':gene,
                        'bed':count,
                        'flank':flank,
                        'assembly':assembly,
			'rescount':len(coors)
			}

            tmplt = loader.get_template("Drosophila/result.html")
            return HttpResponse(tmplt.render(RequestContext(request,searchRes)))
#            coors = []
#            for row in rows:
#                coors.append([row[0][3:],row[1],row[2]])
#            data = {'assembly':assembly,'coors':coors}
#            tmplt = loader.get_template("common/blastOut.html")
#            return HttpResponse(tmplt.render(RequestContext(request,data)))
            #return HttpResponseRedirect("/hrb/?assembly=%s&chrom=%s&start=%d&end=%d"%(assembly,row[0][3:],row[1],row[2]))
        else:
            tmplt = loader.get_template('message.html')
            return HttpResponse(tmplt.render(RequestContext(request, {'message':"No Result Found"})))
    else:
        tmplt = loader.get_template('message.html')
        return HttpResponse(tmplt.render(RequestContext(request, {'message':"Please go to search page."})))
