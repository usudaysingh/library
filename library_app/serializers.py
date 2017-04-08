from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.utils import timezone 

from .models import Books, Status, BookStatus, AppUser

class BookStatusSerializer(serializers.Serializer):
	by = serializers.CharField()
	at = serializers.DateTimeField(default=timezone.now)
	status =  serializers.CharField()
	reader =  serializers.CharField()
	status_code = serializers.CharField()

	def validate_status_code(self,value):
		status = Status.objects.filter(code=value)
		if not status:
			msg = 'Please enter correct status code'
			raise serializers.ValidationError(msg)
		else:
			return value


class CreateBookSerializer(serializers.Serializer):
	book_name = serializers.CharField(max_length=500, required=True)
	author = serializers.CharField(max_length=500, required=True)
	publisher = serializers.CharField(max_length=500, required=True)
	publishing_year = serializers.IntegerField(required=True)
	# status_history = serializers.ListField(child=serializers.CharField())
	# status_code = serializers.CharField(max_length=10,required=True)

	# class Meta:
	# 	# Each room only has one event per day.
	# 	validators = [UniqueTogetherValidator(
	# 	    queryset=Books.objects.all(),
	# 	    fields=['book_name', 'author_name']
	# 	)]

	def validate_status_code(self,value):
		status = Status.objects.filter(code=value)
		if not status:
			msg = 'Please enter correct status code'
			raise serializers.ValidationError(msg)
		else:
			return value


	def validate_publishing_year(self,value):
		if value < timezone.now().year:
			return value
		else:
			msg= 'Please enter correct publication year'
			raise serializers.ValidationError(msg)

	def create(self, validated_data):
		validated_data['available'] = True
		add_status = {
			'by':'uday',
			'at':timezone.now(),
			'status':'Added in library',
			'status_code':'ADD',
			'reader':'dolly'
		}
		# validated_data['added_in_library']=timezone.now()
		validated_data['available'] = True
		book_instance = Books(**validated_data)
		book_instance.status.status_history.append(BookStatus(**add_status))
		book_instance.status.latest_status = BookStatus(**add_status)
		book_instance.save()
		return book_instance
		

class GetBookListSerializer(serializers.Serializer):
	book_name = serializers.CharField(max_length=500)
	book_id = serializers.CharField()
	author = serializers.CharField(max_length=500)
	publisher = serializers.CharField()
	available = serializers.BooleanField()
	# status_history = BookStatusSerializer(many=True)
	added_in_library = serializers.DateTimeField()
	modified = serializers.DateTimeField()

	def __init__(self, *args, **kwargs):
		show_fields = kwargs.pop('show_fields', None)
		super(GetBookListSerializer, self).__init__(*args, **kwargs)

		if show_fields:
		    # for multiple fields in a list
		    show_fields.append('book_name')
		    all_fields = set(self.fields.keys())
		    remove_fields = all_fields - set(show_fields)
		    remove_fields = list(remove_fields)
		    for field_name in remove_fields:
		        self.fields.pop(field_name)

class LogBookStatusSerializer(serializers.Serializer):
	status_history = BookStatusSerializer(many=True)
	latest_status = BookStatusSerializer()

class RetrieveBookSerializer(serializers.Serializer):
	book_name = serializers.CharField(max_length=500)
	book_id = serializers.CharField()
	author = serializers.CharField(max_length=500)
	publisher = serializers.CharField()
	available = serializers.BooleanField()
	status = LogBookStatusSerializer()
	added_in_library = serializers.DateTimeField()
	modified = serializers.DateTimeField()
	publishing_year = serializers.CharField()
	fine_amount = serializers.IntegerField()

class UpdateBookSerializer(serializers.Serializer):
	book_name = serializers.CharField(max_length=500)
	author = serializers.CharField(max_length=500)
	publisher = serializers.CharField()
	publishing_year = serializers.IntegerField()
	# status_code = serializers.CharField()

	# def validate_status_code(self, value):
	# 	status = Status.objects.filter(code=value)
	# 	if not status:
	# 		msg = 'Please enter correct status code'
	# 		raise serializers.ValidationError(msg)
	# 	else:
	# 		return value

	def validate_publishing_year(self,value):
		print value
		print timezone.now().year
		if value < timezone.now().year:
			return value
		else:
			msg= 'Please enter correct publication year'
			raise serializers.ValidationError(msg)

class UserSerializer(serializers.Serializer):
	username = serializers.CharField()
	email = serializers.CharField()
	first_name = serializers.CharField()
	last_name = serializers.CharField()
	is_active = serializers.BooleanField(default=True)
	user_type = serializers.CharField(default='ST')
	password = serializers.CharField()
	confirm_password = serializers.CharField()

	def validate(self, data):
		if data['password'] == data['confirm_password']:
			return data
		else:
			raise serializers.ValidationError("Those passwords don't match.")

	def save(self, validated_data):
		password = validated_data.pop('password')
		confirm_password = validated_data.pop('confirm_password')
		student = AppUser(**validated_data)
		student.set_password(password)
		student.save()
		return student

class LoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()
