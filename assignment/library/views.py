from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User, User_Profile
from library.models import Books
from library.serializers import BooksSerializer, ValidateSerializer
from users.utils import Authenticate
# import jwt
# import datetime


class AddBookView(APIView):

    def post(self, request):
        auth = Authenticate()
        payload = auth.check_authentication(request)
        user = User_Profile.objects.filter(user=payload['id']).first()

        if auth.check_librarian(user):
            book = BooksSerializer(data=request.data)
            book.is_valid(raise_exception=True)
            book.save()
            return Response(book.data)
        else:
            return Response('Access Denied ! Un Authorised Operation', status=400)


class AllBooksView(APIView):

    def get(self, request):
        auth = Authenticate()
        payload = auth.check_authentication(request)
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response(serializer.data)


class BookDeleteView(APIView):

    def delete(self, request):
        auth = Authenticate()
        payload = auth.check_authentication(request)
        user = User_Profile.objects.get(user=payload['id'])

        # serializer = ValidateSerializer(data=request)
        # if serializer.is_valid(raise_exception=True):
            # auth.check_librarian(user)
        if auth.check_librarian(user):
            book_id = Books.objects.filter(id=request.data['id'])
            book_id.delete()
            return Response({
                'message': 'Book deleted successfully'
            })
        return Response('Access Denied ! Un Authorised Operation', status=400)


class IssueBookView(APIView):

    def post(self, request):
        auth = Authenticate()
        payload = auth.check_authentication(request)
        user = User_Profile.objects.filter(user=payload['id']).first()

        book_id = request.data['id']
        book_id = Books.objects.filter(id=book_id).first()
        if book_id.status == 'BORROWED':
            return Response({
                'message': 'Book already issued, please try later'
            })
        book_id.status = 'BORROWED'
        book_id.issued_by = user.user.id
        book_id.save()
        return Response({
            'message': 'Book Issued'
        })

class ReturnBookView(APIView):

    def post(self, request):
        auth = Authenticate()
        payload = auth.check_authentication(request)
        user = User_Profile.objects.filter(user=payload['id']).first()
        book_id = request.data['id']
        book_id = Books.objects.filter(id=book_id).first()
        if user.user.id != book_id.issued_by.id:
            return Response({
                'message': 'Something Went Wrong, User have not issued this book'
            })
        book_id.status = 'AVAILABLE'
        book_id.issued_by = None
        book_id.save()
        return Response({
            'message': 'Returned Successfully',
        })


class UpdateBookView(APIView):

    def post(self, request):
        auth = Authenticate()
        payload = auth.check_authentication(request)
        user = User_Profile.objects.filter(id=payload['id']).first()

        if auth.check_librarian(user):
            book_id = Books.objects.filter(id=request.data['id'])
            if not book_id:
                return Response({
                    'message': 'No record found'
                })
            vals = {key:request.data[key] for key in request.data.keys()}
            book_id.update(**vals)
            book_id = book_id.first()
            book_id.save()
            return Response({
                'message': 'Update Successfull'
            })
        return Response('Access Denied ! Un Authorised Operation', status=400)