from django.contrib import admin
from chat.models import Conversation, Message, AuthToken

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(AuthToken)
