import logging
from logging.handlers import RotatingFileHandler
import os

# 创建日志目录
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 设置日志文件路径
LOG_FILE = os.path.join(LOG_DIR, 'file_processing.log')

# 设置日志格式
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 创建 RotatingFileHandler，最大文件大小10MB，保留3个备份
handler = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=3)

# 设置日志级别为 DEBUG
handler.setLevel(logging.INFO)

# 设置日志格式
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

# 获取日志记录器
logger = logging.getLogger('file_processing_logger')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def get_logger():
    return logger
