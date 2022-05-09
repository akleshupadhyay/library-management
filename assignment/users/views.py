from users.serializers import UserSerializers, UserProfileSerializers
from rest_framework.response import Response
from django.contrib.auth import authenticate
from users.utils import Authenticate
from rest_framework.views import APIView
import jwt
import datetime
from users.models import User_Profile
from django.contrib.auth.models import User




class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'message': 'Incorrect Username/password !'})

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': 'Login Successfull for {}'.format(user.username),
            'jwt_token':token
        }
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout successfully !'
        }
        return response


class ShowUsersView(APIView):

    def get(self, request):

        auth = Authenticate()
        payload = auth.check_authentication(request)
        user = User_Profile.objects.filter(user=payload['id']).first()

        if auth.check_librarian(user):
            member_ids = User_Profile.objects.filter(user_role='member')
            res = []
            for member in member_ids:
                profile_serializer = UserProfileSerializers(member)
                res.append(profile_serializer.data)
            return Response({
                'Members':res
            })
        return Response('Access Denied ! Un Authorised Operation', status=400)


class DeleteUserView(APIView):
    def delete(self, request):
        auth = Authenticate()
        payload = auth.check_authentication(request)
        user = User_Profile.objects.filter(user=payload['id']).first()
        try:
            if request.data['username'] != user.user.username and user.user_role != 'librarian':
                return Response({
                    'message': 'UnAtuhorised access'
                })
        except Exception as e:
            return Response({
                'message': 'Something Went Wrong'
            })
        user_id = User.objects.filter(username=request.data['username']).first()
        user_id.delete()
        return Response(
            {'message': 'User Deleted Successfully'}
        )


class UpdateMemberView(APIView):

    def post(self, request):
        auth = Authenticate()
        payload = auth.check_authentication(request)
        user = User_Profile.objects.filter(user=payload['id']).first()
        if auth.check_librarian(user):
            user = User_Profile.objects.filter(username=request.data['username'])
            if not user:
                return Response({
                    'message': 'No record found'
                })
            vals = {key:request.data[key] for key in request.data.keys()}
            user.update(**vals)
            user = user.first()
            user.save()
            return Response({
                'message': 'Update Successfull'
            })
        return Response('Access Denied ! Un Authorised Operation', status=400)