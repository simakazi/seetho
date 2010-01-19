# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseServerError,HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from models import *
from forms import FeedForm
from reader.feedget import feedfinder,feedparser
from datetime import datetime
import time
from django.db.models import Q

@login_required
def add_feed(request):
    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            feed_url=form.cleaned_data['feed_url']
            feed_cheked=form.cleaned_data['feed_cheked']
            filter_must=form.cleaned_data['filter_must']
            filter_may=form.cleaned_data['filter_may']
            filter_not=form.cleaned_data['filter_not']
            folder_title=form.cleaned_data['folder_title']
            folder_id=form.cleaned_data['folder_id']
            if not feed_cheked:
                feed_url=feedfinder.feed(feed_url)
            feed=Feed.objects.filter(url=feed_url)
            if not (feed):
                feed=Feed(url=feed_url,last_cheked="2009-01-01 00:00")
                feed.save()
            else:
                feed=feed[0]
                folder=0
            if (folder_id!=-1):
                folder=Folder.objects.get(id=folder_id)
            else:
                folder=Folder(title=folder_title)
                folder.save()
            pair=FeedFilterPair(folder=folder,feed=feed,user=request.user,last_cheked="2009-01-01 00:00",title="")
            pair.save()
            for q in [(1,filter_must),(2,filter_may),(3,filter_not)]:
                for w in map(lambda x:x.strip(),q[1].split(",")):
                    if w!="":
                        filter1=Filter(type=q[0],value=w,pair=pair)
                        filter1.save()
            if folder_id==-1:
                up=UserFolder(user=request.user,folder=folder,relation='C')
                up.save()
            return HttpResponseRedirect(u"/folder/"+unicode(folder.id))
        else:
            return HttpResponseServerError("You've entered incorrect URL!")
    elif request.method=='GET':
        url=""
        try:
            url=request.GET["u"]
            url=feedfinder.feed(url)
            if not url:
                url="http://"
        except:
            url=""
        folder=None
        try:
            folder=request.GET["f"]
            folder=Folder.objects.get(id=folder)
        except:
            folder=None
        P=Folder.objects.filter(Q(userfolder__user=request.user,userfolder__relation='C'))#|Q(group__members=request.user))
        form = FeedForm()
        return render_to_response("add_feed.html",{"form":form,"folder":folder,"url":url,"user":request.user,"folders":P})
    return HttpResponseServerError("Bad request!")

def list_entry(request,entry_id):
  try:
    entry=Entry.objects.get(id=entry_id)
    return render_to_response("simple_entry.html",{"entry":entry,"user":request.user})
  except:
    return HttpResponseNotFound("No such entry!")

@login_required
def purge_group(request):
    if request.method=='POST':
        try:
            id=request.POST['id']
            Group.objects.filter(id=id).delete()
            return HttpResponse("Ok")
        except:
            return HttpResponseNotFound("")
    else:
        return HttpResponseServerError("Bad request.")

@login_required
def unsubscribe_group(request,group_id):
    try:
        g=Group.objects.get(id=group_id)
        Membership.objects.get(group=g,user=request.user).delete()
        return list_group(request,group_id)
    except:
        return HttpResponseNotFound()

@login_required
def subscribe_group(request,group_id):
    try:
        g=Group.objects.get(id=group_id)
        m=Membership(group=g,user=request.user,rights="R")
        m.save()
        return list_group(request,group_id)
    except:
        return HttpResponseNotFound()

@login_required
def list_group_folder(request,group_id,folder_id):
    try:
        p=Folder.objects.get(id=folder_id)
        full_folder(p)
        e=p.folderentry_set.all()[0:20]
        userfolder=""
        try:
            userfolder=Membership.objects.get(group__id=group_id,user=request.user).rights
            if userfolder!='C' and userfolder!='A':
                userfolder=""
        except:
            userfolder=""
        return render_to_response("folder_listing.html",{'userfolder':userfolder,'folder':p,'entries':e,'more':(e.count()<p.folderentry_set.count())*20})
    except:
        return HttpResponseNotFound("")

