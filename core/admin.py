from django.contrib import admin
from .models import Currency, Category, Transaction,AllowList
# Register your models here.

admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(AllowList)