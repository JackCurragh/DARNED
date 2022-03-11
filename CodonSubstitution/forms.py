from django import forms

frms = ( ( 0, '0' ), ( 1, '1' ), ( 2, '2' ) )


class File_Upload( forms.Form ):
    frame = forms.ChoiceField( frms )
    filename = forms.FileField()
class File_Upload2( forms.Form ):
    fasta_file = forms.FileField()
