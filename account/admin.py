from django.contrib import admin
from account.models import User
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
 
class UserModelAdmin(BaseUserAdmin):
    list_display = ('id','email', 'name', 'tc', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'tc')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name','tc', 'password1', 'password2'),
        }),
    )
    search_fields = ('id',)
    ordering = ('email','id')
    filter_horizontal = ()

admin.site.register(User, UserModelAdmin)

admin.site.register(Place)
admin.site.register(Week)
admin.site.register(Flight)
admin.site.register(Passenger)
# admin.site.register(User)
admin.site.register(Ticket)