#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from models import *
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import json
from wechat_sdk.basic import WechatBasic
from wechat_sdk.lib import XMLStore

from private_settings import *
# Create your views here.

# 测试账号，获得各种权限

wechat = WechatBasic(token=token, appid=appid, appsecret=appsecret)


def get_all_user(request):
        users_data = wechat.get_followers()
        for open_id in users_data['data']['openid']:
            print open_id
            cur_user_info = wechat.get_user_info(open_id)
            print cur_user_info
            cur_username = cur_user_info['nickname']
            cur_group_id = cur_user_info['groupid']
            cur_simpleuser = SimpleUser(
                name = cur_username,
                open_id=open_id,
                group=cur_group_id,
                )
            cur_simpleuser.save()
        return HttpResponse(json.dumps(users_data, ensure_ascii=False), content_type='application/json')


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
    menu_data = {
        "button": [
            {
                "name": "产品简介",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "产品作用",
                        "url": "http://www.example.com/function/"
                    },
                    {
                        "type": "view",
                        "name": "产品图片",
                        "url": "http://www.example.com/picture/"
                    },
                    {
                        "type": "view",
                        "name": "价格展示",
                        "url": "http://www.example.com/show_price/"
                    }]
            },
            {
                "type": "view",
                "name": "案例",
                "url": "http://www.example.com/example/"
            },
            {
                "type": "view",
                "name": "商城",
                "url": "http://www.example.com"
            }]
    }
    wechat.create_menu(menu_data)
    return HttpResponse(json.dumps(wechat.get_menu(), ensure_ascii=False), content_type='application/json')


def init_check(request):
    signature = request.GET.get('signature')  # Request 中 GET 参数 signature
    timestamp = request.GET.get('timestamp')  # Request 中 GET 参数 timestamp
    nonce = request.GET.get('nonce')
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return HttpResponse(request.GET.get('echostr'))
    else:
        return None

@csrf_exempt
def index(request):
    if request.method == 'POST':
        body_text = request.body
        wechat.parse_data(body_text)
        openid = get_openid(body_text)
        message = wechat.get_message()
        response = None
        if message.type == 'text':
            if message.content == u'关于我们':
                response = wechat.response_news([
                    {
                        'title': u'【有人@你】2016年，它能让你投资健康！',
                        'description': u'21世纪，电磁波辐射无处不在，更成为影响人们健康的“头号隐形杀手”。',
                        'picurl': 'https://mmbiz.qlogo.cn/mmbiz/nTPviaiaCpUNgSF6trK1Rm8J5cojYDN6vKpXcQDG6wRMTW4ALWqzWyMI24h2XkwqKrAU9gEqsClHMAXTvYmZ6nvg/0?wx_fmt=png',
                        'url': u'http://mp.weixin.qq.com/s?__biz=MzA5MTc2OTA1NA==&mid=401003680&idx=1&sn=ea02432620669c202a2de3193bcb7e59&scene=20#rd',
                    }
                ])
            elif message.content == u'商业合作':
                resp_text = '''
欢迎加盟我公司，期待与您的合作！
公司信息：湖北伟润网络科技有限公司

——美国品牌Q-Link抗辐射智能穿戴系列产品湖北地区总代理。


商业合作联系方式：

E-mail:hbwrwl2015@163.com

Tel:13908689118 张先生
                '''
                response = wechat.response_text(resp_text)
            else:
                resp_text = '''
您好，感谢关注科灵可礼品汇！
清新无辐射，关爱您和您的家人！
如需了解我公司及产品，请回复关键词“关于我们”，即可获得详细介绍。
如需进行商业合作，请回复关键词“商业合作”，即可获取相关信息。
如有相关问题请留言，我们稍后会为您详细解答。
                    '''
                response = wechat.response_text(resp_text)
        elif message.type == 'image':
            response = wechat.response_text(u'图片')
        elif message.type == 'subscribe':
            resp_text = '''
您好，感谢关注科灵可礼品汇！
清新无辐射，关爱您和您的家人！
如需了解我公司及产品，请回复关键词“关于我们”，即可获得详细介绍。
如需进行商业合作，请回复关键词“商业合作”，即可获取相关信息。
                '''
            response = wechat.response_text(resp_text)
        else:
            response = wechat.response_text(u'未知')
        return HttpResponse(response, content_type="application/xml")

    else:
        if request.GET:
            return init_check(request)
        else:
            return HttpResponse('index')