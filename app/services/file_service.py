from app.logger import get_logger
import os

from app.utils.trie import keyword_to_primary, trie
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
    遍历 YAML 规则构造的 Trie，如果文件名中包含某个二级标签，
    则记录该标签及其在文件名中的出现位置（进行归一化：去除空格、转换为小写）。
    将匹配到的关键词按一级标签进行分组：
      - 每个一级标签只显示一次
      - 对应的二级标签按照文件名中首次出现顺序排列（如果二级标签与一级标签相同则不重复显示）
    最后，将各组结果以分号分隔返回，例如：
      "失效, 跳水, 问题; 培训, 课件"
    如果处理过程中出现错误，则返回空字符串。
    """
    try:
        # 在文件名中搜索所有匹配的关键词，返回 (index, keyword) 列表
        matches = trie.search_in_text(path)
        if not matches:
            return ""
        # 记录每个匹配的关键词及其归一化后的结果
        occurrences = []
        for index, keyword in matches:
            norm_keyword = keyword.strip().lower()  # 归一化
            occurrences.append((index, norm_keyword))
        # 按出现位置排序
        occurrences.sort(key=lambda x: x[0])

        # 根据归一化关键词查找对应的一级标签，并分组存储
        groups = {}  # key: primary, value: list of secondary keywords (按首次出现顺序，不重复)
        for pos, norm_keyword in occurrences:
            # 查找一级标签，注意在构建 keyword_to_primary 时要确保关键词也归一化
            primary = keyword_to_primary.get(norm_keyword, "").strip()
            if primary == "":
                # 如果映射中没有一级标签，则以自身作为一级标签
                primary = norm_keyword
            # 如果该一级标签组不存在，创建一个空列表
            if primary not in groups:
                groups[primary] = []
            # 如果当前关键词尚未加入该组，则添加
            if norm_keyword not in groups[primary]:
                groups[primary].append(norm_keyword)

        # 为了保证整体顺序与文件名中出现顺序一致，我们根据每个一级标签第一次出现的位置进行排序
        primary_order = []
        seen_primary = set()
        for pos, norm_keyword in occurrences:
            primary = keyword_to_primary.get(norm_keyword, "").strip()
            if primary == "":
                primary = norm_keyword
            if primary not in seen_primary:
                seen_primary.add(primary)
                primary_order.append(primary)

        # 构造最终结果字符串：
        # 对于每个一级标签，只输出一次，然后附上该组中不等于一级标签的二级标签
        result_parts = []
        for primary in primary_order:
            secondaries = groups.get(primary, [])
            # 过滤掉与 primary 相同的二级标签（只保留一个 primary）
            group_tags = [primary] + [sec for sec in secondaries if sec != primary]
            result_parts.append(", ".join(group_tags))

        # 如果有多个一级标签组，可以用分号分隔各组结果
        result = "; ".join(result_parts)
        return result
    except Exception as e:
        logger.error(f"错误处理文件 '{path}': {e}")
        return ""


def mark_files(file_list: list) -> list[str]:
    """
    对传入的文件列表进行打标。

    :param file_list: 文件列表，每个元素为字典，至少包含 'path' 和 'dir' 键
    :return: 返回一个打标结果的列表（仅对非目录文件进行打标），顺序与输入顺序一致；
             对于文件夹则返回空字符串。
    """
    results = []
    for file_item in file_list:
        try:
            if not file_item.get("dir", False):
                file_path = file_item.get("path")
                if file_path is None:
                    raise ValueError("path参数没有找到")
                tag_result = mark_file(file_path)
                results.append(tag_result)
            else:
                results.append("")
        except Exception as e:
            logger.error(f"错误处理 {file_item}文件: {e}")
            results.append("")
    return results

