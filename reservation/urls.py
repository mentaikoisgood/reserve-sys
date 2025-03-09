from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'services', views.ServiceViewSet)
router.register(r'timeslots', views.TimeSlotViewSet)
router.register(r'reservations', views.ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 