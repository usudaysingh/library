import json
import requests

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .models import Books #, Author, Publisher
from .serializers import GetBookListSerializer,  CreateBookSerializer, RetrieveBookSerializer, UpdateBookSerializer
from rest_framework.response import Response
from rest_framework import permissions

class UserPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            if view.action == 'list' or view.action == 'retrieve':
                return True
            else:
                return False
        else:
            return True

class BookViewset(viewsets.ModelViewSet):
	'''
		Book operations
	'''
	model = Books
	serializer_class = GetBookListSerializer
	permission_classes = (UserPermission,)

	def get_serializer_class(self):
		serializer_action_classes = {
		    'create': CreateBookSerializer,
		    'list': GetBookListSerializer,
		}
		if hasattr(self, 'action'):
		    return serializer_action_classes.get(self.action, self.serializer_class)
		return self.serializer_class

	def get_queryset(self):
		queryset = self.model.objects.all()
		keys = self.request.query_params.keys()
		if keys:
			if 'available' in keys:
				value = self.request.query_params.get('available')
				if value == 'true':
					queryset = queryset.filter(available=True)
				else:
					queryset = queryset.filter(available=False)
		return queryset

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			book_instance = serializer.create(serializer.data)
			return Response(GetBookListSerializer(book_instance).data)
		return Response(serializer.errors)

	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		fields = self.request.query_params.get('fields')
		if fields:
			fields = fields.split(',')
			serialize = self.get_serializer(queryset, show_fields=fields, many=True)
		else:
			serialize = self.get_serializer(queryset, many=True)
		return Response(serialize.data)


class UpdateRetrieveBook(viewsets.ModelViewSet):
	'''
		Retrieve and update book
	'''

	model = Books
	serializer_class = RetrieveBookSerializer
	permission_classes = (UserPermission,)

	def get_serializer_class(self):
		serializer_action_classes = {
		    'retrieve': RetrieveBookSerializer,
		    'update': UpdateBookSerializer,
		}
		if hasattr(self, 'action'):
		    return serializer_action_classes.get(self.action, self.serializer_class)
		return self.serializer_class


	def retrieve(self, request, *args, **kwargs):
		book_id = kwargs.get('book_id')
		try:
			data = self.model.objects.get(book_id=book_id)
			serializer = self.get_serializer(data)
			return Response(serializer.data)
		except Exception as ObjectDoesNotExist:
			error = {
				'error' :'Book does not exist please enter correct book id.'
			}
			return Response(error)

	def update(self, request, *args, **kwargs):
		book_id = kwargs.get('book_id')
		book = self.model.objects.filter(book_id=book_id)
		if book:
			serializer = self.get_serializer(data = request.data)
			if serializer.is_valid():
				data = {
				'goood':'goingggg'
				}
		else:
			error = {
				'error' :'Book does not exist please enter correct book id.'
			}
			return Response(error)
		return Response(serializer.errors)