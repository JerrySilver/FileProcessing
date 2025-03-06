import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # 配置上传的文件夹路径
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大文件大小 16 MB

    # MySQL 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Repeatlink@localhost:3306/<database>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'  # 用于 session 和 cookie 加密

    # RabbitMQ 配置
    RABBITMQ_HOST = 'localhost'  # RabbitMQ 服务地址
    RABBITMQ_QUEUE = 'file_task_queue_durable_test02'  # 队列名称
    RABBITMQ_USER = 'admin'  # 默认用户
    RABBITMQ_PASSWORD = 'admin'  # 默认密码



