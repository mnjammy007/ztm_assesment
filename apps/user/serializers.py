from rest_framework import serializers
from apps.user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

            # Blacklist all existing refresh tokens
            for token in OutstandingToken.objects.filter(user=instance):
                BlacklistedToken.objects.get_or_create(token=token)

        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    I have custom token serializer as auto incrementing id was not giving the clear picture of the user and I wanted to have a more descriptive token. The token will have the following claims:
    to have a look at the token about what data it contains, visit https://www.jwt.io/ and paste the token in the "Encoded" section, you will see the claims in the "Decoded" section.
    - iss   (issuer)
    - username
    - email
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["iss"] = "zippee"
        token["username"] = user.username
        token["email"] = user.email

        return token
