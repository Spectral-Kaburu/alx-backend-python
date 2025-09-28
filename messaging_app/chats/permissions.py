from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
- Only authenticated users can access the API.
- Only participants of a conversation can send/view/update/delete messages.
    """

    def has_permission(self, request, view):
        # Must be logged in
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant in the conversation.
        Works for both Conversation and Message objects.
        """
        if hasattr(obj, "participants"):  # conversation instance
            return request.user in obj.participants.all()

        if hasattr(obj, "conversation"):  # message instance
            return request.user in obj.conversation.participants.all()

        return False
