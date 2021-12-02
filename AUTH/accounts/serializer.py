from rest_framework import serializers
from django.contrib.auth import authenticate


from django.contrib.auth import get_user_model
User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #phone, password, customer_name = 'Bablu', dob = '1998-11-2', email = 'rajukaju@gmail.com', createdDate
        fields = ('phone', 'password')
        #fields = ('phone', 'password', 'customer_name', 'dob', 'email', 'createdDate')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'first_login')


class LoginUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        if phone and password:
            if User.objects.filter(phone=phone).exists():
                print(phone,password)
                user = authenticate(request=self.context.get('request'),
                                    phone=phone, password=password)
                print(user)

            else:
                msg = {'detail': 'Phone number is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = {
                'status' : False,
                'detail' : 'phone no and pswd not found in request'
            }
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data