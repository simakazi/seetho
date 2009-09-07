# -*- coding: utf-8 -*-
from django import forms

class FeedForm(forms.Form):
    url = forms.URLField(label="Resource URL",initial="http://",max_length=300)
    
