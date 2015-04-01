from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from chat.models import Conversation, Message, AuthToken
import json
import traceback


@csrf_exempt
def api(request):
    if not request.method == 'POST' or request.META['REMOTE_ADDR'] != "127.0.0.1":
        return HttpResponse(status=403)

    try:

        debug_file = open('/srv/teamcity/django-debug/chat-api.log', 'a')

        result = {'status': "OK"}
        data = json.loads(request.POST.get('request', ''))
        action = data.get('action', '')

        debug_file.write(action + '\n')

        if action == "checkCredentials":
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user:
                result['authResult'] = "OK"
                result['username'] = user.username
            else:
                result['authResult'] = "ERROR"

        elif action == "checkAuthToken":
            user = User.objects.get(username=data.get('username'))
            token = AuthToken.objects.filter(user=user, token=data.get('authToken'))
            if token.exists():
                result['authResult'] = "OK"
                result['username'] = user.username
            else:
                result['authResult'] = "ERROR"

        elif action == "addMessage":
            conversation = Conversation.objects.get(id=data.get('message').get('conversation'))
            sender = User.objects.get(username=data.get('message').get('sender'))
            Message.create(conversation, sender, data.get('message').get('text'), data.get('message').get('timestamp'))

        elif action == "getMessages":
            conversation = Conversation.objects.get(id=data.get('conversation'))
            if data.get('messageTimeStamp'):
                message = Message.objects.get(conversation=conversation, timestamp=data.get('messageTimeStamp'))
            else:
                message = None
            result['messages'] = conversation.get_messages(data.get('direction'), message)

        elif action == "getOrAddConversation":
            users = []
            for user in data.get('userlist'):
                # TODO: check if users are connected users
                users.append(User.objects.get(username=user))
            if len(users) > 1:
                conversation = Conversation.find_by_users_or_create(users)
                result['conversation'] = {}
                result['conversation']['id'] = conversation.id
                result['name'] = conversation.name
                result['conversation']['users'] = []
                for user in users:
                    result['conversation']['users'].append(user.username)
            else:
                result['status'] = "ERROR - there must be at least 2 users in a conversation"

        elif action == "getConversationsOfUser":
            user = User.objects.get(username=data.get('username'))
            conversations = Conversation.get_conversations_of_user(user)
            result['conversations'] = []
            for conversation in conversations:
                users = []
                for user in list(conversation.members.all()):
                    users.append(user.username)
                conversation_object = {
                    'id': conversation.id,
                    'name': conversation.name,
                    'users': users
                }
                result['conversations'].append(conversation_object)
                debug_file.write(conversation_object)

        elif action == "updateAuthToken":
            user = User.objects.get(username=data.get('username'))
            AuthToken.create_or_update_for_user(user, data.get('newAuthToken'), data.get('oldAuthToken'))

        elif action == "version":
            result['version'] = "v0.1"

        else:
            result['status'] = "ERROR - unknown action"

    except Conversation.DoesNotExist:
        result['status'] = "ERROR - unknown conversation"
    except User.DoesNotExist:
        result['status'] = "ERROR - unknown user"
    except Exception as e:
        result['status'] = "ERROR - unexpected error"
        print("ERROR - " + e.__str__())
        print(type(e))
        print(traceback.print_tb(e.__traceback__))

        debug_file.write("ERROR - " + e.__str__())
        debug_file.write(type(e))
        debug_file.write(traceback.print_tb(e.__traceback__))

        debug_file.write(result['status'])

    try:
        return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as e:
        debug_file.write(str(result))
        debug_file.write("ERROR - " + e.__str__())
        debug_file.write(type(e))
        debug_file.write(traceback.print_tb(e.__traceback__))