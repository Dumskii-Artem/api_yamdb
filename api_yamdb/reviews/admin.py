from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title, User

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
        'is_staff',
        'is_superuser',
    )
    list_editable = ('role',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('role',)

    @admin.display(description='Инфо')
    def bio_info(self, user):
        return user.bio[:MAX_DISPLAY_LENGTH]


admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
