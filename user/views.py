from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):

    def post(self, request):
        data = request.data
        role=data['role'].lower()
        if (role == 'owner' or role == 'employee' or role == 'customer'):
            user = User.objects.create_user(email=data['email'], password=data['password'], role=data['role'], name=data['name'])
            return Response(UserSerializer(user).data, status=201)
        return Response({'error': 'Invalid'}, status=400)


from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class LoginView(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user': UserSerializer(user).data})
        return Response({'error': 'Invalid'}, status=400)



class UsersView(APIView):

    permission_classes = [IsAuthenticated]
    def get (self, request):
        query= User.objects.all()
        serializer = UserSerializer(query, many= True)
        return Response(serializer.data)
