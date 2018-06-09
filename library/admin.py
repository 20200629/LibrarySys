from django.contrib import admin
from .models import Book,Tag
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ['id','isbn', 'title', 'author','translator','publisher']

admin.site.register(Book,BookAdmin)
admin.site.register(Tag)

