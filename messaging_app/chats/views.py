from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, CustomUser
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
)
from rest_framework.exceptions import PermissionDenied
from .permissions import IsParticipantOfConversation as ipoc

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    permission_classes = [permissions.IsAuthenticated, ipoc]

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        # Return only conversations the user is a participant in
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, ipoc]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        # Ensure user is part of the conversation
        if self.request.user not in conversation.participants.all():
            return Message.objects.none()

        return conversation.messages.all().order_by('sent_at')

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not part of this conversation.")

        serializer.save(conversation=conversation, sender=self.request.user)
