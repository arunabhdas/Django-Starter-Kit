from django import forms
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminBase

from tinymce.widgets import TinyMCE


class FlatPageForm(forms.ModelForm):

    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = FlatPage

class FlatPageAdmin(FlatPageAdminBase):
    
    form = FlatPageForm
 
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
