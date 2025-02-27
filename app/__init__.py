from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.services.rabbitmq_service import start_consumer_thread
from config import Config
from app.utils.error_handler import register_error_handlers  # 引入异常处理函数
from flask_marshmallow import Marshmallow  # 引入 Marshmallow

# 初始化 Flask 应用
app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db = SQLAlchemy(app)

# 初始化 Flask-Marshmallow
ma = Marshmallow(app)

# 初始化 API
api = Api(app)

# 注册全局异常捕获器
register_error_handlers(app)

# # 启动 RabbitMQ 消费者线程
# def start_rabbitmq_consumer():
#     rabbitmq_service.start_listener_thread()  # 启动消费者线程
#     print("RabbitMQ consumer thread is ready.")
#
# # 启动消费者线程
# start_rabbitmq_consumer()
start_consumer_thread()
# 导入路由配置
from app.resources.urls import *
