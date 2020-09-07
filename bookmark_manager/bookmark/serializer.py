from .models import *
from rest_framework import serializers, fields


class BookmarkSerializers(serializers.ModelSerializer):
	"""
		Bookmark serializer to create bookmark records.
		URLS for available customer should be unique to avoid bookmark duplicacy.

	"""

	class Meta:
		model = Bookmark
		fields = ('title', 'url', 'source_name', 'customer')

	def validate(self, data):
		""" Custom validation to check duplicate urls for given customer """
		customer = data['customer']
		url = data['url']
		bookmarks = CustomerBookmark.objects.filter(customer= customer).values_list('bookmark_id', flat=True)
		is_exist = Bookmark.objects.filter(id__in = bookmarks, url=url).exists()
		if is_exist:
			raise serializers.ValidationError("BookMark with same url already exists for the Customer")
		return data

	def validate_url(self, url):
		""" Custom validation to check if url is None or empty """
		if not url:
			raise serializers.ValidationError("url is required")
		return url

	def create(self, validated_data):
		""" Override create method to create Boookmark entry as well as CustomerBookmark association."""
		customer = validated_data['customer']
		bookmark = Bookmark.objects.create(**validated_data)
		CustomerBookmark.objects.create(customer = customer, bookmark = bookmark)
		return bookmark

class BookmarkListSerializers(serializers.ModelSerializer):
	""" Bookmark serializer to get list of bookmarks """
	created_at =  serializers.DateTimeField(format="%Y-%m-%d")
	class Meta:
		model = Bookmark
		exclude = ['updated_at', 'id']

		


class CustomerSerializers(serializers.ModelSerializer):
	"""
		Customer model serializer.

	"""
	#To get Bookmark records of the associated customer.
	bookmarks = BookmarkListSerializers(source= "get_book_marks", read_only=True, many=True)
	
	class Meta:
		model = Customer
		fields = ('id','first_name','last_name', 'dob', 'email', 'latitude', 'longitude', 'bookmarks')