import os
from app.logger import get_logger

# 获取日志记录器
logger = get_logger()

def process_file(file_path):
    """处理单个文件"""
    logger.info(f"Processing file: {file_path}")
    # print(f"Processing file: {file_path}")
    return f"Processed {file_path}"

def process_files_in_folder(folder_path):
    """处理文件夹中的所有文件"""
    if not os.path.isdir(folder_path):
        raise ValueError("Invalid folder path")

    processed_files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            result = process_file(file_path)
            processed_files.append(result)

    # 记录处理完成的信息
    logger.info(f"Completed processing files in folder: {folder_path}")
    return processed_files

def process_message(message):
    """处理 RabbitMQ 消息"""
    try:
        folder_path = message.decode('utf-8')  # 解码消息（假设是 UTF-8 编码）
        print(f"Processing folder: {folder_path}")

        # 调用现有的函数来处理文件夹中的文件
        processed_files = process_files_in_folder(folder_path)

        # 返回处理结果
        return processed_files

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return None


def rename_files_in_folder(folder_path):
    """
    将指定文件夹中的所有文件重命名为 1, 2, 3, 4, ... 等等。
    :param folder_path: 文件夹路径
    :return: 返回操作结果信息
    """
    try:
        # 获取文件夹中的所有文件
        files = os.listdir(folder_path)

        # 排除非文件（如子文件夹）
        files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]

        # 按照数字重命名
        for index, file in enumerate(files, start=1):
            # 获取文件的扩展名
            file_extension = os.path.splitext(file)[1]

            # 新文件名
            new_file_name = f"{index}{file_extension}"

            # 获取原文件和新文件的完整路径
            old_file_path = os.path.join(folder_path, file)
            new_file_path = os.path.join(folder_path, new_file_name)

            # 重命名文件
            os.rename(old_file_path, new_file_path)
            logger.info(f"Renamed '{file}' to '{new_file_name}'")

        return {"status": "success", "message": "Files renamed successfully"}

    except Exception as e:
        logger.error(f"Error renaming files: {e}")
        return {"status": "error", "message": str(e)}

def folder_exists(folder_path):
    """
    检查指定的文件夹是否存在。
    :param folder_path: 要检查的文件夹路径
    :return: 如果文件夹存在返回 True，否则返回 False
    """
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        logger.info(f"Folder exists: {folder_path}")
        return True
    else:
        logger.error(f"Folder does not exist: {folder_path}")
        return False