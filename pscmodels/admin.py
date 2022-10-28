from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Posts, Shared,  Following, Comments, Archive, Vote, Profile

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Posts)
admin.site.register(Vote)
admin.site.register(Comments)
admin.site.register(Following)
admin.site.register(Shared)
admin.site.register(Archive)

UserAdmin.fieldsets += ('Custom fields set', {'fields': ('bio', 'role', 'profile_pic',)}),
