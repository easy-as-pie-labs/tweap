from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from chat.models import Conversation, Message, AuthToken
import json


@csrf_exempt
def api(request):
    if not request.method == 'POST' or request.META['REMOTE_ADDR'] != "127.0.0.1":
        return HttpResponse(status=403)

    print(request.POST.get('request'))
    data = json.loads(request.POST.get('request', ''))

    action = data.get('action')
    result = {}
    result.status = "OK"

    try:

        if action == "checkCredentials":
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user:
                result.authResult = "OK"
            else:
                result.authResult = "ERROR"

        elif action == "addMessage":
            conversation = Conversation.objects.get(id=data.get('message').get('conversation'))
            sender = User.objects.get(username=data.get('message').get('sender'))
            Message.create(conversation, sender, data.get('message').get('text'))

        elif action == "getMessages":
            conversation = Conversation.objects.get(id=data.get('conversation'))
            message = Message.objects.filter(id=data.get('messageId'))
            if not message.exists():
                message = None
            result.messages = conversation.get_messages(message)

        elif action == "getOrAddConversation":
            users = []
            for user in data.get('userlist'):
                # TODO: check if users are connected users
                users.append(User.objects.filter(username=user))
            if len(users) > 1:
                conversation = Conversation.find_by_users_or_create(users)
                result.conversation = {}
                result.conversation.id = conversation.id
                result.conversation.users = []
                for user in users:
                    result.conversation.users.append(user.username)
            else:
                result.status = "ERROR - there must be at least 2 users in a conversation"

        elif action == "getConversationsOfUser":
            user = User.objects.get(username=data.get('username'))
            conversations = Conversation.get_conversations_of_user(user)
            result.conversations = []
            for conversation in conversations:
                result.conversations.append(conversation.id)

        elif action == "updateAuthToken":
            user = User.objects.get(username=data.get('username'))
            AuthToken.create_or_update_for_user(user, data.get('newAuthToken'), data.get('oldAuthToken'))

        elif action == "getAuthTokensForUser":
            user = User.objects.get(username=data.get('username'))
            tokens = AuthToken.get_for_user(user)
            result.authTokens = []
            for token in tokens:
                result.authTokens.append[token.token]

        elif action == "version":
            result.version = "v0.1"

        else:
            result.status = "ERROR - unknown action"

    except conversation.DoesNotExist:
        result.status = "ERROR - unknown conversation"
    except User.DoesNotExist:
        result.status = "ERROR - unknown user"
    except Exception as e:
        result.status = "ERROR - " + Exception.__name__

    print(result)
    return HttpResponse(json.dumps(result), content_type="application/json")