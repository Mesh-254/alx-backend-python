from django.urls import path, include
from rest_framework import routers

from chats import views

# Create a router and register our ViewSets with it.
router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet, basename='messages')
router.register(r'conversations', views.ConversationViewSet, basename='conversations')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]