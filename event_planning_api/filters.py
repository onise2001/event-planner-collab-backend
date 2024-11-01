from rest_framework.filters import BaseFilterBackend


class EventFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        my_events = request.query_params.get('my-events')

        if my_events:
            queryset = queryset.filter(organizer=request.user)

        
        return queryset
    



class EventFilesFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        event_id = request.query_params.get('event_id')

        if event_id:
            queryset = queryset.filter(event__id=event_id)

        return queryset
    

class EventCommentsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        event_id = request.query_params.get('event_id')

        if event_id:
            queryset = queryset.filter(event__id=event_id)

        return queryset
    


class NotificationsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = queryset.filter(receiver=request.user)
        return queryset
    


class InvitationFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        my_invitations = request.query_params.get('my_inv')
        if my_invitations:
            queryset = queryset.filter(guest=request.user)

        return queryset
    



class RSVPFilesFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        event_id = request.query_params.get('event_id')
        my_rsvps = request.query_params.get('my_rsvp')

        if event_id:
            queryset = queryset.filter(event__id=event_id)
        
        if my_rsvps:
            queryset = queryset.filter(user__id=request.user.id)

        return queryset
    