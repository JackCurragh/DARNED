from django import forms



HS_ASSEMBLY = tuple([(j,'HG'+str(j)) for j in range(18,20)])
HS_CHROM = tuple([(str(j),'Chr'+str(j)) for j in range(1,23)]+[('X','ChrX'),('Y','ChrY')])

MM_ASSEMBLY = ((9,'MM9'),(10,'MM10'))
MM_CHROM = tuple([(str(j),'Chr'+str(j)) for j in range(1,20)]+[('X','ChrX'),('Y','ChrY')])

DM_ASSEMBLY = ((3,'DM3'),(3,'DM3'))
DM_CHROM = (('2L','Chr2L'),
            ('2R','Chr2R'),
            ('3L','Chr3L'),
            ('3R','Chr3R'),
            ('4','Chr4'),
            ('X','ChrX'))

STRAND = (('+','+'),('-','-'))
SEQTYPE = (('A','All'),('E','Exon'),('I','Intron'),('O','Other'))
EXOTYPE = (('A','All'),('C','CDS'),('5','5\'UTR'),('3','3\'UTR'))
SEQNAMES = (('refGene','RefGene'),('refSeq','RefSeq'))

#Human's Searches
class HS_Searches(forms.Form):
    hs_assembly = forms.ChoiceField(HS_ASSEMBLY,widget=forms.Select(attrs={'auto_id':'False'}))
    hs_chrom = forms.ChoiceField(HS_CHROM)
    hs_start = forms.IntegerField()
    hs_end = forms.IntegerField()
    hs_flank = forms.IntegerField()#default 0, non it not permitted 
    hs_seqtype = forms.ChoiceField(SEQTYPE,widget=forms.Select(attrs={'onchange':"hs_displayExonType('id_hs_seqtype');"}))
    hs_exotype = forms.ChoiceField(EXOTYPE)
    hs_source = forms.CharField()#add js for autosuggesion
    hs_seq = forms.CharField(widget=forms.Textarea(attrs={'cols':'100','rows':'15'}))
    hs_seqname = forms.ChoiceField(SEQNAMES)
    hs_seqid = forms.CharField()



#Drosophila Seraches
class DM_Searches(forms.Form):
    dm_assembly = forms.ChoiceField(DM_ASSEMBLY)
    dm_chrom = forms.ChoiceField(DM_CHROM)
    dm_start = forms.IntegerField()#add widget to check it is an int(js methods)
    dm_end = forms.IntegerField()#same as start#default value 0
    dm_flank = forms.IntegerField()#default 0, non it not permitted 
    dm_seqtype = forms.ChoiceField(SEQTYPE,widget=forms.Select(attrs={'onchange':"dm_displayExonType('id_dm_seqtype');"}))
    dm_exotype = forms.ChoiceField(EXOTYPE)
    dm_seq = forms.CharField(widget=forms.Textarea(attrs={'cols':'100','rows':'15'}))
    dm_seqname = forms.ChoiceField(SEQNAMES)
    dm_seqid = forms.CharField()

#Mouse Seraches
class MM_Searches(forms.Form):
    mm_assembly = forms.ChoiceField(MM_ASSEMBLY)
    mm_chrom = forms.ChoiceField(MM_CHROM)
    mm_start = forms.IntegerField()#add widget to check it is an int(js methods)
    mm_end = forms.IntegerField()#same as start#default value 0
    mm_flank = forms.IntegerField()#default 0, non it not permitted 
    mm_seqtype = forms.ChoiceField(SEQTYPE,widget=forms.Select(attrs={'onchange':"mm_displayExonType('id_mm_seqtype');"}))
    mm_exotype = forms.ChoiceField(EXOTYPE)
    mm_seq = forms.CharField(widget=forms.Textarea(attrs={'cols':'100','rows':'15'}))
    mm_seqname = forms.ChoiceField(SEQNAMES)
    mm_seqid = forms.CharField()


