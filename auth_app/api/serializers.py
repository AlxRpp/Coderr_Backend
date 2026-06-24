from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Handles new user registration. Expects username, email, password, repeated_password and type."""

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

    def validate_email(self, value):
        """Checks that no other user is already using this email adress before registration."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('email already exists')
        return value

    def save(self):
        """Creates the user account after verifying that both passwords match. The password is hashed before saving."""
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError(
                {'Error': 'Passwords dont match'})

        account = User(
            email=self.validated_data['email'], username=self.validated_data['username'], type=self.validated_data['type'])
        account.set_password(pw)
        account.save()
        return account
