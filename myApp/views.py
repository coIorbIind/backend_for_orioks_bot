from django.contrib.auth.models import User
from django.core.files import File
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from . models import Profile
from . serializers import *
from . services import *


class GetMarksView(APIView):

    def get(self, *args, **kwargs):
        username = self.request.query_params.get('telegram_username')
        try:
            user = Profile.objects.get(telegram_username=username)
        except Profile.DoesNotExist:
            return Response({'msg': 'Профиль не найден'})
        res = get_marks(user)
        if res.get("msg") == "Error":
            return Response({'msg': "Что-то пошло не так"})

        user.marks = json.dumps(res.get("marks"), ensure_ascii=False)

        user.save()
        serialized_user = ProfileMarksSerializer(user, many=False)
        return Response(serialized_user.data)


class CheckMarksView(APIView):

    def get(self, *args, **kwargs):
        username = self.request.query_params.get('telegram_username')
        try:
            user = Profile.objects.get(telegram_username=username)
        except Profile.DoesNotExist:
            return Response({'msg': 'Профиль не найден'})
        res = check_marks(user)
        if res.get("msg") == "Error":
            return Response({'msg': "Что-то пошло не так"})

        if res.get("changes"):
            user.marks = json.dumps(res.get("marks"), ensure_ascii=False)
            user.save()
            return Response({'msg': res.get("changes")})

        return Response({'msg': "Изменения не найдены"})


class CreateUserView(APIView):

    def post(self, *args, **kwargs):
        post_data = self.request.data
        username = post_data.get('username')
        telegram_username = post_data.get('telegram_username')
        password = post_data.get('password')
        user = User(username=username, password=password)
        try:
            user.save()   # can be exception
            profile = Profile(user=user, telegram_username=telegram_username)

            # here will be commands for saving cookies
            cookies_dict = get_cookies(profile)
            if cookies_dict.get("msg") == "Success":
                profile.cookies = cookies_dict.get("cookies")

            profile.save()
        except IntegrityError:
            return Response({'msg': "Пользователь с таким именем уже существует"})
        return Response({'msg': f"Пользователь успешно создан. Сообщение о печеньках {cookies_dict.get('msg')}"})
