from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id","email","username","is_staff","is_active","is_superuser","role"]
    list_display_links = ["id","email","username"]
    list_filter = ["is_staff","is_superuser","is_active"]
    list_editable = ["is_active"]
    search_fields = ["email"]
    
    fieldsets = [
        (
            "User Login Information",{
                "fields" : ("email","password")
            }
        ),
        (
            "User Personal Information",{
                "fields" : ("first_name","last_name")
            }
        ),
        (
            "User Groups and Permission",{
                "fields" : ("groups","user_permissions")
            }
        ),
        (
            "User Status",{
                "fields" : ("is_active","is_staff","is_superuser")
            }
        ),
        (
            "Login Information",{
                "fields" : ("last_login",)
            }
        )
    ]

    ordering = ["id"]
    filter_horizontal = ("groups", "user_permissions")
