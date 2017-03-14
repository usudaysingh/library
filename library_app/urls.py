'''
___author__ ="uday"
'''

from django.conf.urls import url
from .apis import BookViewset,UpdateRetrieveBook

urlpatterns = [
    url(r'^books/$', BookViewset.as_view({'post': 'create', 'get': 'list'}), name='books'),
    url(r'^books/(?P<book_id>\w+)$', UpdateRetrieveBook.as_view({'put': 'update', 'get': 'retrieve'}), name='book-update'),
]
