from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PrivacyViewSet, MediumViewSet, EventViewSet,RSVPViewSet,InvitaionViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'category', CategoryViewSet)
router.register(r'privacy',PrivacyViewSet)
router.register(r'medium', MediumViewSet)
router.register(r'event', EventViewSet)
router.register(r'rsvp', RSVPViewSet)
router.register(r'invitation', InvitaionViewSet)

urlpatterns = [
    path('', include(router.urls))
    
]
