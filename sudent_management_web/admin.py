from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from sudent_management_web.models import CustomUser, RoomMember

# Register your models here.
class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)
admin.site.register(RoomMember)