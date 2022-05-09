from rest_framework import serializers

from library.models import Books
from users.utils import Authenticate
from users.models import User_Profile

class BooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = ('id', 'book_name', 'author_name', 'rate', 'status', 'issued_by')


class ValidateSerializer(serializers.Serializer):

    def validate(self, attrs):
        auth = Authenticate()
        payload = auth.check_authentication(attrs)
        user = User_Profile.objects.get(user=payload['id'])
        if auth.check_librarian(user):
            return user
        else:
            raise serializers.ValidationError({'meaaage':'Access Denied ! Un Authorised Operation'})

