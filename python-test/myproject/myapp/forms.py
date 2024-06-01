from django import forms

class UploadFileForm(forms.Form):
    audio_file = forms.FileField()
