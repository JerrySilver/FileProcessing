# app/services/rabbitmq_service.py
import os
import threading
import uuid

import pika
import json
from app.services.file_service import rename_files_in_folder
from app.config import Config
from app.logger import get_logger

# 获取日志记录器
logger = get_logger()

# 使用配置文件中的 RabbitMQ 信息
RABBITMQ_HOST = Config.RABBITMQ_HOST
RABBITMQ_QUEUE = Config.RABBITMQ_QUEUE
RABBITMQ_USER = Config.RABBITMQ_USER
RABBITMQ_PASSWORD = Config.RABBITMQ_PASSWORD

def send_to_rabbitmq(file_path, task_type):
    """
    将任务发送到 RabbitMQ 队列
    :param file_path: 文件路径
    :param task_type: 任务类型
    """
    task_id = str(uuid.uuid4())  # 生成唯一的 task_id
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=Config.RABBITMQ_HOST,
            credentials=pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD)
        ))
        channel = connection.channel()

        # 确保队列存在
        channel.queue_declare(queue=Config.RABBITMQ_QUEUE)

        task = {
            'file_path': file_path,
            'task_type': task_type,
            'task_id': task_id  # 传递 task_id
        }

        # 发布消息
        channel.basic_publish(
            exchange='',
            routing_key=Config.RABBITMQ_QUEUE,
            body=json.dumps(task)
        )

        logger.info(f"Sent task to RabbitMQ: {task}")

        connection.close()

        return task_id  # 返回 task_id，以便前端使用

    except Exception as e:
        logger.error(f"Error sending task to RabbitMQ: {e}")
        raise

def validate_folder_path(folder_path):
    """
    检查文件夹路径是否存在
    :param folder_path: 文件夹路径
    :return: 如果文件夹存在则返回 True，否则返回 False
    """
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        return True
    else:
        logger.error(f"Folder not found or is not a directory: {folder_path}")
        return False


def start_consuming():
    """
    启动 RabbitMQ 消费者，监听队列并处理任务
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=Config.RABBITMQ_HOST,
            credentials=pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD)
        ))
        channel = connection.channel()

        # 声明队列
        channel.queue_declare(queue=Config.RABBITMQ_QUEUE, durable=False)

        # 消费任务的回调函数
        def callback(ch, method, properties, body):
            try:
                task = json.loads(body)
                folder_path = task.get('file_path')  # 获取任务中的文件夹路径
                task_type = task.get('task_type')    # 获取任务类型
                task_id = task.get('task_id')        # 获取任务 ID

                if folder_path:
                    logger.info(f"Processing task {task_id} of type {task_type} for folder: {folder_path}")
                    result = rename_files_in_folder(folder_path)
                    if result.get("status") == "success":
                        logger.info(f"Task {task_id} completed successfully")
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                    else:
                        logger.error(f"Task {task_id} failed for folder: {folder_path}")
                        ch.basic_nack(delivery_tag=method.delivery_tag)  # 任务失败，拒绝消息
                else:
                    logger.error(f"Task {task_id} failed: No folder path found in the task.")
                    ch.basic_nack(delivery_tag=method.delivery_tag)

            except Exception as e:
                logger.error(f"Error processing task: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag)  # 确保即使出现错误也会拒绝消息

        # 设置消费者，监听队列
        channel.basic_consume(queue=Config.RABBITMQ_QUEUE, on_message_callback=callback)
        logger.info('Waiting for tasks. To exit press CTRL+C')
        channel.start_consuming()

    except Exception as e:
        logger.error(f"Error in RabbitMQ consumer: {e}")

def start_consumer_thread():
    """
    启动消费者线程
    """
    consumer_thread = threading.Thread(target=start_consuming)
    consumer_thread.daemon = True  # 设置为守护线程，程序退出时会自动结束
    consumer_thread.start()
    logger.info("Consumer thread started.")