from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ["id","post_title","post_date"]

admin.site.register(Post,PostAdmin)
admin.site.register(PostImage)
admin.site.register(Comment)
admin.site.register(register_table)