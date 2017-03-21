from django.utils import timezone 

from django.db import models
from django_fsm import FSMField, transition

import requests
import os
import mongoengine
import json

from django.contrib.auth.models import AbstractUser

current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, 'transition_status.json')

with open(filename) as f:
    TRANSITION_MAP = json.loads(f.read())

# Create your models here.

class AppUser(AbstractUser):
	type_choices = (
		('MNGR', 'Manager'),
		('AST', 'Assistant'),
		('ST','Student'),
	)
	user_type = models.CharField(max_length=500, choices=type_choices)

	def save(self, *args, **kwargs):
		if self.is_superuser:
			self.user_type = 'MNGR'
		super(AppUser, self).save(*args, **kwargs)

# class Books(models.Model):
# 	book_name = models.CharField(max_length=500)
# 	book_id = models.CharField(max_length=500)
# 	author_name = models.CharField(max_length=500)
# 	added = models.DateTimeField(default=timezone.now)
# 	modified = models.DateTimeField(default=timezone.now)
# 	available = models.BooleanField(default=True)
# 	status_history = 

# 	To perform operation on model end before creating or saving object
# 	def save(self, *args, **kwargs):
# 		super(Books, self).save(*args, **kwargs)

class BooksFlow(models.Model):
	book_id = models.IntegerField(default='1')
	name = models.CharField(max_length=100)
	status = FSMField(default='ADD', protected=True)

	@transition(field=status, source=TRANSITION_MAP.get('ISU'), target='ISU')
	def issue(self):
		pass

	@transition(field=status, source=TRANSITION_MAP.get('RSU'), target='RSU')
	def reissue(self):
		pass

	@transition(field=status, source=TRANSITION_MAP.get('RMV'), target='RMV')
	def remove(self):
		pass

	@transition(field=status, source=TRANSITION_MAP.get('RTN'), target='RTN')
	def returned(self):
		pass

class Status(models.Model):
	code = models.CharField(max_length=10)
	name = models.CharField(max_length=50)

class BookStatus(mongoengine.EmbeddedDocument):
	by = mongoengine.StringField()
	at = mongoengine.DateTimeField(default=timezone.now)
	status = mongoengine.StringField()
	status_code = mongoengine.StringField()
	reader = mongoengine.StringField(blank=True)

class StatusLog(mongoengine.EmbeddedDocument):
	status_history = mongoengine.ListField(mongoengine.EmbeddedDocumentField(BookStatus))
	latest_status = mongoengine.EmbeddedDocumentField(BookStatus)

class Books(mongoengine.DynamicDocument):
	book_name = mongoengine.StringField()
	book_id = mongoengine.SequenceField()
	author = mongoengine.StringField()
	available = mongoengine.BooleanField()
	added_in_library = mongoengine.DateTimeField()
	modified = mongoengine.DateTimeField()
	publisher = mongoengine.StringField()
	publishing_year = mongoengine.IntField()
	fine_amount = mongoengine.IntField(default=0)
	status = mongoengine.EmbeddedDocumentField(StatusLog, default=StatusLog())
	# status_history = mongoengine.ListField(mongoengine.EmbeddedDocumentField(BookStatus))

	def save(self, *args, **kwargs):
		if not self.added_in_library:
			self.added_in_library = timezone.now()
		self.modified = timezone.now()
		super(Books, self).save(*args, **kwargs)

class Author(mongoengine.DynamicDocument):
	author_name = mongoengine.StringField()
	author_id = mongoengine.SequenceField()
	books = mongoengine.ListField()

class Publisher(models.Model):
	publisher_name = models.CharField(max_length=500)
	publisher_id = models.IntegerField()
	# authors = models.ManyToManyField(Author)
	# books = models.ManyToManyField(Books)