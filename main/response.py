#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from main import app
#from .models import set_user_info, get_user_student_info, get_user_library_info
from .utils import AESCipher, init_wechat_sdk


def wechat_response(data):
    """微信消息处理回复"""
    global message, openid, wechat

    wechat = init_wechat_sdk()
    wechat.parse_data(data)
    message = wechat.get_message()
    openid = message.source
    # 用户信息写入数据库
    #set_user_info(openid)

    try:
        get_resp_func = msg_type_resp[message.type]
        response = get_resp_func()
    except KeyError:
        # 默认回复微信消息
        response = 'success'

    # 保存最后一次交互的时间
    set_user_last_interact_time(openid, message.time)
    return response

# 储存微信消息类型所对应函数（方法）的字典
msg_type_resp = {}


def set_msg_type(msg_type):
    """
    储存微信消息类型所对应函数（方法）的装饰器
    """
    def decorator(func):
        msg_type_resp[msg_type] = func
        return func
    return decorator


@set_msg_type('text')
def text_resp():
    """文本类型回复"""
    # 默认回复微信消息
    response = 'success'
    # 替换全角空格为半角空格
    message.content = message.content.replace(u'　', ' ')
    # 清除行首空格
    message.content = message.content.lstrip()
    # 指令列表
    commands = {
        u'取消': cancel_command,
        u'^\?|^？': all_command,
        u'^wifi|^WIFI|^配置': printer_airkiss_command,

        u'^绑定|^綁定': auth_url,
        u'更新菜单': update_menu_setting
    }
    # 状态列表
    state_commands = {
        'chat': chat_robot,
        'express': express_shipment_tracking
    }
    # 匹配指令
    command_match = False
    for key_word in commands:
        if re.match(key_word, message.content):
            # 指令匹配后，设置默认状态
            set_user_state(openid, 'default')
            response = commands[key_word]()
            command_match = True
            break
    if not command_match:
        # 匹配状态
        state = get_user_state(openid)
        # 关键词、状态都不匹配，缺省回复
        if state == 'default' or not state:
            response = command_not_found()
        else:
            response = state_commands[state]()
    return response


@set_msg_type('click')
def click_resp():
    """菜单点击类型回复"""
    commands = {
        'phone_number': phone_number,
        'express': enter_express_state,
        'score': exam_grade,
        'borrowing_record': borrowing_record,
        'renew_books': renew_books,
        'sign': daily_sign,
        'chat_robot': enter_chat_state,
        'music': play_music,
        'weather': get_weather_news
    }
    # 匹配指令后，重置状态
    set_user_state(openid, 'default')
    response = commands[message.key]()
    return response


@set_msg_type('scancode_waitmsg')
def scancode_waitmsg_resp():
    """扫码类型回复"""
    set_user_state(openid, 'express')
    response = express_shipment_tracking()
    return response


@set_msg_type('subscribe')
def subscribe_resp():
    """订阅类型回复"""
    set_user_state(openid, 'default')
    response = subscribe()
    return response


def borrowing_record():
    """查询借书记录"""
    return library_check_auth(u'查询中……')


def renew_books():
    """续借图书"""
    return library_check_auth(u'续借中……', renew=True)

def search_books():
    """图书馆找书"""
    content = app.config['LIBRARY_TEXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)



def auth_url():
    """教务系统、图书馆绑定的 URL"""
    jw_url = app.config['HOST_URL'] + '/auth-score/' + openid
    library_url = app.config['HOST_URL'] + '/auth-library/' + openid
    content = app.config['AUTH_TEXT'] % (jw_url, library_url)
    return wechat.response_text(content)


def get_school_news():
    """读取学院新闻"""
    school_news.get.delay(openid)
    return 'success'


def get_weather_news():
    """获取天气预报"""
    weather.get.delay(openid)
    return 'success'


def update_menu_setting():
    """更新自定义菜单"""
    try:
        wechat.create_menu(app.config['MENU_SETTING'])
    except Exception as e:
        return wechat.response_text(e)
    else:
        return wechat.response_text('Done!')


def developing():
    """维护公告"""
    return wechat.response_text('该功能维护中')


def enter_express_state():
    """进入快递查询模式"""
    set_user_state(openid, 'express')
    return wechat.response_text(app.config['ENTER_EXPRESS_STATE_TEXT'])


def cancel_command():
    """取消状态"""
    content = app.config['CANCEL_COMMAND_TEXT'] + app.config['COMMAND_TEXT']
    return wechat.response_text(content)


def enter_chat_state():
    """进入聊天模式"""
    set_user_state(openid, 'chat')
    return wechat.response_text(app.config['ENTER_CHAT_STATE_TEXT'])


def cet_score():
    """回复四六级查询网址"""
    content = app.config['CET_SCORE_TEXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)


def postcard():
    """明信片查询"""
    content = app.config['POSTCARD_TEXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)


def html5_games():
    """HTML5游戏"""
    content = app.config['HTML5_GAMES_TEXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)


def contact_us():
    """合作信息"""
    content = app.config['CONTACT_US_TEXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)


def academic_calendar():
    """校历"""
    return wechat.response_news(app.config['ACADEMIC_CALENDAR_NEWS'])


def bbs_url():
    """论坛网址"""
    content = app.config['BBS_URL_TXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)


def bus_routes():
    """公交信息"""
    return wechat.response_news(app.config['BUS_ROUTES_NEWS'])


def weather_radar():
    """气象雷达动态图"""
    content = app.config['WEATHER_RADAR_TEXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)


def command_not_found():
    """非关键词回复"""
    # 客服接口回复信息
    content = app.config['COMMAND_NOT_FOUND_TEXT'] + app.config['HELP_TEXT']
    wechat_custom.send_text(openid, content)
    # 转发消息到微信多客服系统
    return wechat.group_transfer_message()


def all_command():
    """回复全部指令"""
    content = app.config['COMMAND_TEXT']
    return wechat.response_text(content)


def subscribe():
    """回复订阅事件"""
    content = app.config['WELCOME_TEXT'] + app.config['COMMAND_TEXT']
    return wechat.response_text(content)


def phone_number():
    """回复电话号码"""
    content = app.config['PHONE_NUMBER_TEXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)

def printer_airkiss_command():
    """代开airkiss 页面"""
    airkissURL = app.config['HOST_URL']+"/wechat/printer/airkiss"
    content = app.config['AIRKISS_URL_TXT'].fromat(airkissURL)
    return wechat.response_text(content)

if __name__ == '__main__':
    import sys;
    file = open(sys.argv[1],'r')
    data = file.read()
    print(data)
    wechat_response(data)
