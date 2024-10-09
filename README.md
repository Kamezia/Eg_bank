## Eg bank
this a virtual bank where you can do some simple transactions (create, delete, update, retrieve) transactions, currencies and categories but only the authoraized users can execute it.


## Set up the requirements to run the on your browser

First, you‘ll need to have Python installed, which you can download from the official Python website if you don‘t have it already. Then create a folder on your desktop (Eg_bank)

Create a virtual environment to isolate its packages from your computer:

```terminal(powershell)
python -m venv venvo
```

Activate the virtual environment:

```terminal(powershell)
venvo\Scripts\activate.ps1
```

With the virtual environment active, install Django using pip:

```terminal(powershell)
pip install django
pip install djangorestframework
```

# Creating the Django Project

django-admin startproject (piggybank)

## This will create a new directory called piggybank with the basic structure of a Django project. Let‘s also create a new app within our project that will handle the core piggybank functionality:

```terminal(powershell)
cd (Eg_bank)
python manage.py startapp (core)
```

The created app(core) is where we‘ll put most of our project settings file code. Make sure to add it to the list of installed apps in the your piggybank/settings.py file:

```python
INSTALLED_APPS = [
    ...
    'core',
]
```

# Designing the Database Models

Next, let‘s consider what database models we‘ll need for our your project app. We‘ll define models for:

User: the built-in Django user model, extended with a custom user profile.
Currency: represents the currencies on the bank.
Category: represents the type of the transaction.
Transaction: represents the transaction you want to execute.
AllowList: this to get the category by ip_address.

Here‘s an example of what model might look like (core/models.py):
```python 
from django.db import models
from django.contrib.auth.models import User


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=32, blank=True)


    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount  = models.DecimalField(max_digits=7, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="transactions")
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="transactions")


    def __str__(self):
        return f"{self.amount} {self.currency.code} {self.date}"
    

class AllowList(models.Model):   
    ip_address = models.GenericIPAddressField()
    
    def __str__(self):
        return self.ip_address
```


### We can define similar models for any other app you want to create.  After creating the models, we need to create a migration and sync the database:

```terminal(powershell)
python manage.py makemigrations 
python manage.py migrate
```


## Now we move on the views (where we write the logic of our app) and here an example:

### core.views.py

```python 
from rest_framework.viewsets import ModelViewSet
from .models import Currency
from .serializers import CurrencySerializer



class CurrencyModelViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
```

This operate the CRUD operations create, delete, update and retrieve.


## Then create a serializers file to transform/recreate data objects to/from a portable format.

### core.serializers.py 


```python
from rest_framework import serializers
from core.models import Currency

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name")
```

## After creating the serializers.py, create the urls.py file to get the endpoint directory 

### core.urls.py

```python
from django.urls import path,include
from core import views
from rest_framework import routers
from core.views import CurrencyModelViewSet

router = routers.SimpleRouter()

router.register('currencies', CurrencyModelViewSet, basename="currencies")

urlpatterns = [
    path('', include(router.urls)),

]
```

## In order to be able to execute the operations and read the changes you have done, you must set the the urls of the app(core) in the urls.py of the project(piggybank):

### piggybank.urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("core.urls")),
]
```

## How to Perform CRUD Operations with Postman

To perform CRUD operations, such as listing all currencies, you can use Postman. 

### Step 1: Open Postman

Make sure you have Postman installed on your computer.

### Step 2: Create a New Request

In Postman, create a new request.

### Step 3: Enter the URL

To get a list of all currencies, enter the following URL:

### Step 4: Send the Request

Select the **GET** method and click **Send**.

You should see a list of all currencies in the response.

![List of all currencies](./"C:\Users\HP\Downloads\List Currencies.png")

---