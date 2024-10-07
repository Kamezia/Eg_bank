from django.urls import path,include
from core import views
from rest_framework import routers
from core.views import CategoryModelViewSet, TransactionModelViewSet, CurrencyModelViewSet

router = routers.SimpleRouter()
router.register('categories', CategoryModelViewSet, basename="categories")
router.register('transactions', TransactionModelViewSet, basename="transactions")
router.register('currencies', CurrencyModelViewSet, basename="currencies")
# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),

]
