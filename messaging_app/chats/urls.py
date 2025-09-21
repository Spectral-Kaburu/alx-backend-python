from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# Root router for conversations
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under conversations
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Export both sets of URLs
urlpatterns = router.urls + conversations_router.urls
