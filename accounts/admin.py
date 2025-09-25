from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add custom fields to the admin change form.
    # These fields will appear in a new section titled 'Extra Info'.
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone_number', 'address', 'profile_picture', 'date_of_birth')}),
    )
