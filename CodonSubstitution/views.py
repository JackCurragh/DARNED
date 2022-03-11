#===============================================================================
# Don't dare to change this code if you don't know what is written here and what
# are you planning to do. :Anmol Kiran
#===============================================================================


# Create your views here.
from django.http import HttpResponseRedirect
# from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.template.loader import get_template
from django.http import HttpResponse
import string

from forms import *
# Imaginary function to handle an uploaded file.

#===============================================================================
# Codon Informations
#===============================================================================

codon = {'AAA' : 'K', 'ACA' : 'T', 'AGA' : 'R', 'ATA' : 'I',
         'AAC' : 'N', 'ACC' : 'T', 'AGC' : 'S', 'ATC' : 'I',
         'AAG' : 'K', 'ACG' : 'T', 'AGG' : 'R', 'ATG' : 'M',
         'AAT' : 'N', 'ACT' : 'T', 'AGT' : 'S', 'ATT' : 'I',
         'CAA' : 'Q', 'CCA' : 'P', 'CGA' : 'R', 'CTA' : 'L',
         'CAC' : 'H', 'CCC' : 'P', 'CGC' : 'R', 'CTC' : 'L',
         'CAG' : 'Q', 'CCG' : 'P', 'CGG' : 'R', 'CTG' : 'L',
         'CAT' : 'H', 'CCT' : 'P', 'CGT' : 'R', 'CTT' : 'L',
         'GAA' : 'E', 'GCA' : 'A', 'GGA' : 'G', 'GTA' : 'V',
         'GAC' : 'D', 'GCC' : 'A', 'GGC' : 'G', 'GTC' : 'V',
         'GAG' : 'E', 'GCG' : 'A', 'GGG' : 'G', 'GTG' : 'V',
         'GAT' : 'D', 'GCT' : 'A', 'GGT' : 'G', 'GTT' : 'V',
         'TAA' : '*', 'TCA' : 'S', 'TGA' : '*', 'TTA' : 'L',
         'TAC' : 'Y', 'TCC' : 'S', 'TGC' : 'C', 'TTC' : 'F',
         'TAG' : '*', 'TCG' : 'S', 'TGG' : 'W', 'TTG' : 'L',
         'TAT' : 'Y', 'TCT' : 'S', 'TGT' : 'C', 'TTT' : 'F',
         # RNA specific
         'AUA' : 'I', 'AUC' : 'I', 'AUG' : 'M',
         'AAU' : 'N', 'ACU' : 'T', 'AGU' : 'S', 'AUU' : 'I',
         'CUA' : 'L', 'CUC' : 'L', 'CUG' : 'L',
         'CAU' : 'H', 'CCU' : 'P', 'CGU' : 'R', 'CUU' : 'L',
         'GUA' : 'V', 'GUC' : 'V', 'GUG' : 'V',
         'GAU' : 'D', 'GCU' : 'A', 'GGU' : 'G', 'GUU' : 'V',
         'UAA' : '*', 'UCA' : 'S', 'UGA' : '*', 'UUA' : 'L',
         'UAC' : 'Y', 'UCC' : 'S', 'UGC' : 'C', 'UUC' : 'F',
         'UAG' : '*', 'UCG' : 'S', 'UGG' : 'W', 'UUG' : 'L',
         'UAU' : 'Y', 'UCU' : 'S', 'UGU' : 'C', 'UUU' : 'F'
         }
#===============================================================================
# 
#===============================================================================


def wwwcodon( request ):
    if request.method == 'POST':
        form = File_Upload( request.POST, request.FILES )
        if form.is_valid():
            infile = request.FILES['filename']
            frame = int( request.POST['frame'] )  # Change it to correct format
            #===================================================================
            # Storing sequence names and sequences in a dictionary
            #===================================================================
            alignseq = {}
            for line in infile:
                #print line
                data = line[:-1].split()
		if 'CLUSTAL' in line or len( data ) < 2 or '*' in data[0] or '.' in data[0] or ':' in data[0]: 
                    continue
                seqname, seq = data[0], data[1]
                if alignseq.has_key( seqname ):
                    alignseq[seqname] += seq
                else:
                    alignseq[seqname] = seq[frame:]
            codon_color = {}
            nonsyn_vs_syn = {}
            tnonsyn = {}
            tsyn = {}
            for j in range( 0, len( alignseq[alignseq.keys()[0]] ), 3 ):
                tmpcodon = []
                for key in alignseq.keys():
                    tmpcodon.append( alignseq[key][j:j + 3] )
                tmpcdn = set( tmpcodon )
                for tmdn in list( tmpcdn ):
                    if '-' in tmdn:
                        tmpcdn -= set( [tmdn] )
                        
                cdnCount = []
                tmpcdn = list( tmpcdn )
                for tmdn in tmpcdn:
                    cdnCount.append( tmpcodon.count( tmdn ) )
                # print tmpcdn, cdnCount
                    
                if cdnCount != []:
                    maxcdn = tmpcdn[cdnCount.index( max( cdnCount ) )]
                temp_non_syn = 1
                temp_syn = 1
                for key in alignseq.keys():
                    if not codon.has_key( alignseq[key][j:j + 3] ) or maxcdn == alignseq[key][j:j + 3] or len( alignseq[key][j:j + 3] ) < 3 or '-' in alignseq[key][j:j + 3]:
                        clr = ''
                        if '-' in alignseq[key][j:j+3]:
                            temp_non_syn += 1
                    elif codon[maxcdn] == codon[alignseq[key][j:j + 3]]:
                        clr = 'green'
                        temp_syn += 1
                    else:
                        clr = '#8A4117'
                        temp_non_syn += 1
                    if codon.has_key( alignseq[key][j:j + 3] ) and codon[alignseq[key][j:j + 3]] == '*':
                        clr = '#E6A9EC'
                        temp_non_syn += 1
                    
                    if codon_color.has_key( key ):
                        codon_color[key].append( clr )
                    else:
                        codon_color[key] = [clr]
                nonsyn_vs_syn[j/3]=temp_syn*1.0/temp_non_syn
                tnonsyn[j/3] = temp_non_syn - 1
                tsyn[j/3] = temp_syn - 1

            to_return = "<html><head></head><body><table>" 
            for key in alignseq.keys():
                to_return += "<tr style='height:5px'><td>%s</td><td></td>" % key 
                for j in range( len( codon_color[key] ) ):
                    to_return += "<td bgcolor='%s'>%s</td>" % ( codon_color[key][j], alignseq[key][3 * j:3 * j + 3] ) 
                to_return += "</tr>" 
            rat = "<tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td><td></td>"
            nonsyn = "<tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td><td></td>"
            syn = "<tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td><td></td>"
        
            for j in range(len(codon_color[alignseq.keys()[0]])):
                rat += "<td>%.2f</td>" %nonsyn_vs_syn[j]
                nonsyn += "<td>%d</td>" %tnonsyn[j]
                syn += "<td>%d</td>" %tsyn[j]
            rat +="</tr>"
            syn += "</tr>"
            nonsyn += "</tr>"
            to_return += syn + nonsyn + rat


            to_return += "</table></body></html>"
            to_return = filter(lambda x:x in string.printable,to_return)
            template = get_template( 'res.html' )
            return HttpResponse( template.render( RequestContext( request, {'result':to_return} ) ) )
        else:
            print "Form is not valid"
    else:
        template = get_template( 'codon.html' )
        var = {}
        var = {
                'aln':File_Upload()
              }
        return HttpResponse( template.render( RequestContext( request, var ) ) )
