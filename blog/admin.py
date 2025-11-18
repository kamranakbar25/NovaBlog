from django.contrib import admin
from .models import Post, Category, Comment

# Category register karein
admin.site.register(Category)

# Post Admin customization (Yahan galti thi, ab fix hai)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    search_fields = ('title', 'body')

admin.site.register(Post, PostAdmin)

# Comment register karein
admin.site.register(Comment)