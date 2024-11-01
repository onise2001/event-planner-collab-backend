from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Category, FileUpload, Privacy, Medium, Event, RSVP, Invitation, EventInfo,Comment, Notification
from .serializers import CategorySerializer, FileUploadSerializer, PrivacySerializer, MediumSerializer, EventSerializer, RSVPSerializer, InvitationSerializer, EventInfoSerializer,CommentSerializer,NotificationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOrganizer
from .filters import EventFilesFilter,EventCommentsFilter, EventFilter,NotificationsFilter,InvitationFilter,RSVPFilesFilter
from users.models import CustomUser

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
    filter_backends = [EventFilter]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    # def create(self,request):
    #     ...

    def get_permissions(self):
        if self.action in ['list', "retrieve",'head','options']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOrganizer]

        return [permission() for permission in permission_classes]


class RSVPViewSet(ModelViewSet):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    filter_backends = [RSVPFilesFilter]
    
    
    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        #event_obj = Event.objects.filter(pk=event['id'])
        event_info = EventInfo.objects.filter(event=event).first()
        user = self.request.user

        invitation = Invitation.objects.filter(event=event, guest=user).first()
        
        rsvp = serializer.save(user=user)
        event_info.total_rsvps += 1
        
        if invitation:
            if rsvp.accepted:
                event_info.total_accepted_rsvps += 1
                event_info.invitaion_accepted_rsvps += 1
                event.members += 1
            else :
                event_info.total_rejected_rsvps += 1
                event_info.invitation_rejected_rsvps += 1
        else:
            event_info.total_accepted_rsvps += 1
            event.members += 1

        
        event.save()
        
        event_info.save()


        if invitation:
            invitation.rsvp = rsvp
            invitation.save()
        





class InvitaionViewSet(ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    filter_backends = [InvitationFilter]


    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        event_info = EventInfo.objects.filter(event=event).first()
        if event_info:
            event_info.total_invitations += 1
            event_info.save()


        new_invitation = serializer.save(host=self.request.user)
        receiver = CustomUser.objects.filter(pk=serializer.data['guest']["id"]).first()
        notification = Notification.objects.create(
                type=Notification.TYPE_CHOICES[0][0],
                sender=self.request.user,
                receiver=receiver,
                invitation=new_invitation
        )
        notification.save()



class EventInfoViewSet(GenericViewSet):
    queryset = EventInfo.objects.all()
    serializer_class = EventInfoSerializer
    lookup_field = 'pk'

    def list(self,requset):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self,request, pk=None):
        event = self.get_object()
        if event:
            serializer = self.serializer_class(event)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_404_NOT_FOUND)
    


class FileUploadViewSet(GenericViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    filter_backends = [EventFilesFilter]


    def create(self,request):
        try:
            event = Event.objects.get(pk=request.data.get('event_id'))
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        

        file_list = request.FILES.getlist('file')
        print(file_list)
        file_instances = []

        for file in file_list:
            file_instance = FileUpload(event=event, file=file)
            file_instance.save()
            file_instances.append(file_instance)
        print(file_instances)
        serializer = self.serializer_class(file_instances, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    

    def list(self,request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)




class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [EventCommentsFilter]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class NotificationViewSet(GenericViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [NotificationsFilter]

    def list(self, request):
        serializer = self.serializer_class(self.filter_queryset(self.queryset), many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)