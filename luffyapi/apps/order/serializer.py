'''
 @Description:见字如面 
 @Author: MING
 @Title: 
 @Date: 2022/8/12 9:07
'''
import uuid

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from course.models import Course
from luffyapi.libs.ailipay.pay import alipay
from . import models


class OrderModelSerializer(ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, many=True)

    class Meta:
        model = models.Order
        fields = ['total_amount', 'subject', 'pay_type', 'course']

    def check_price(self, attrs):
        total_amount = attrs.get('total_amount')
        course_list = attrs.get('course')
        course_price = 0
        for course in course_list:
            course_price += course.price
        if total_amount == course_price:
            return total_amount
        else:
            raise ValidationError("订单价格有误重新支付")

    def gen_out_trade_no(self):

        return str(uuid.uuid4())

    def get_user(self):
        # 需要request对象(视图传入request)
        request = self.context.get('request')
        return request.user

    def get_pay_url(self, total_amount, out_trade_no, subject):
        order_string = alipay.api_alipay_trade_page_pay(
            #订单号
            out_trade_no=out_trade_no,
            #价格
            total_amount=float(total_amount),#传入价格是小数点类型，要转成float
            #订单名称
            subject=subject,
            return_url=settings.RETURN_URL,
            notify_url=settings.NOTIFY_URL  # 可选，不填则使用默认 notify url
        )

    def _before_create(self, attrs, user, pay_url,out_trade_no):
        attrs["user"] = user
        attrs["out_trade_no"]=out_trade_no
        self.context["pay_url"] = pay_url

    def validate(self, attrs):
        total_amount = self.check_price(attrs)
        out_trade_no = self.gen_out_trade_no()
        subject = attrs.get('subject')
        user = self.get_user()
        pay_url = self.get_pay_url(total_amount, out_trade_no, subject)
        self._before_create(attrs, user, pay_url,out_trade_no)
        return attrs

    def create(self, validated_data):
        course_list = validated_data.pop('course')
        order = models.Order.objects.create(**validated_data)
        for course in course_list:
            models.OrderDetail.objects.create(course=course, price=course.price, order=order, real_price=course.price)
        return order
