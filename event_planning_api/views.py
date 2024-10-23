from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Category, Privacy, Medium, Event, RSVP, Invitation
from .serializers import CategorySerializer, PrivacySerializer, MediumSerializer, EventSerializer, RSVPSerializer, InvitationSerializer
# Create your views here.

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PrivacyViewSet(ModelViewSet):
    queryset = Privacy.objects.all()
    serializer_class = PrivacySerializer


class MediumViewSet(ModelViewSet):
    queryset = Medium.objects.all()
    serializer_class = MediumSerializer



class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    # def create(self,request):
    #     ...



class RSVPViewSet(ModelViewSet):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class InvitaionViewSet(ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)