# -*- coding: utf-8 -*-
from django import forms

class FeedForm(forms.Form):
    feed_url = forms.URLField(label="Resource URL",initial="http://",max_length=300)
    feed_cheked = forms.BooleanField(initial=False,required=False)
    filter_must=forms.CharField(initial="",max_length=300,required=False)
    filter_may=forms.CharField(initial="",max_length=300,required=False)
    filter_not=forms.CharField(initial="",max_length=300,required=False)
    folder_title=forms.CharField(initial="New folder",max_length=100)
    folder_id=forms.IntegerField()
    