@login_required
def list_group(request,group_id):
    #try:
        g=Group.objects.get(id=group_id)
        rights=""
        try:
            rights=Membership.objects.get(group=g,user=request.user).rights
        except:
            rights="N"
        return render_to_response("group_users.html",{"groups":request.user.group_set.all(),"group":g,"rights":rights})
    #except:
    #    return HttpResponseNotFound()

@login_required
def create_group(request):
    title=request.POST["title"]
    g=Group(title=title)
    g.save()
    m=Membership(user=request.user,group=g,rights='C')
    m.save()
    return list_group(request,g.id)

@login_required
def list_group_topic(request,group_id,topic_id):
    try:
        topic=GroupTopic.objects.get(id=topic_id)
        rights=""
        try:
            rights=Membership.objects.get(group=topic.group,user=request.user).rights
        except:
            rights="N"
        return render_to_response("group_topic_listing.html",{'topic':topic,'rights':rights})
    except:
        return HttpResponseNotFound()

@login_required
def list_topic(request,id):
    try:
        topic=Topic.objects.get(id=id)
        return render_to_response("topic_listing.html",{'topic':topic})
    except:
        return HttpResponseNotFound()

@login_required
def delete_entry(request):
    if request.method=='POST':
        try:
            folder=request.POST["folder_id"]
            entry=request.POST["entry_id"]
            if (folder!="-1"):
                FolderEntry.objects.filter(folder__id=folder,entry__id=entry).delete();
            else:
                Favor.objects.filter(entry__id=entry,user=request.user).delete();
            return HttpResponse("Ok")
        except:
            return HttpResponseServerError("Error")
    else:
        return HttpResponseServerError("Error")

@login_required
def add_comment(request):
    if request.method=='POST':
        text=request.POST["text"]
        topic=request.POST["topic"]
        new=Comment(topic=Topic.objects.get(id=topic),text=text,author=request.user,created=datetime.now(),carma=0)
        new.save()
        return HttpResponse("Ok")
    else:
        return HttpResponseServerError("Bad request.")

@login_required
def my_profile(request):
    return render_to_response("profile.html",{"victim":request.user,"user":request.user})

@login_required
def save_profile(request):
    if request.method=='POST':
        login=request.POST["id_username"]
        first=request.POST["id_first_name"]
        last=request.POST["id_last_name"]
        user=auth.User.objects.get(id=request.user.id)
        user.first_name=first
        user.last_name=last
        user.username=login
        user.save()
        return HttpResponseRedirect("/profile")

@login_required
def user_profile(request,user_id):
    user=0
    try:
        user=auth.User.objects.get(id=user_id)
    except:
        return HttpResponseNotFound("No such user")
    return render_to_response("profile.html",{"victim":user,"user":request.user})

@login_required
def list_group_user(request,group_id,user_id):
    try:
        user=auth.User.objects.get(id=user_id)
        group=Group.objects.get(id=group_id)
        comments_count=Comment.objects.filter(author=user).count()
        topics_count=GroupTopic.objects.filter(group=group,starter=user).count()
        folders_count=group.folders.filter(userfolder__user=user).count()
        rights=""
        try:
            rights=Membership.objects.get(group=group,user=request.user).rights
        except:
            rights="N"
        hisrights=""
        try:
            hisrights=Membership.objects.get(group=group,user=user).rights
        except:
            hisrights="N"
        return render_to_response("group_user.html",{"groups":request.user.group_set.all(),"user":user,"group":group,"comments":comments_count,"topics":topics_count,"folders":folders_count,"rights":rights,"hisrights":hisrights})
    except:
        return HttpResponseNotFound()

@login_required
def grant_group_user_rights(request,group_id,user_id,new_rights):
    try:
        user=auth.User.objects.get(id=user_id)
        group=Group.objects.get(id=group_id)
        rights=""
        try:
            rights=Membership.objects.get(group=group,user=request.user).rights
        except:
            rights="N"
        his_rights=""
        M=0
        try:
            M=Membership.objects.get(group=group,user=user)
            his_rights=M.rights
        except:
            his_rights="N"
        if ( rights=='C' or (rights=='A' and (new_rights=='M' or (his_rights=='M' and new_rights=='R')))):
            M.rights=new_rights
            M.save()
        return list_group_user(request,group_id,user_id)
    except:
        return HttpResponseNotFound()

