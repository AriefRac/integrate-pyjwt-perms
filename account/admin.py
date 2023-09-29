from django.contrib import admin
from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    '''Admin View for CustomUser'''

    list_display = (
        'email',
        'fullname',
        'id',
        'is_active',
        'is_staff',
        'is_superuser'

        )