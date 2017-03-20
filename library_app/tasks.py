import datetime
from celery.decorators import periodic_task

from .models import Books

@periodic_task(run_every=datetime.timedelta(seconds=1))
def update_fine():
	print "yahooo main to hu pagal"