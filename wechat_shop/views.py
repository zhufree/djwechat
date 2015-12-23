#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from models import *
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

import json
from wechat_sdk.basic import WechatBasic
from wechat_sdk.lib import XMLStore

from private_settings import *
# Create your views here.

# 测试账号，获得各种权限

wechat = WechatBasic(token=token,appid=appid,appsecret=appsecret)


def get_all_user(request):
    pass


def get_all_goods(request):
    pass


def add_new_user(request):
    pass


def add_new_good():
    pass


def show_goods():
    pass

# 获取用户的openid，进一步获取其他信息
def get_openid(data):
    if type(data) == unicode:
        data = data.encode('utf-8')
    elif type(data) == str:
        pass

    xml = XMLStore(xmlstring=data)

    result = xml.xml2dict
    openid = result.pop('FromUserName')
    return openid


def set_menu(request):
    menu_data={
        "button":[
        {
            "name":"产品简介",
            "sub_button":[
            {
                "type":"view",
                "name":"产品作用",
                "url":"http://www.example.com/function/"
            },
            {
                "type":"view",
                "name":"产品图片",
                "url":"http://www.example.com/picture/"
            },
            {
                "type":"view",
                "name":"价格展示",
                "url":"http://www.example.com/show_price/"
            }]
        },
        {
            "type":"view",
            "name":"案例",
            "url":"http://www.example.com/example/"
        },
        {
            "type":"view",
            "name":"商城",
            "url":"http://www.example.com"
        }]
        }
    wechat.create_menu(menu_data)
    return HttpResponse(json.dumps(wechat.get_menu(), ensure_ascii=False),content_type='application/json')


@csrf_exempt
def index(request):
    if request.method == 'POST':
        body_text = request.body
        wechat.parse_data(body_text)
        openid = get_openid(body_text)
        message = wechat.get_message()
        response = None
        if message.type == 'text':
            if message.content == u'我的信息':
                wechat.get_access_token()
                userinfo = wechat.get_user_info(openid)
                response = wechat.response_text(userinfo)
        elif message.type == 'image':
            response = wechat.response_text(u'图片')
        else:
            response = wechat.response_text(u'未知')
        return HttpResponse(response, content_type="application/xml")

    else:
        signature = request.GET.get('signature')  # Request 中 GET 参数 signature
        timestamp = request.GET.get('timestamp')  # Request 中 GET 参数 timestamp
        nonce =request.GET.get('nonce')
        if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponse(request.GET.get('echostr'))
