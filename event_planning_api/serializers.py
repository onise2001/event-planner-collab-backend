from rest_framework import serializers
from .models import Category, FileUpload, Privacy, Medium, Event, RSVP, Invitation, EventInfo, Comment, Notification
from users.serializers import CustomUserSerializer
from users.models import CustomUser

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Privacy
        fields = '__all__'

class MediumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medium
        fields = '__all__'


class SimpleInvitationSerializer(serializers.ModelSerializer):
    guest_id = serializers.PrimaryKeyRelatedField(read_only=True, source='guest')

    class Meta:
        model = Invitation
        fields = ['id', 'guest_id']



class EventSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, source='category')

    privacy = PrivacySerializer(read_only=True)
    privacy_id = serializers.PrimaryKeyRelatedField(queryset=Privacy.objects.all(), write_only=True, source='privacy')
    
    medium = MediumSerializer(read_only=True)
    medium_id = serializers.PrimaryKeyRelatedField(queryset=Medium.objects.all(), write_only=True, source='medium')

    organizer = CustomUserSerializer(read_only=True)
    #organizer_id =serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, source='organizer')
    invitations = SimpleInvitationSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = '__all__'

    
    
    def create(self,validated_data):
            new_event = Event.objects.create(**validated_data)
            if new_event:
                event_info = EventInfo.objects.create(event=new_event,host=new_event.organizer)
                event_info.save()
            new_event.save()
            return new_event

    


class RSVPSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), write_only=True, source="event")
    user = CustomUserSerializer(read_only=True)
    #user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, source='user')
    class Meta:
        model = RSVP
        fields = '__all__'



class InvitationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), write_only=True, source="event")
    host = CustomUserSerializer(read_only=True)
    #host_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, source='host')
    guest = CustomUserSerializer(read_only=True)
    guest_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, source='guest')
    rsvp = RSVPSerializer(read_only=True)
    
    class Meta:
        model = Invitation
        fields = '__all__'




class EventInfoSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    host  = CustomUserSerializer(read_only=True)
    class Meta:
        model = EventInfo
        fields = '__all__'



class FileUploadSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), write_only=True, source='event')
    class Meta:
        model = FileUpload
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    #event = EventSerializer(read_only=True, )
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), source='event')
    user = CustomUserSerializer(read_only=True)
    # user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, source='user')
    class Meta:
        model = Comment
        fields = ['id','text', 'user','event_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['event_id'] = instance.event.id  # Keep only the event ID in output
        return representation
    



class NotificationSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)
    receiver = CustomUserSerializer(read_only=True)
    invitation = InvitationSerializer(read_only=True)
    rsvp =  RSVPSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'