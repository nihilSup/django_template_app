from django.contrib import admin
from rango.models import Category, Page

class CategoryAdmin(admin.ModelAdmin):
    'custom functionality for category admin'
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)

class PageAdmin(admin.ModelAdmin):
    'custom functionality for page admin'
    list_display = ('title', 'category', 'url')
    fieldsets = [
        ('Main info:', {'fields': ['category']}),
        ('Details:', {'fields': ['title', 'url', 'views']})
    ]
admin.site.register(Page, PageAdmin)
