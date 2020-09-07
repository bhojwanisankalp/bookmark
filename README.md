# BOOKMARK MANAGER

CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Installation
 * Create Customers
 * API end points
 
 
 INTRODUCTION
------------


The bookmark manager is a web-based application build on Python-based web frame Django, to manage Customer's bookmarks.
This application provides REST APIs for the creation and browsing of Bookmarks.

 INSTALLATION
------------
The application is easy to install. The user needs to have python version 3 or greater, 
pip package installer. Using a virtual environment is recommended. The application is configured to use the SQLite database which comes with a new Django project setup and also available with this application. 

The following steps to setup are.
* Clone this repo 
* Create virtual environment
* Get to the project directory using 'cd' where 'requirements.txt' exist.
* Install all required packages using  'pip install -r requirements.txt'
* Check the application setup by 'python manage.py check'.
* Makemigrations using 'python manage.py makemigrations bookmark'
* Then apply migrations using 'python manage.py migrate'
* Create super user to using 'python manage.py createsuperuser', follow the cli for admin credentials.
* Runserver server using 'python manage.py runserver'
* Access the app's admin panel using 127.0.0.1:8000/admin

 CREATE CUSTOMERS
------------

* To create customers, users can access customer sections in the Admin panel.
* Provide all details of the customers including geolocation while creating customers.


 API endpoints
------------
* This APP is configured to use Django restframe work BasicAuthentication and IsAuthenticated permission required settings.
* Currently there are two endpoints available
  * '/api/create' - Accepts both POST and GET request. For the request method GET the endpoint will return all available 
    customers with their associated bookmarks.For request method POST the endpoint accepts param to create new bookmark.
  body format example in json- 
    {
    "customer":"2",
    "title":"Title Of bookmark",
    "url":"https://github.com",
    "source_name": "Git Hub"
    }
  * '/api/browse' - Accepts request method type 'GET'. This endpoinr can be used to  get the available bookmarks on the basis of query params passed
  available query params key
    * customer_id
    * source_name
    * title
    * lat , long, radius. Note: For location based filter all these three params are required
    * start_date, end_date Note: For date range based both of these two params are required in format "YYYY-MM-DD"
    * sort_by, This parameter can be passed to sort the order of response. Default is customer_id
