from .models import MessageHistory

from django.http import HttpResponse


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
    user.delete() # This will trigger the post_delete signal
    return HttpResponse("Your account has been deleted successfully.")

