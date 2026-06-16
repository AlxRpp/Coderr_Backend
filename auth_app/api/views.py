from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Creates a new user and returns a token right away."""
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id
            }
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    permission_classes = [AllowAny]
    data = {}

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            if not email or not password:
                return Response({'ErrorMessage': 'Please enter valid credentials '}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(email=email)
            pw_check = user.check_password(password)

            if pw_check:
                token, created = Token.objects.get_or_create(user=user)
                self.data = {
                    'token': token.key,
                    'username': user.username,
                    'email': user.email,
                    'user_id': user.id
                }
            else:
                return Response({'ErrorMessage': 'Please enter valid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'ErrorMessage': 'Please enter valid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.data, status=status.HTTP_200_OK)
