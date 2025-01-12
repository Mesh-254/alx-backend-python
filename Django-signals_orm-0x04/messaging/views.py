from .models import MessageHistory, Message
from django.db.models import Prefetch
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def message_history(message_id):
    """
    Display the message edit history in the user interface, 
    allowing users to view previous versions of their messages.

    """
    # Get the message history for a message
    message_history = MessageHistory.objects.filter(pk=message_id
                                                    ).order_by('timestamp').all()
    return message_history


def delete_user_account(request):
    """
    Function to delete a user account and all associated data.
    """
    user = request.user
    user.delete()  # This will trigger the post_delete signal
    return HttpResponse("Your account has been deleted successfully.")

@cache_page(60)
def threaded_conversation(request):
    """
    Function to display a threaded conversations for a given user.
    """
    # Query all top-level messages for the user
    top_level_messages = Message.objects.filter(sender=request.user, parent_message_isnull=True
                                                ).prefetch_related(Prefetch(
                                                    'replies',
                                                    queryset=Message.objects.select_related(
                                                        'sender', 'receiver'),
                                                    to_attr='replies_cache'  # Store pre-fetched replies here
                                                )
    ).select_related('sender', 'receiver')

    def build_thread(message):
        """
        Function to build a threaded conversation.
        recursively
        """
        return {
            'message': message,
            'replies': [build_thread(reply) for reply in getattr(message, 'replies_cache', [])]
        }
    # Build the entire threaded structure
    threaded_conversation = [build_thread(
        message) for message in top_level_messages]

    return threaded_conversation


def unread_inbox_view(request):
    """
     display only unread messages in a user’s inbox.

    """

    user = request.user
    unreadmessages = Message.unread.unread_for_user(user).only('id', 'sender', 'content', 'created_at')

    return unreadmessages
