from django.contrib import admin
from .models import BookInstance, Book, Author, Genre


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    fields = ('id', 'due_back', 'status')


class BooksInline(admin.TabularInline):
    model = Book
    fields = ('title', 'isbn')


# admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn')
    inlines = [BooksInstanceInline]
    
    list_filter = ('author',)
    fieldsets = (
        ('Book data:', {
            'fields': [('title', 'author'), 'isbn']
        }),
    )


# admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'get_date_of_birth')
    inlines = [BooksInline]

    list_filter = ('last_name',)
    fieldsets = (
        ('Author data:', {
            'fields': [('first_name', 'last_name')]
        }),
        ('Years of life:', {
            'fields': [('date_of_birth', 'date_of_death')]
        }),
    )


admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)


# admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book')

    list_filter = ('due_back',)
    fieldsets = (
        ('Current book instance:', {
            'fields': [('book', 'id'), 'imprint']
        }),
        ('Availability:', {
            'fields': [('status', 'due_back')]
        }),
    )