@login_required
def start_group_topic(request):
    if request.method=='POST':
        title=request.POST["title"]
        group_id=request.POST["group_id"]
        new=GroupTopic.objects.create(title=title,starter=request.user,started=datetime.now(),group=Group.objects.get(id=group_id),last_post=datetime.now())
        return list_group_topic(request,new.topic_ptr.id)
    else:
        return HttpResponseServerError("Bad request.")

@login_required
def list_group_folders(request,groupid):
    rights=""
    try:
        rights=Membership.objects.get(group=groupid,user=request.user).rights
    except:
        rights="N"
    return render_to_response('group_folders.html', {"groups":request.user.group_set.all(),
    'group':Group.objects.get(id=groupid),'rights':rights,'user':request.user
    })

@login_required
def list_group_users(request,groupid):
    rights=""
    try:
        rights=Membership.objects.get(group=groupid,user=request.user).rights
    except:
        rights="N"
    return render_to_response('group_users.html', {"groups":request.user.group_set.all(),
    'group':Group.objects.get(id=groupid),'rights':rights,'user':request.user
    })

@login_required
def list_group_topics(request,groupid):
    rights=""
    try:
        rights=Membership.objects.get(group=groupid,user=request.user).rights
    except:
        rights="N"
    return render_to_response('group_topics.html', {"groups":request.user.group_set.all(),
    'group':Group.objects.get(id=groupid),'rights':rights,'user':request.user
    })

@login_required
def list_groups(request):
    return render_to_response("groups.html",{"groups":request.user.group_set.all(),"user":request.user})

@login_required
def search(request,find_what):
    if find_what=="":
        return render_to_response("search.html",{})
    else:
        return render_to_response("search.html",
        {
        "find_what":find_what,
        "groups":Group.objects.filter(title__contains=find_what),
        "folders":Folder.objects.filter(title__contains=find_what)
        }
        )

@login_required
def find_feed(request):
    if request.method=='GET':
        url=request.GET["url"]
        url=feedfinder.feed(url)
        return HttpResponse(url)
    else:
        return HttpResponseServerError("Bad request.")

@login_required
def suggest_feed(request):
    if request.method=='POST':
        control_id=request.POST['control_id']
        div_id=request.POST['div_id']
        first_chars=request.POST['first_chars']
        L=map(lambda x:x.url,Feed.objects.filter(url__startswith=first_chars)[:5])
        return render_to_response("suggest_widget.html",{"L":L,"control_id":control_id,"div_id":div_id})
    else:
        return "Error"

def index(request):
    return render_to_response('news.html',{
    'news':News.objects.all()[:15],
    'user':request.user
    })

@login_required
def clean_folder(request):
    if request.method=='POST':
        try:
            id=request.POST['id']
            if ((UserFolder.objects.filter(folder__id=id,user=request.user)[0]).relation=='C'):
                FolderEntry.objects.filter(folder__id=id).delete()
            return list_folder_entries(request,id)
        except:
            return HttpResponseNotFound("")
    else:
        return HttpResponseServerError("Bad request.")

@login_required
def purge_folder(request):
    if request.method=='POST':
        try:
            id=request.POST['id']
            if (UserFolder.objects.filter(folder__id=id,user=request.user)[0].relation=='C'):
                Folder.objects.filter(id=id).delete()
            return HttpResponse("Ok")
        except:
            return HttpResponseNotFound("")
    else:
        return HttpResponseServerError("Bad request.")

@login_required
def create_folder(request):
    if request.method=='POST':
        title=request.POST['title']
        p=Folder(title=title)
        p.save()
        group_id=-1
        try:
            group_id=request.POST["group_id"]
            group=Group.objects.get(id=group_id)
            group.folders.add(p)
            group.save()
        except:
            up=UserFolder(user=request.user,folder=p,relation='C')
            up.save()
        return list_folder_entries(request,p.id)
    else:
        return HttpResponseServerError("Bad request.")

