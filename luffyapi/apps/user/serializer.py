import re

from django.conf import settings
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models


class UserSerilaizer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['username', 'password', 'id']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def validate(self, attrs):

        # 多种登录方式
        user = self._get_user(attrs)
        # 签发token
        token = self._get_token(user)
        # 放到context中，我在视图类中可以取出来
        self.context['token'] = token
        self.context['user'] = user

        return attrs

    def _get_user(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        import re
        if re.match('^1[3-9][0-9]{9}$', username):
            user = models.User.objects.filter(telephone=username).first()
        elif re.match('^.+@.+$', username):  # 邮箱
            user = models.User.objects.filter(email=username).first()
        else:
            user = models.User.objects.filter(username=username).first()
        if user:
            ret = user.check_password(password)
            if ret:
                return user
            else:
                raise ValidationError('密码错误')
        else:
            raise ValidationError('用户不存在')

    def _get_token(self, user):
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler(user)  # 通过user对象获得payload
        token = jwt_encode_handler(payload)  # 通过payload获得token
        return token


class CodeUserSerilaizer(serializers.ModelSerializer):
    code = serializers.CharField()

    class META:
        model = models.User
        feilds = ['telephone', 'code']

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(user)
        # 放到context中，我在视图类中可以取出来
        self.context['token'] = token
        self.context['user'] = user
        return attrs

    def _get_user(self, attrs):
        telephone = attrs.get('telephone')
        code = attrs.get('code')
        # 取出原有的code
        cache_code = cache.get(settings.PHONE_CACHE_KEY % telephone)
        if code == cache_code:
            if re.match('^1[3-9][0-9]{9}$', telephone):
                user = models.User.objects.filter(telephone=telephone).first()
                if user:
                    #登录之后验证码直接删除
                    cache.set(settings.PHONE_CACHE_KEY % telephone,'')
                    return user
                raise ValidationError("用户不存在")
        else:
            raise ValidationError('验证码错误')

    def _get_token(self, user):
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler(user)  # 通过user对象获得payload
        token = jwt_encode_handler(payload)  # 通过payload获得token
        return token


class UserRegrsterSerilaizer(serializers.ModelSerializer):
    code=serializers.CharField(max_length=6,min_length=6)
    class Meta:
        model = models.User
        fields = ['telephone', 'password','code']
        extra_kwargs = {
            'password': {'max_length':16,'min_length':16,}
        }
    def validate_password(self, attrs):
        password=attrs.get('password')
        if not re.match('^(?![a-zA-Z]+$)(?!\d+$)(?![^\da-zA-Z\s]+$).{1,16}$',password):
            raise ValidationError("密码必须包含字母或特殊字符")
        return attrs
    def validate(self, attrs):
        telephone=attrs.get('telephone')
        code = attrs.get('code')
        # 取出原有的code
        cache_code = cache.get(settings.PHONE_CACHE_KEY % telephone)
        if code == cache_code:
            if re.match('^1[3-9][0-9]{9}$', telephone):
                attrs["username"]=telephone #设置初始用户名
                return attrs
            else:
                raise ValidationError("手机号码不合法")
        else:
            raise ValidationError("验证码错误")
    #重写create
    def create(self, validated_data):
        validated_data.pop('code')
        user=models.User.objects.create_user(**validated_data)
        return user


