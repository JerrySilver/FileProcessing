import threading

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from app.services.rabbitmq_rpc_server import start_rpc_server  # 导入RPC消费者启动函数
from config import Config
from app.utils.error_handler import register_error_handlers  # 引入异常处理函数
from flask_marshmallow import Marshmallow  # 引入 Marshmallow
from app.logger import get_logger

# 获取日志记录器
logger = get_logger()

# 初始化 Flask 应用
app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db = SQLAlchemy(app)

# 初始化 Flask-Marshmallow
ma = Marshmallow(app)

# 初始化 API
api = Api(app)

# 启动 RabbitMQ RPC 消费者线程
def start_rabbitmq_rpc_consumer():
    consumer_thread = threading.Thread(target=start_rpc_server, daemon=True)
    consumer_thread.start()
    logger.info("RabbitMQ RPC 消费者线程已启动.")
    # print("RabbitMQ RPC 消费者线程已启动.")

start_rabbitmq_rpc_consumer()
# 注册全局异常捕获器
register_error_handlers(app)

# 导入路由配置
from app.resources.urls import *
