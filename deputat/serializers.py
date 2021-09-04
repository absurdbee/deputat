from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from rest_framework.response import Response
from users.models import User
from district.models import District2
from common.utils import get_location
from datetime import date, datetime
from django.utils import timezone


def is_child(year, month, day):
    today = date.today()
    old = today.year - year - ((today.month, today.day) < (month, day))
    return int(old) < 18

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    area = serializers.CharField(required=False, write_only=True)
    gender = serializers.CharField(required=True, write_only=True)
    date_day = serializers.CharField(required=True, write_only=True)
    date_month = serializers.CharField(required=True, write_only=True)
    date_year = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    "A user is already registered with this e-mail address.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Пароль 1 и пароль 2 не совпадают")
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        users_count = User.objects.only("pk").count()

        self.cleaned_data = self.get_cleaned_data()
        user.phone = users_count + 15600
        area_pk = self.validated_data.get('area', '')
        if area_pk:
            user.area = District2.objects.get(pk=area_pk)
        user.gender = self.validated_data.get('gender', '')

        self.date_day = int(self.validated_data.get('date_day', ''))
        self.date_month = int(self.validated_data.get('date_month', ''))
        self.date_year = int(self.validated_data.get('date_year', ''))
        if is_child(self.date_year, self.date_month, self.date_day):
            raise serializers.ValidationError("Детям регистрация не разрешена!")
        birthday = str(self.date_day) + "/" + str(self.date_month) + "/" + str(self.date_year)
        birthday = datetime.strptime(birthday, '%d/%m/%Y')
        user.birthday = birthday

        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        get_location(request, user)
        return user
