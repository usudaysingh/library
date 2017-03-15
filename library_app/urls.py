'''
___author__ ="uday"
'''

from django.conf.urls import url
from .apis import BookViewset,UpdateRetrieveBook, UpdateBookStatus

urlpatterns = [
    url(r'^books/$', BookViewset.as_view({'post': 'create', 'get': 'list'}), name='books'),
    url(r'^books/(?P<book_id>\d+)$', UpdateRetrieveBook.as_view({'put': 'update', 'get': 'retrieve'}), name='book-update'),
    url(r'^books/update_status/(?P<book_id>\d+)$', UpdateBookStatus.as_view({'put':'update'}),name='book-status-update'),
]
