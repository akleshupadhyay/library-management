import jwt
from rest_framework.response import Response


class Authenticate():
    def check_authentication(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return Response({
                'message': 'Authentication Required'
            })
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({
                'message': 'Authentication Required'
            })
        return payload

    def check_librarian(self, user):
        if user.user_role == 'librarian':
            return True
        else:
            return False


