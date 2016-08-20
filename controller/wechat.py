from flask import Blueprint, request, render_template
import json
from tools.wechat_tools import wechat_tools
from model.model import *
from app_config import db
import xmltodict
from tools.wechat_message_handler import *
from app_config import wechat

wechat_bp = Blueprint('wechat', __name__)

session_event_handler = {}


@wechat_bp.route('/main/', methods=['GET', 'POST'])
def main():
    echostr = request.values.get('echostr')
    if not wechat.check_signature(request.values.get('signature'), request.values.get('timestamp'),
                                  request.values.get('nonce')):
        return
    if echostr:
        return echostr
    wechat.parse_data(request.data.decode())
    event = wechat.message.type
    if event == 'text':
        return receive_message_handler()
    elif event == "click":
        return click_event_handler()
    return 'success'


@wechat_bp.route('/register/')
def register():
    code = request.values.get('code')
    open_ID = wechat_tools.get_openID_by_code(code)
    user = user_account.query.filter_by(open_ID=open_ID).first()
    if user:
        return '''
        <script>
                alert('您已注册')
        </script>
        '''
    return render_template('register.html', open_ID=open_ID)


@wechat_bp.route('/check_register/', methods=['GET', 'POST'])
def check_register():
    phone = request.values.get('phone')
    password = request.values.get('password')
    open_ID = request.values.get('open_ID')
    db.session.add(user_account(open_ID, phone, password))
    db.session.commit()
    return 'success'


def receive_message_handler():
    user_ID = wechat.message.source
    if wechat.message.content == '取消':
        if session_event_handler.get(user_ID):
            del session_event_handler[user_ID]
        clear_temp(user_ID)
        return wechat.response_text('请重新操作')
    if session_event_handler.get(user_ID):
        user_content = wechat.message.content
        function = session_event_handler.get(user_ID)
        response_text = function(user_content, user_ID=user_ID, handler=session_event_handler)
        if response_text:
            return wechat.response_text(response_text)
    else:
        return wechat.response_text("hi朋友你好啊")


def click_event_handler():
    event_key = wechat.message.key
    if event_key == 'torrentkitty':
        session_event_handler[wechat.message.source] = torrentkitty_search_by_keyword
        return wechat.response_text("请输入关键词")
    elif event_key == 'zimuzu':
        pass
