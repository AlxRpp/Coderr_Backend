from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import RegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationView(APIView):
    """Handles POST requests for creating a new user account.
    Returns an auth token right away so the client doesn't need to login seperately after registering."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Validates the registration data, creates the user and returns a token together with basic user info."""
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
    """Handles login by looking up the user by email and checking the password against the stored hash."""

    permission_classes = [AllowAny]
    data = {}

    def post(self, request):
        """Returns a token and basic user info if credentials are valid.
        Returns 400 for wrong password, missing fields or an unknown email adress."""
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            if not username or not password:
                return Response({'ErrorMessage': 'Please enter valid credentials '}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(username=username)
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
