from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chats import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'message', views.MessageViewSet, basename='messages')
router.register(r'conversation', views.ConversationViewSet, basename='conversations')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]