from rest_framework import serializers
from .models import Category, Privacy, Medium, Event, RSVP, Invitation
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



class EventSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, source='category')

    privacy = PrivacySerializer(read_only=True)
    privacy_id = serializers.PrimaryKeyRelatedField(queryset=Privacy.objects.all(), write_only=True, source='privacy')
    
    medium = MediumSerializer(read_only=True)
    medium_id = serializers.PrimaryKeyRelatedField(queryset=Medium.objects.all(), write_only=True, source='medium')

    organizer = CustomUserSerializer(read_only=True)
    #organizer_id =serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, source='organizer')
    class Meta:
        model = Event
        fields = '__all__'

    


class RSVPSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), write_only=True, source="event")
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, source='user')
    class Meta:
        model = RSVP
        fields = '__all__'



class InvitationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), write_only=True, source="event")
    host = CustomUserSerializer(read_only=True)
    host_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, source='host')
    guest = CustomUserSerializer(read_only=True)
    guest_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, source='guest')
    
    class Meta:
        model = Invitation
        fields = '__all__'


