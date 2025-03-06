import os
import shutil
from werkzeug.utils import secure_filename
from app.config import Config


class FileUtils:
    """
    文件处理工具类，提供常见的文件操作方法
    """

    @staticmethod
    def allowed_file(filename):
        """
        检查文件名是否符合允许的扩展名
        :param filename: 文件名
        :return: 是否符合扩展名
        """
        allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def save_file(file, folder_path):
        """
        保存上传的文件到指定文件夹
        :param file: 文件对象
        :param folder_path: 保存文件的文件夹路径
        :return: 文件保存的路径
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # 如果文件夹不存在，则创建文件夹

        if file and FileUtils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(folder_path, filename)
            file.save(file_path)
            return file_path
        else:
            raise ValueError("File extension not allowed.")

    @staticmethod
    def delete_file(file_path):
        """
        删除指定的文件
        :param file_path: 要删除的文件路径
        :return: 是否成功删除
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                raise FileNotFoundError(f"File {file_path} not found.")
        except Exception as e:
            raise Exception(f"Error deleting file: {e}")

    @staticmethod
    def rename_file(old_file_path, new_file_name):
        """
        重命名文件
        :param old_file_path: 原文件路径
        :param new_file_name: 新的文件名
        :return: 新的文件路径
        """
        try:
            if os.path.exists(old_file_path):
                file_extension = os.path.splitext(old_file_path)[1]  # 获取文件扩展名
                new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name + file_extension)
                os.rename(old_file_path, new_file_path)
                return new_file_path
            else:
                raise FileNotFoundError(f"File {old_file_path} not found.")
        except Exception as e:
            raise Exception(f"Error renaming file: {e}")

    @staticmethod
    def move_file(source_path, destination_path):
        """
        移动文件到新的目录
        :param source_path: 源文件路径
        :param destination_path: 目标文件路径
        :return: 是否成功移动
        """
        try:
            if os.path.exists(source_path):
                shutil.move(source_path, destination_path)
                return destination_path
            else:
                raise FileNotFoundError(f"File {source_path} not found.")
        except Exception as e:
            raise Exception(f"Error moving file: {e}")

    @staticmethod
    def get_file_size(file_path):
        """
        获取文件大小
        :param file_path: 文件路径
        :return: 文件大小（字节）
        """
        try:
            if os.path.exists(file_path):
                return os.path.getsize(file_path)
            else:
                raise FileNotFoundError(f"File {file_path} not found.")
        except Exception as e:
            raise Exception(f"Error getting file size: {e}")

    @staticmethod
    def file_exists(file_path):
        """
        检查文件是否存在
        :param file_path: 文件路径
        :return: 是否存在
        """
        return os.path.exists(file_path)

    @staticmethod
    def create_directory(directory_path):
        """
        创建目录（如果目录不存在）
        :param directory_path: 目录路径
        :return: 是否成功创建目录
        """
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"Error creating directory: {e}")
