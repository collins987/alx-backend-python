from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to access or modify it.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False

        if request.method in ["PUT", "PATCH", "DELETE"]:
            # Only allow modifying or deleting if user is a participant
            return user in obj.participants.all()

        # Allow viewing if user is a participant
        return user in obj.participants.all()
