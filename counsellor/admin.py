from django.contrib import admin
from counsellor.forms import CounsellorAdminCreationForm, UserAdminCreationForm
from counsellor.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
admin.site.register(Consent)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UnPriviledgedUserForm
    add_form = UserAdminCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "other_names",
        "is_active",
        "is_staff",
        "is_superuser",
        "user_type",
        "sex",
        "religion",
        "marital_status",
        "phone",
    ]

    list_display_links = ['username', 'email', 'first_name', 'last_name']
    
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']

    ordering = ['-created_at']
    list_filter = []
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'username',
            'first_name',
            'last_name',
            'other_names',
            'phone',
            'address',
            'sex',
            'religion',
            'marital_status',
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
        )}),
        (None, {'fields': (
            'user_type',

        )}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'password',
                'password2'
                )
            }
        ),
    )

class CounsellorAdmin(UserAdmin):
    add_form = CounsellorAdminCreationForm

    list_display = [
        "email",
        "first_name",
        "last_name",
        "other_names",
        "is_active",
        "is_staff",
        "is_superuser",
        "sex",
        "phone",
        "available",
    ]

    list_display_links = ['email', 'first_name', 'last_name']
    
    search_fields = ['first_name', 'last_name', 'email', 'phone']

    ordering = ['-created_at']
    list_filter = []
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'username',
            'first_name',
            'last_name',
            'other_names',
            'phone',
            'address',
            'sex',
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
        )}),
        (None, {'fields': (
            'available',

        )}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password',
                'password2'
                )
            }
        ),
    )



admin.site.register(User, UserAdmin)
admin.site.register(Counsellor, CounsellorAdmin)
