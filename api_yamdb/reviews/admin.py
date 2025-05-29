from xmlrpc.client import boolean

from django.contrib import admin

from reviews.models import Comment, Review, User

MAX_DISPLAY_LENGTH = 30

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio_info',
        'role',
        'is_staff_display',
        'is_superuser_display',
    )
    list_editable = ('role',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('role',)

    @admin.display(description='Инфо')
    def bio_info(self, obj):
        return obj.bio[:MAX_DISPLAY_LENGTH]

    @admin.display(boolean=True, description='staff')
    def is_staff_display(self, obj):
        return obj.is_staff

    @admin.display(boolean=True, description='super')
    def is_superuser_display(self, obj):
        return obj.is_superuser

admin.site.register(Review)
admin.site.register(Comment)
