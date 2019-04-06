from django.contrib import admin
from app.models import MediaAuthor, Media, Review, User

# Register your models here.
admin.site.register(MediaAuthor)
admin.site.register(Media)
admin.site.register(Review)
admin.site.register(User)