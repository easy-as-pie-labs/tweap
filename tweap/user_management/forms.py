from django import forms
from django.utils.translation import ugettext


class ImageUploadForm(forms.Form):
    picture = forms.ImageField(
        label=ugettext('Change profile picture'),
        initial=ugettext('No file selected')
    )
