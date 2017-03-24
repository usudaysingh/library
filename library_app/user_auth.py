import json
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from django.core import serializers
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import login, logout, authenticate
 

class AuthView(viewsets.ModelViewSet):

	serializer_class = LoginSerializer

	def login(self, request, *args, **kwargs):
		username = request.data['username']
		password = request.data['password']
		user = authenticate(username=username, password=password)
		login(request, user)
		data = {
			'token':serializers.serialize("json", [user.auth_token])
		}
		return Response(data)

	def loginview(self,request, *args, **kwargs):
		if request.user.is_authenticated():
			data = {
				'success':request.user.username + ' is already logged in.'
			}
		else:
			data = {
				'message':'Please login.'
			}

		return Response(data)


	def logout(self, request, *args, **kwargs):
	    logout(request)
	    return Response({'success':'loggedout'})


class CreateNewUser(viewsets.ModelViewSet):
	'''
	To register new user
	'''
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

