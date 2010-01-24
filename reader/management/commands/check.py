from django.core.management.base import NoArgsCommand
from django.conf import settings
from reader.models import Feed
import threading
import time


class CheckThread(threading.Thread):
    def run(self):
        while 1:
            print self.getName(),self.id_list
            for x in self.id_list:
                Feed.objects.get(id=x).Check()
            time.sleep(300)

class Command(NoArgsCommand):
    help = 'Checks updates on all feeds in db'
    feeds_in_thread=2
    def handle_noargs(self, **options):
        while 1:
            print "Running threads"
            self.cycle()
            #print "Done. Sleeping"
            #time.sleep(60)
    
    def cycle(self):
        threads=[]
        feeds=Feed.objects.all()
        c=feeds.count()
        alive_threads=c/self.feeds_in_thread+1
        maxid=0
        for i in xrange(0,alive_threads):
            t=CheckThread()
            t.id_list=[]
            for j in xrange(0,self.feeds_in_thread):
                if i*self.feeds_in_thread+j<c:
                    maxid=max(maxid,feeds[i*self.feeds_in_thread+j].id)
                    t.id_list.append(feeds[i*self.feeds_in_thread+j].id)
            t.setName("Thread"+str(i))
            threads.append(t)
            threads[-1].start()
        del feeds
        while 1:
            f=Feed.objects.filter(id__gt=maxid)
            if f.count():
                for q in f:
                    maxid=max(maxid,q.id)
                    if len(threads[-1].id_list)>=self.feeds_in_thread:
                        threads.append(CheckThread())
                        threads[-1].id_list=[q.id]
                        threads[-1].start()
                    else:
                        threads[-1].id_list.append(q.id)
            time.sleep(1)