from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('username', 'full_name',
                                          'gender')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2', 'username', 'full_name', 'gender',),
        }),
    )
    list_display = ('name', 'username', 'group', 'is_staff')
    search_fields = ('username', 'full_name')
    ordering = ('-id',)

    def name(self, ins):
        return ins.username+" "+ins.full_name

    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)
    group.short_description = 'Groups'