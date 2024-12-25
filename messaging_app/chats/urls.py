from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from chats import views

# Create a router and register ViewSets for the main routes
router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet, basename='messages')
router.register(r'conversations', views.ConversationViewSet, basename='conversations')

# Create a nested router to handle messages related to a specific conversation.
nested_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', views.MessageViewSet, basename='conversation-messages')

# The API URLs are now determined automatically by the router, including nested routes.
urlpatterns = [
    path('', include(router.urls)),          # Include main router
    path('', include(nested_router.urls)),   # Include nested router for messages in conversations
]
