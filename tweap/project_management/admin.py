from django.contrib import admin
from project_management.models import Project, Invitation, Tag

admin.site.register(Project)
admin.site.register(Invitation)
admin.site.register(Tag)