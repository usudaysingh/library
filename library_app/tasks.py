import datetime
from celery.decorators import periodic_task

from .models import Books

@periodic_task(run_every=datetime.timedelta(seconds=1))
def update_fine():
	books = Books.objects.all()
	for book in books:
		book.fine_amount = 90
		book.save()