def full_folder(p):
    for q in FeedFilterPair.objects.filter(folder=p):
        #q.feed.Check()# THIS FUCKING MADNESS MUST BE DELETED IN PRODUCTION!!!!!!!!!!!!!!!
        for e in Entry.objects.filter(feed=q.feed,downloaded__gt=q.last_cheked).exclude(folderentry__folder=p):
            flag1=True
            flag2=False
            flag2on=False
            flag3=True
            for f in Filter.objects.filter(pair=q):
                if (f.type==1 and e.summary.count(f.value)==0):
                    flag1=False
                elif (f.type==2 and e.summary.count(f.value)==0):
                    flag2on=True
                elif (f.type==2):
                    flag2on=True
                    flag2=True
                elif (f.type==3 and e.summary.count(f.value)!=0):
                    flag3=False
            if (flag3 and flag1 and (flag2 or (flag2==flag2on))):
                ep=FolderEntry(folder=p,entry=e)
                ep.save()
        q.last_cheked=datetime.now()
        q.save()

def list_folder_entries(request,folder_id):
    try:
      p=Folder.objects.get(id=folder_id)
      print p
      full_folder(p)
      e=p.folderentry_set.all()[0:20]
      print e
      userfolder=None
      try:
        userfolder=UserFolder.objects.get(user=request.user,folder=p)
      except:
        pass
      if request.method=="POST":
        return render_to_response("folder_listing.html",{'userfolder':userfolder,'folder':p,'entries':e,'more':(e.count()<p.folderentry_set.count())*20})
      else:
        P=Folder.objects.filter(Q(userfolder__user=request.user))#|Q(group__members=request.user))
        return render_to_response("folder_direct.html",{'userfolder':userfolder,'folder':p,'folders':P,'entries':e,'more':(e.count()<p.folderentry_set.count())*20})
    except:
      return HttpResponseNotFound("")

def more_folder_entries(request,folder_id,next):
    next=int(next)
    p=Folder.objects.get(id=folder_id)
    e=p.folderentry_set.all()[next:next+20]
    return render_to_response("one_entry.html",{'folder':p,'entries':e,'more':(next+e.count()<p.folderentry_set.count())*(next+20)})

def list_folders(request,user_id):
    if user_id:
        try:
            user=auth.User.objects.get(id=user_id)
            P=Folder.objects.filter(Q(userfolder__user=user))#|Q(group__members=request.user))
            return render_to_response('folders.html', {
            'feedform':FeedForm(),'folders':P,'user':request.user,'owner':user
            })
        except:
            return HttpResponseNotFound("")
    else:
        return list_user_folders(request)

@login_required
def list_user_folders(request):
    P=Folder.objects.filter(Q(userfolder__user=request.user))#|Q(group__members=request.user))
    print P
    #for p in P:
    #    full_folder(p)
    #F=None
    return render_to_response('folders.html', {
    'feedform':FeedForm(),'folders':P,'user':request.user,'owner':request.user
    })

def list_favorites(request,user_id):
    if user_id:
        try:
            user=auth.User.objects.get(id=user_id)
            P=Folder.objects.filter(Q(userfolder__user=user))#|Q(group__members=request.user))
            f=Favor.objects.filter(user=user)
            return render_to_response("favorites.html",{"favors":f,"folders":P,'owner':user,'user':request.user})
        except:
            return HttpResponseNotFound("")
    else:
        return list_user_favorites(request)

@login_required
def list_user_favorites(request):
    P=Folder.objects.filter(Q(userfolder__user=request.user))#|Q(group__members=request.user))
    f=Favor.objects.filter(user=request.user)
    return render_to_response("favorites.html",{"favors":f,"folders":P,'owner':request.user,'user':request.user})

@login_required
def favorite_entry(request):
    if request.method=="POST":
        try:
            e=request.POST["entry_id"]
            if Favor.objects.filter(entry__id=e,user=request.user).count()==0:
                f=Favor(user=request.user,entry=Entry.objects.get(id=e))
                f.save()
                return HttpResponse("Ok")
            else:
                return HttpResponseServerError("Allready favored!")
        except:
            return HttpResponseServerError("Bad request.")
    else:
        return HttpResponseServerError("Bad request.")

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")