from django import forms
from django.utils.translation import ugettext


class ImageUploadForm(forms.Form):
    picture = forms.ImageField(
        label=ugettext('Change profile picture'),
        initial=ugettext('No file selected'),
    )

    def __init__(self, *args, **kwargs):
        super(ImageUploadForm, self).__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs.update({'accept': 'image/*'})