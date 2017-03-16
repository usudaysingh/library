from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.utils import timezone 

from .models import Books, Status, BookStatus

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
		status = {
			'by':'uday',
			'at':timezone.now(),
			'status':'Added in library',
			'status_code':validated_data['status_code'],
			'reader':'dolly'
		}
		validated_data['added_in_library']=timezone.now()
		book_instance = Books(**validated_data)
		book_instance.status_history.append(BookStatus(**status))
		book_instance.save()
		return book_instance
		

class GetBookListSerializer(serializers.Serializer):
	book_name = serializers.CharField(max_length=500)
	book_id = serializers.CharField()
	author = serializers.CharField(max_length=500)
	publisher = serializers.CharField()
	available = serializers.BooleanField()
	#status_history = BookStatusSerializer(many=True)
	added_in_library = serializers.DateTimeField()
	modified = serializers.DateTimeField()

	def __init__(self, *args, **kwargs):
		show_fields = kwargs.pop('show_fields', None)
		super(GetBookListSerializer, self).__init__(*args, **kwargs)

		if show_fields:
		    # for multiple fields in a list
		    all_fields = set(self.fields.keys())
		    remove_fields = all_fields - set(show_fields)
		    remove_fields = list(remove_fields)
		    for field_name in remove_fields:
		        self.fields.pop(field_name)

class RetrieveBookSerializer(serializers.Serializer):
	book_name = serializers.CharField(max_length=500)
	book_id = serializers.CharField()
	author = serializers.CharField(max_length=500)
	publisher = serializers.CharField()
	available = serializers.BooleanField()
	status_history = BookStatusSerializer(many=True)
	added_in_library = serializers.DateTimeField()
	modified = serializers.DateTimeField()
	publishing_year = serializers.CharField()

class UpdateBookSerializer(serializers.Serializer):
	book_name = serializers.CharField(max_length=500)
	author = serializers.CharField(max_length=500)
	publisher = serializers.CharField()
	publishing_year = serializers.IntegerField()
	# status_code = serializers.CharField()

	def validate_status_code(self, value):
		status = Status.objects.filter(code=value)
		if not status:
			msg = 'Please enter correct status code'
			raise serializers.ValidationError(msg)
		else:
			return value

	def validate_publishing_year(self,value):
		print value
		print timezone.now().year
		if value < timezone.now().year:
			return value
		else:
			msg= 'Please enter correct publication year'
			raise serializers.ValidationError(msg)