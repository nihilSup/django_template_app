from django.contrib import admin
from rango.models import Category, Page

admin.site.register(Category)

class PageAdmin(admin.ModelAdmin):
    'custom functionality for '
    list_display = ('title', 'category', 'url')
    fieldsets = [
        ('Main info:', {'fields': ['category']}),
        ('Details:', {'fields': ['title', 'url', 'views']})
    ]
admin.site.register(Page, PageAdmin)
