# -*- coding: utf-8 -*-
from django.db import models

class Feed(models.Model):
    url=models.URLField(max_length=300)
    last_cheked=models.DateTimeField()
    
    def __unicode__(self):
	print "%s (%s)" % (url,last_cheked)
    
    class Meta:
	ordering=["last_cheked"]
	db_table="feeds"

class Entry(models.Model):
    native_id=models.CharField(max_length=300)
    title=models.CharField(max_length=300)
    summary=models.TextField()
    url=models.URLField(max_length=300)
 
    feed=models.ForeignKey(Feed)
    def __unicode__(self):
	print title+native_id
    
    class Meta:
	db_table="entries"
