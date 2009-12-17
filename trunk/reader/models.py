# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import models as auth

class Tag(models.Model):
    title=models.CharField(max_length=50)
    
    class Meta:
	ordering=["title"]
	db_table="tags"

class Feed(models.Model):
    url=models.URLField(max_length=300,verify_exists=False)
    last_cheked=models.DateTimeField()
    title=models.CharField(max_length=100)
    subtitle=models.CharField(max_length=100)
    link=models.URLField(max_length=200)

    def __unicode__(self):
	return u"%s (%s)" % (self.url,self.last_cheked)
    
    class Meta:
	ordering=["last_cheked"]
	db_table="feeds"

class Entry(models.Model):
    native_id=models.CharField(max_length=300)
    title=models.CharField(max_length=300)
    summary=models.TextField()
    url=models.URLField(max_length=300)
    downloaded=models.DateTimeField()
    created=models.DateTimeField()

    feed=models.ForeignKey(Feed)
    def __unicode__(self):
	return self.title
    
    class Meta:
	ordering=["-created"]
	db_table="entries"

class Folder(models.Model):
    title=models.CharField(max_length=100)
    tags=models.ManyToManyField(Tag)
    
    class Meta:
	db_table="folders"

class Favor(models.Model):
    user=models.ForeignKey(auth.User)
    entry=models.ForeignKey(Entry)
    
    class Meta:
        db_table="Favors"
        ordering=["entry"]

class FolderEntry(models.Model):
    folder=models.ForeignKey(Folder)
    entry=models.ForeignKey(Entry)

    class Meta:
	ordering=["entry"]

class FeedFilterPair(models.Model):
    title=models.CharField(max_length=100)
    feed=models.ForeignKey(Feed)
    user=models.ForeignKey(auth.User)
    last_cheked=models.DateTimeField()
    folder=models.ForeignKey(Folder)    

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
    members=models.ManyToManyField(auth.User,through='Membership')
    folders=models.ManyToManyField(Folder)
    tags=models.ManyToManyField(Tag)
    
    class Meta:
	ordering=["title"]
	db_table="groups"

class Membership(models.Model):
    user=models.ForeignKey(auth.User)
    group=models.ForeignKey(Group)
    rights=models.CharField(max_length=1,choices=(
    ('C','Creator'),
    ('A','Admin'),
    ('M','Moderator'),
    ('R','Reader'),
    ))

class Topic(models.Model):
    group=models.ForeignKey(Group)
    title=models.CharField(max_length=100)
    started=models.DateTimeField()
    starter=models.ForeignKey(auth.User)
    last_post=models.DateTimeField()

class Comment(models.Model):
    topic=models.ForeignKey(Topic)
    text=models.TextField()
    author=models.ForeignKey(auth.User)
    created=models.DateTimeField()
    carma=models.IntegerField()

class UserFolder(models.Model):
    folder=models.ForeignKey(Folder)
    user=models.ForeignKey(auth.User)
    relation=models.CharField(max_length=1,choices=(
    ('C','Creator'),
    ('F','Friend'),
    ('R','Reader'),
    ))

class News(models.Model):
    title=models.CharField(max_length=100)
    published=models.DateTimeField(auto_now_add=True)
    text=models.TextField()
