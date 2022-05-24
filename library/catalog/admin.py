from django.contrib import admin
from .models import BookInstance, Book, Author, Genre


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


# admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn')
    inlines = [BooksInstanceInline]
    
    list_filter = ('title',)


# admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth')

    fields = [('first_name', 'last_name'), ('date_of_birth')]

    list_filter = ('last_name',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)


# admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
