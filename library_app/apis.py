import json
import requests

from django.contrib.auth.models import User, Group
from django.utils import timezone 
from rest_framework import viewsets
from .models import Books, BookStatus, BooksFlow, AppUser #, Author, Publisher
from .serializers import GetBookListSerializer,  CreateBookSerializer, RetrieveBookSerializer, UpdateBookSerializer,\
	BookStatusSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import permissions
from django_fsm import can_proceed
from django.core.exceptions import PermissionDenied

class UserPermission(permissions.BasePermission):
    """
   Check Permission before performing operation
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            if view.action == 'list' or view.action == 'retrieve':
                return True
            else:
                return False
        elif request.user.is_authenticated() and request.user.user_type == 'MNGR':
        	return True
        else:
            if view.action == 'list' or view.action == 'retrieve':
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
				request_data = serializer.data
				data_keys = request_data.keys()
				book = book[0]
				for i in data_keys:
					book[i] = request_data[i]
				book.save()
				return Response(serializer.data)
		else:
			error = {
				'error' :'Book does not exist please enter correct book id.'
			}
			return Response(error)
		return Response(serializer.errors)

class UpdateBookStatus(viewsets.ModelViewSet):
	serializer_class = BookStatusSerializer
	model = Books
	permission_classes = (UserPermission,)

	def update(self,request,*args,**kwargs):
		book_id = kwargs.get('book_id')
		try:
			book = self.model.objects.get(book_id=book_id)
			serializer = self.get_serializer(data=request.data)
			if serializer.is_valid():
				flow = BooksFlow.objects.get_or_create(book_id=book_id,name=book.book_name)
				flow = flow[0]
				# To check for issue
				if not can_proceed(flow.issue):
					error = {
						'error':'TransitionNotAllowed:'
					}
					return Response(error)
				flow.issue()
				flow.save()

				data = serializer.data
				data['at'] = timezone.now
				if data['status_code'] in ['ISU','RMV','RSU']:
					book.available = False
				else:
					book.available = True
				book.status_history.append(BookStatus(**data))
				book.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors)
		except Exception as ObjectDoesNotExist:
			error = {
				'error' :'Book does not exist please enter correct book id.'
			}
			return Response(error)

class CreateNewUser(viewsets.ModelViewSet):
	serializer_class = UserSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data = request.data)
		if serializer.is_valid():
			serialize_data = serializer.data
			user_instance = serializer.save(serializer.data)
			success = {
			'success':'User created successfully',
			'username':request.data['username']
			}
			return Response(success)
		else:
			return Response(serializer.errors)