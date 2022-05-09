from django.urls import path
from .views import AddBookView, AllBooksView, BookDeleteView, IssueBookView, ReturnBookView, UpdateBookView


urlpatterns = [
    path('addbook/', AddBookView.as_view()),
    path('booksdetails/', AllBooksView.as_view()),
    path('deletebook/', BookDeleteView.as_view()),
    path('issuebook/', IssueBookView.as_view()),
    path('returnbook/', ReturnBookView.as_view()),
    path('updatebook/', UpdateBookView.as_view()),
]