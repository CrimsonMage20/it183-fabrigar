from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodSerializerViewSet

router = DefaultRouter()
router.register(r'foods', FoodSerializerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]