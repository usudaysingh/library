from django.contrib import admin
from .models import Books, AppUser,Status,BooksFlow #, Author, Publisher
# Register your models here.
#admin.site.register(Books)
admin.site.register(AppUser)
admin.site.register(Status)
admin.site.register(BooksFlow)
# admin.site.register(Author)
# admin.site.register(Publisher)