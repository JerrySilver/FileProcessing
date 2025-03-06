from app.logger import get_logger
import os
from app.utils.yaml_loader import tag_data

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


def mark_file(path: str) -> str:
    """
    对单个文件名进行打标：
    遍历 YAML 规则，如果文件名中包含某个二级标签，
    则记录该标签在文件路径中的首次出现位置，
    最后按出现位置排序并返回去重后的二级标签列表，
    用逗号分隔。如果处理过程中出现错误，则返回空字符串。
    """
    try:
        matches = []
        # 遍历所有一级标签下的二级标签
        for primary, secondary_list in tag_data.items():
            if secondary_list:
                for secondary in secondary_list:
                    idx = path.find(secondary)
                    if idx != -1:
                        matches.append((idx, secondary))
        # 如果没有匹配项，直接返回空字符串
        if not matches:
            return ""
        # 对同一二级标签，只保留首次出现的位置（最小的 idx）
        unique_matches = {}
        for idx, sec in matches:
            if sec not in unique_matches or idx < unique_matches[sec]:
                unique_matches[sec] = idx
        # 将匹配结果按出现位置排序
        sorted_matches = sorted(unique_matches.items(), key=lambda x: x[1])
        result = ", ".join([sec for sec, idx in sorted_matches])
        return result
    except Exception as e:
        logger.error(f"Error processing file '{path}': {e}")
        return ""


def mark_files(file_list: list) -> list[str]:
    """
    对传入的文件列表进行打标。

    :param file_list: 文件列表，每个元素为字典，至少包含 'path' 和 'dir' 键。
    :return: 返回一个打标结果的列表（仅对非目录文件进行打标），若出现错误，则相应位置返回空字符串。
    """
    results = []
    for file_item in file_list:
        try:
            # 如果不是文件夹，则进行打标
            if not file_item.get('dir', False):
                file_path = file_item.get('path')
                if file_path is None:
                    raise ValueError("Missing 'path' in file item")
                tag_result = mark_file(file_path)
                results.append(tag_result)
            else:
                # 如果是文件夹，则不打标，返回空字符串或其他默认值
                results.append("")
        except Exception as e:
            logger.error(f"Error processing file item {file_item}: {e}")
            results.append("")
    return results
