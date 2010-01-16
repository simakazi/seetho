# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import models as auth
from datetime import datetime
import time
from reader.feedget import feedparser

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
     
    def Check(self):
        if self.last_cheked<datetime.now() or self.last_cheked==-1:
            print self.url
            R=feedparser.parse(self.url,modified=self.last_cheked.utctimetuple())
            if not self.title:
                try:
                    self.title=R.feed.title
                except:
                    self.title=self.url
                try:
                    self.subtitle=R.feed.subtitle
                except:
                    self.subtitle=""
                try:
                    self.link=R.feed.link
                except:
                    self.link=self.url
            E=R.entries
            self.last_cheked=datetime.now()
            self.save()
            for e in E:
                Entry.fromFeedParser(self,e)
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
    
    @staticmethod
    def fromFeedParser(feed,e):
        eid=""
        if e.has_key("id"):
            eid=e.id
        else:
            eid=e.link
        if not (feed.entry_set.filter(native_id=eid)):
            title=""
            if e.has_key("title"):
                title=e.title
            else:
                title=u"Без заголовка"
            dt=datetime.now()
            en=Entry(native_id=eid,title=title,summary=e.description,url=e.link,feed=feed,downloaded=dt,created=datetime.utcfromtimestamp(time.mktime(e.updated_parsed)))
            en.save()
            feed.last_cheked=dt
            feed.save()
            return True
        return False
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
    title=models.CharField(max_length=100)
    started=models.DateTimeField()
    last_post=models.DateTimeField()

class Comment(models.Model):
    topic=models.ForeignKey(Topic)
    text=models.TextField()
    author=models.ForeignKey(auth.User)
    created=models.DateTimeField()
    carma=models.IntegerField()

class GroupTopic(Topic):
    starter=models.ForeignKey(auth.User)
    group=models.ForeignKey(Group)

class EntryTopic(Topic):
    entry=models.ForeignKey(Entry)

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
