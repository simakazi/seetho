# -*- coding: utf-8 -*-
from django import forms

class FeedForm(forms.Form):
    feed_url = forms.URLField(label="Resource URL",initial="http://",max_length=300)
    feed_cheked = forms.BooleanField(initial=False)
    filter_must=forms.CharField(initial="",max_length=300,required=False)
    filter_may=forms.CharField(initial="",max_length=300,required=False)
    filter_not=forms.CharField(initial="",max_length=300,required=False)
    pull_title=forms.CharField(initial="New pull",max_length=100)
    pull_id=forms.IntegerField()
    
