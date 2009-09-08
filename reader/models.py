# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import models as auth

class Tag(models.Model):
    title=models.CharField(max_length=50)
    
    class Meta:
	ordering=["title"]
	db_table="tags"


class Feed(models.Model):
    url=models.URLField(max_length=300)
    last_cheked=models.DateTimeField()
    title=models.CharField(max_length=100)
    subtitle=models.CharField(max_length=100)
    link=models.URLField(max_length=200)

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
    downloaded=models.DateTimeField(auto_now_add=True)

    feed=models.ForeignKey(Feed)
    def __unicode__(self):
	print title+native_id
    
    class Meta:
	db_table="entries"

class Pull(models.Model):
    title=models.CharField(max_length=100)
    tags=models.ManyToManyField(Tag)
    
    class Meta:
	db_table="pulls"

class PullEntry(models.Model):
    pull=models.ForeignKey(Pull)
    entry=models.ForeignKey(Entry)

class FeedFilterPair(models.Model):
    title=models.CharField(max_length=100)
    feed=models.ForeignKey(Feed)
    user=models.ForeignKey(auth.User)
    last_cheked=models.DateTimeField()
    pull=models.ForeignKey(Pull)    

    class Meta:
	db_table="pairs"

class Filter(models.Model):
    type=models.IntegerField(choices=((1,"must"),(2,"may"),(3,"not")))
    value=models.CharField(max_length=50)
    pair=models.ForeignKey(FeedFilterPair)
    
    class Meta:
	db_table="filters"

class Group(models.Model):
    title=models.CharField(max_length=100)
    users=models.ManyToManyField(auth.User)
    pulls=models.ManyToManyField(Pull)
    tags=models.ManyToManyField(Tag)
    
    class Meta:
	ordering=["title"]
	db_table="groups"

class UserPull(models.Model):
    pull=models.ForeignKey(Pull)
    user=models.ForeignKey(auth.User)

class News(models.Model):
    title=models.CharField(max_length=100)
    published=models.DateTimeField(auto_now_add=True)
    text=models.TextField()
