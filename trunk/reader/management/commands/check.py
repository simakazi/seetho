from django.core.management.base import NoArgsCommand
from django.conf import settings
from reader.models import Feed

class Command(NoArgsCommand):
    help = 'Checks updates on all feeds in db'
    
    def handle_noargs(self, **options):
        print "Checking..."
        f=Feed.objects.all()[0]
        c=f.id
        while 1:
            f.Check()
            f=Feed.objects.all()[0]
            if f.id==c:
                return