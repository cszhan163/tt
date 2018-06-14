#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, render_template, jsonify, Markup, abort, \
    send_from_directory
from . import app, redis
from .utils import check_signature, get_jsapi_signature_data
from .response import wechat_response
#from .plugins import score, library
#from .models import is_user_exists
import ast


@app.route("/wxcheck", methods=['GET', 'POST'])
@check_signature
def handle_wechat_request():
    """
    处理回复微信请求
    """
    if request.method == 'POST':
        return wechat_response(request.data)
    else:
        # 微信接入验证
        return request.args.get('echostr', '')


@app.route('/wechat/printer/airkiss', methods=['GET'])
def printer_airkiss(openid=None):
    """"""
    if request.method == 'GET':
        print("start airkiss!!"+request.url)
        jsapi = get_jsapi_signature_data(request.url)
        #jsapi['jsApiList'] = ['hideAllNonBaseMenuItem']
        jsapi['jsApiList'] = [
          'checkJsApi',
          'openWXDeviceLib',
          'closeWXDeviceLib',
          'startScanWXDevice',
          'getWXDeviceInfos',
          'connectWXDevice',
          'disconnectWXDevice',
          'configWXDeviceWiFi',
        ]
        jsapi['beta'] = 'true'
        static_full_url = request.host_url +"static"
        print(static_full_url)
        print(jsapi)
        #return render_template('test.html')
        return render_template('printerairkiss.html',
                               title=u'打印机设置',
                               desc=u'设置打印机的wifi连接',
                               static_url=static_full_url,
                               jsapi=Markup(jsapi))
    else:
        abort(404)

@app.route('/robots.txt')
def robots():
    """搜索引擎爬虫协议"""
    return send_from_directory('web', request.path[1:])


@app.errorhandler(404)
def page_not_found(error):
    return "page not found!", 404


@app.errorhandler(Exception)
def unhandled_exception(error):
    app.logger.error('Unhandled Exception: %s', (error))
    return "Error", 500
