from django.contrib import admin

from .models import *

admin.site.register(Repositorium)
admin.site.register(Issue)
admin.site.register(Branch)
admin.site.register(Commit)
admin.site.register(Comment)
admin.site.register(Milestone)
admin.site.register(Notification)
admin.site.register(Reaction)
admin.site.register(Task)
admin.site.register(Event)
admin.site.register(PullRequest)