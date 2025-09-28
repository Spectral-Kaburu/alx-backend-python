from django.urls import path, include
from rest_framework_nested import routers as rts
from .views import ConversationViewSet, MessageViewSet
from .auth import RegisterView, LoginView, RefreshView

con = 'conversation'
# DRF routers
router = rts.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename=con)

# Nested router for messages under conversations
conrts = rts.NestedDefaultRouter(router, r'conversations', lookup=con)
conrts.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView, name="login"),
    path("refresh/", RefreshView, name="token_refresh"),
    path('', include(router.urls)),
    path('', include(conrts.urls)),
]


"""from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# Root router for conversations
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename=con)

# Nested router for messages under conversations
conrts = routers.NestedDefaultRouter(router, r'conversations', lookup=con)
conrts.register(r'messages', MessageViewSet, basename='conversation-messages')

# Export both sets of URLs
urlpatterns = router.urls + conrts.urls
"""