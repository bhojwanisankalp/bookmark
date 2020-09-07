from django.db import models

class Customer(models.Model):
	"""
		Customers Model Fields
	"""
	first_name = models.CharField(max_length=50, null=True)
	last_name = models.CharField(max_length=50, null=True)
	dob = models.DateField(null=True)
	email = models.EmailField(max_length=254,  null= True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, default= 0)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, default= 0)
	created_at  = models.DateTimeField(auto_now_add = True, null = True)
	updated_at = models.DateTimeField(auto_now = True, null = True)


	def __str__(self):
		""" String representation of Model Instance """
		return self.first_name +' '+self.last_name

	def get_book_marks(self):
		""" To get associated Bookmark model instances. """
		bookmark_ids = CustomerBookmark.objects.filter(customer = self).values_list('bookmark_id', flat = True)
		return Bookmark.objects.filter(pk__in = bookmark_ids)

class Bookmark(models.Model):
	"""
		Bookmarks Model Fields
	"""
	customer = models.ForeignKey(Customer, on_delete = models.CASCADE,null= True)
	title = models.CharField(max_length=255, null=True)
	url = models.URLField(max_length=2048, null = True)
	source_name = models.CharField(max_length =100, null=True) 
	created_at  = models.DateTimeField(auto_now_add = True, null = True)
	updated_at = models.DateTimeField(auto_now = True, null = True)

	def __str__(self):
		""" String representation of Model Instance """
		return self.title


class CustomerBookmark(models.Model):
	"""Model for relation between Bookmark and Customer"""
	customer = models.ForeignKey(Customer, on_delete = models.CASCADE, null = False)
	bookmark = models.ForeignKey(Bookmark, on_delete = models.CASCADE, null = False)
		

		
