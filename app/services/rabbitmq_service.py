import pika
import uuid
from app.config import Config
from app.logger import get_logger

# 获取日志记录器
logger = get_logger()

class RabbitMQServiceRPC:
    def __init__(self):
        self.connection_params = pika.ConnectionParameters(
            host=Config.RABBITMQ_HOST,
            credentials=pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD)
        )
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()
        # 声明一个临时回调队列，exclusive=True 表示队列在连接断开时自动删除
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message: str, timeout: int = 10) -> str:
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=Config.RABBITMQ_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                delivery_mode=2  # 消息持久化
            ),
            body=message
        )
        logger.info(f"向RPC发送信息: {message} with correlation_id: {self.corr_id}")

        # 等待响应，超时则抛出异常
        import time
        start_time = time.time()
        while self.response is None:
            self.connection.process_data_events()
            if time.time() - start_time > timeout:
                logger.error("RPC 请求超时")
                raise TimeoutError("RPC 请求超时")
        return self.response.decode('utf-8')


# 创建全局 RPC 实例
rabbitmq_rpc = RabbitMQServiceRPC()
