import pika
import json
from app.config import Config
from app.logger import get_logger
from app.services.file_service import mark_files  # 实现打标逻辑
# 获取日志记录器
logger = get_logger()

def on_request(ch, method, properties, body):
    try:
        message = json.loads(body.decode('utf-8'))
        task_type = message.get("task_type")
        if task_type == "mark_files":
            file_list = message.get("fileModelList")
            # 调用打标函数，得到打标结果列表
            marking_results = mark_files(file_list)
            # 构造结果数据：假设返回一个列表，其中每个元素包含文件 ID 和打标结果
            result = []
            if len(marking_results) != len(file_list):
                result = {"error": "打标结果数量不匹配"}
            else:
                for idx, file_item in enumerate(file_list):
                    result.append({"neid": file_item.get("neid"), "tag": marking_results[idx]})
            response = json.dumps(result)
        else:
            response = json.dumps({"error": "未知任务类型"})
    except Exception as e:
        logger.error(f"错误处理 RPC 请求: {e}")
        response = json.dumps({"error": str(e)})

    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_rpc_server():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=Config.RABBITMQ_HOST,
        credentials=pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD)
    ))
    channel = connection.channel()
    channel.queue_declare(queue=Config.RABBITMQ_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=Config.RABBITMQ_QUEUE, on_message_callback=on_request)
    logger.info("消费者服务正在等待消息")
    channel.start_consuming()

if __name__ == "__main__":
    start_rpc_server()
