from django.contrib import admin
from .models import *


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]
    list_display_links = ['title']
    search_fields = ['title']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = [('first_name', 'last_name'), ('date_of_birth', 'date_of_death')]
    list_display_links = ['first_name', 'last_name']
    search_fields = ['last_name', 'first_name']


admin.site.register(Author, AuthorAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

admin.site.register(Genre, GenreAdmin)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('book',)
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
