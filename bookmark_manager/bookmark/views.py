from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from django.db.models import Q, F
from django.db.models.functions import Power, Sin, Cos, ATan2, Sqrt, Radians
from .models import *
from datetime import datetime, timedelta


@api_view(['GET','POST'])
def create(request):
	"""
		To create Bookmark for given customer 
		else get list of customers with available bookmark
		@return Response with success msg and status code 200 for method type POST.
		else Customer objects list with Customer associasted Bookmarks for method type GET.
	"""
	#Create bookmark if request method type is POST
	if request.method == 'POST':
		serializer = BookmarkSerializers(data = request.data)
		
		if serializer.is_valid():
			bookmark = serializer.save()

			return Response('Book mark saved successfull', status = status.HTTP_200_OK)
		
		else:
			
			return Response(serializer.errors, status = status.HTTP_409_CONFLICT)
	
	#Get Customer list with associated Bookmarks for request type GET
	elif request.method == 'GET':
		customers = Customer.objects.all()
		serializer = CustomerSerializers(customers, many=True)
		
		return Response(serializer.data)



@api_view(['GET'])
def browse(request):
	"""
		To browse Bookmarks objects for given params and sorting order. 
		@return Response of bookmarks objects list.
	"""
	params = request.query_params

	sort_by = params.get('sort_by', None)
	
	#Default sorting order
	if not sort_by:
		sort_by = 'customer_id'
	
	#Customer
	customer_id = params.get('customer_id', None)
	q_customer = Q()
	if customer_id:
		#Query Expression to get Bookmarks according to customer id.
		q_customer = Q(customer_id = customer_id)

	#Source name
	source_name = params.get('source_name', None)
	q_source_name = Q()
	if source_name:
		#Query Expression to get Bookmarks according to source name.
		q_source_name = Q(source_name__icontains = source_name)

	#Title
	title = params.get('title', None)
	q_title = Q()
	if title:
		#Query Expression to get Bookmarks according to title.
		q_title = Q(title__icontains = title)
	
	#Geo Location
	current_lat = params.get('lat', None)
	current_long = params.get('long', None)
	radius = params.get('radius', None)
	q_location = Q()
	if all(v is not None for v in [current_long, current_lat, radius]):
		"""
			Implementation of haversine formula 
			to get customers whose geoloactions lies within the given radius
			taking the request param points as center location.
			a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
			c = 2 ⋅ atan2( √a, √(1−a) )
			d = 6371 #Earth radius
		"""
		current_lat = float(current_lat)
		current_long = float(current_long)
		dlat = Radians(F('latitude') - current_lat)
		dlong = Radians(F('longitude') - current_long)

		a = (Power(Sin(dlat/2), 2) + Cos(Radians(current_lat)) * Cos(Radians(F('latitude'))) * Power(Sin(dlong/2), 2))

		c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
		d = 6371 * c
		customers = Customer.objects.filter()\
					.annotate(distance=d)\
					.filter(distance__lt=radius)
		#Query expression for all customers lies within the radius to filter Bookmark model.
		q_location = Q(customer__in= customers)

	#Date Range
	start_date = params.get('start_date', None)
	end_date = params.get('end_date', None)
	q_date_range = Q()
	if start_date is not None and end_date is not None:
		start_date = datetime.strptime(start_date, "%Y-%m-%d")
		end_date = datetime.strptime(end_date, "%Y-%m-%d")
		end_date = end_date + timedelta(days = 1)
		#Query Expression to get Bookmarks according to customer id.
		q_date_range = Q(created_at__range = (start_date, end_date))
	
	#Filter and sort Bookmark model for the given query params.
	bookmarks = Bookmark.objects.filter(q_customer | q_source_name | q_title | q_date_range | q_location).order_by(sort_by)

	#Bookmark serializer
	serializer = BookmarkListSerializers(bookmarks, many = True)
	return Response(serializer.data)