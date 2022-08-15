# Create your views here.
import logging

from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from libs.ailipay import alipay
from utils.logger import log
from . import models
from . import serializer
from rest_framework.views import APIView


class PayView(GenericViewSet, CreateModelMixin):
    # 配套使用认证
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = models.Order.objects.all()
    serializer_class = serializer.OrderModelSerializer

    # 重写create让序列化类拿到request
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.context.get('pay_url'))
class SuccessView(APIView):
    def get(self,request,*args,**kwargs):
        out_trade_no =request.Get.get("out_trade_no")
        order=models.Order.objects.filter(out_trade_no=out_trade_no).first()
        if order.order_status==1:
            return Response("Success")
        else:
            return Response("failed")
    def post(self,request,*args,**kwargs):
        """
        支付宝回调
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # for django users
        data = request.dict()
        # for rest_framework users
        data = request.data
        out_trade_no=data.get('out_trade_no',None)
        gmt_payment=data.get("gmt_payment")
        signature = data.pop("sign")


        #验证签名
        success = alipay.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            models.Order.objects.filter(out_trade_no=out_trade_no).update(order_status=1,pay_time=gmt_payment)
            log.info("%s支付成功"%out_trade_no)
            return Response('success')
        else:
            log.error("%s订单出错"%out_trade_no)
            return Response('error')