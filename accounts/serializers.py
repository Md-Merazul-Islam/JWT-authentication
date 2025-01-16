# from django.contrib.auth.models import User
# from rest_framework import serializers


# class UserRegisterSerializer(serializers.ModelSerializer):
#     confirm_password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'confirm_password']

#     def validate(self, data):
#         if data['password'] != data['confirm_password']:
#             raise serializers.ValidationError({"error": "Passwords do not match."})

#         if User.objects.filter(email=data['email']).exists():
#             raise serializers.ValidationError({"email": "Email already exists."})

#         if User.objects.filter(username=data['username']).exists():
#             raise serializers.ValidationError({"username": "Username already exists."})

#         return data

#     def create(self, validated_data):
#         validated_data.pop('confirm_password')
#         user= User(username=validated_data['username'],
#                    email =validated_data['email']
#                 )
#         user.set_password(validated_data['password'])
#         user.is_active=True
#         user.save()
#         return user

# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)

# class UserDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id','username','email','first_name','last_name']


from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"error": "Passwords do not match."})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {"email": "Email already exists."})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                {"username": "Username already exists."})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
