from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from secret_config import db_url, port, appid, appsecret
from wechat_sdk import *

app = Flask(__name__)

app.secret_key = 'A0Zr98jnjj/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['app_id'] = appid
app.config['app_secret'] = appsecret
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ALLOW_FILE'] = ['jpg', 'jpeg', 'gif', 'png', 'bmp']
db = SQLAlchemy(app)


conf = WechatConf(app_ID='wxd39fc293152eaaf0', appsecret='7dbe721d3175de1bb6b5468ab14ec997',
                  token='token', encrypt_mode='normal')
wechat = WechatBasic(conf=conf)