from django import forms

ORG = (('HU','Human'),
       ('DR','Drosophila')
	)

class File_Upload(forms.Form):
    org = forms.ChoiceField(ORG)
    filename = forms.FileField()
