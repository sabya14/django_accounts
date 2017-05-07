from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    CharField
)
from django.utils.text import slugify
from .tasks import activation_mail_send
from django.db.models import Q
User = get_user_model()

class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'email',
            'first_name',
            'last_name'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True}
        }
    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password')
        if not email and not username:
            raise ValidationError('A username or email is required to login')
        user_obj = User.objects.filter(
            Q(email=email) |
            Q(username=username)
        ).distinct()
        user_obj = user_obj.exclude(email__isnull=True).exclude(email__iexact='')
        if user_obj.exists() and user_obj.count() == 1:
            user_obj = user_obj.first()
        else:
            raise ValidationError('This username/email is not valid.')

        if user_obj:
            if not user_obj.check_password(raw_password=password):
                raise ValidationError('Incorrect password')
        data['first_name'] = user_obj.first_name
        data['last_name'] = user_obj.last_name
        data['email'] = user_obj.email
        data['id'] = user_obj.id
        return data

class UserCreateSerializer(ModelSerializer):
    password2 = CharField(label="Confirm Password",allow_blank=False, write_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'password2',
            'email',
            'first_name',
            'last_name'
        ]
        extra_kwargs = {
            'password':{'write_only': True},
            'password2': {'write_only': True}
            }
    def validate(self, data):
        email = data.get('email',None)
        username = data.get('username',None)
        password = data.get('password',None)
        if not email and not username:
            raise ValidationError("UserName or Email is Required")
        user_obj = User.objects.filter(
            Q(email=email) |
            Q(username=username)
        ).distinct()
        

    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'password2',
            'email',
            'first_name',
            'last_name'
        ]
        extra_kwargs = {
            'password':{'write_only': True},
            'password2': {'write_only': True}
            }


    def validate_password(self,value):
        '''
        :param password:
        :type email:
        :return: 
        '''
        data = self.get_initial()
        password2 = data.get('password2')
        password = value
        if password != password2:
            raise ValidationError("Password should match")
        return value

    def validate_email(self,value):
        '''
        :param email: 
        :return email: 
        '''
        email = value
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("User with the emails already exists")
        return value

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        username = slugify(email)
        print(username)
        user_obj = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.is_active = False
        user_obj.save()
        activation_mail_send.delay(user_obj.id)
        return validated_data

class RetrieveUpdateDestroySerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'email',
            'first_name',
            'last_name'
        ]

    def update(self, instance, validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        user = self.context.get('request').user
        if user.id != instance.id:
            raise ValidationError("Permission Denied")
        instance.email = email
        instance.first_name = first_name
        instance.last_name = last_name
        instance.save()
        return instance

class ProfilePasswordUpdateSerializer(ModelSerializer):
    old_password = CharField(label="Old Password",allow_blank=False, write_only=True)
    new_password = CharField(label="New Password", allow_blank=False, write_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'old_password',
            'new_password',
        ]

    def update(self, instance, validated_data):
        password = validated_data.get('old_password')
        new_password = validated_data.get('new_password')
        user = self.context.get('request').user
        if user.id != instance.id:
            raise ValidationError("Permission Denied")
        if not instance.check_password(raw_password=password):
            raise ValidationError("Incorrect password")
        instance.set_password(new_password)
        instance.save()
        return instance
