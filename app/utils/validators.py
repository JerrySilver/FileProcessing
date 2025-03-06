import os
import re
from werkzeug.exceptions import BadRequest

from app.logger import logger


class Validators:
    """
    验证工具类，提供常见的验证方法
    """

    @staticmethod
    def is_email_valid(email):
        """
        验证邮箱格式是否有效
        :param email: 电子邮件地址
        :return: 如果有效则返回 True，否则抛出 BadRequest 异常
        """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_regex, email):
            return True
        else:
            raise BadRequest("Invalid email format")

    @staticmethod
    def is_password_valid(password):
        """
        验证密码的强度，要求密码至少有8个字符，包含大写字母、小写字母、数字和特殊字符
        :param password: 用户输入的密码
        :return: 如果密码有效则返回 True，否则抛出 BadRequest 异常
        """
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[A-Z])(?=.*[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~])(?=.{8,})'
        if re.match(password_regex, password):
            return True
        else:
            raise BadRequest("Password must be at least 8 characters long, and include upper/lowercase letters, numbers, and special characters")

    @staticmethod
    def is_phone_number_valid(phone_number):
        """
        验证电话号码是否有效，假设手机号格式是类似于 +1 (555) 555-5555
        :param phone_number: 电话号码
        :return: 如果电话号码有效则返回 True，否则抛出 BadRequest 异常
        """
        phone_number_regex = r'^\+?(\d{1,2})?(\(\d{3}\))?[\s\-]?\d{3}[\s\-]?\d{4}$'
        if re.match(phone_number_regex, phone_number):
            return True
        else:
            raise BadRequest("Invalid phone number format")

    @staticmethod
    def is_username_valid(username):
        """
        验证用户名是否有效，用户名必须包含字母或数字，且长度在4到20个字符之间
        :param username: 用户名
        :return: 如果用户名有效则返回 True，否则抛出 BadRequest 异常
        """
        if 4 <= len(username) <= 20 and username.isalnum():
            return True
        else:
            raise BadRequest("Username must be between 4 to 20 characters and only contain letters and numbers")

    @staticmethod
    def is_file_extension_valid(filename, allowed_extensions=None):
        """
        验证文件扩展名是否有效，文件扩展名可以通过 allowed_extensions 参数进行自定义
        :param filename: 文件名
        :param allowed_extensions: 允许的扩展名列表
        :return: 如果文件扩展名有效则返回 True，否则抛出 BadRequest 异常
        """
        if allowed_extensions is None:
            allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','java','python'}

        if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions:
            return True
        else:
            raise BadRequest("Invalid file extension")

    @staticmethod
    def are_files_in_folder_valid(folder_path, allowed_extensions=None):
        """
        验证文件夹中的所有文件是否合规（即每个文件的扩展名是否有效）。
        :param folder_path: 文件夹路径
        :param allowed_extensions: 允许的文件扩展名列表
        :return: 如果所有文件合规则返回 True，否则返回包含错误信息的列表
        """
        invalid_files = []  # 用来存储不合规的文件

        try:
            # 获取文件夹中的所有文件
            files = os.listdir(folder_path)
            # 排除非文件（如子文件夹）
            files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]
            # 验证每个文件的扩展名
            for file in files:
                try:
                    if not Validators.is_file_extension_valid(file, allowed_extensions):
                        invalid_files.append(file)
                except BadRequest:
                    # 捕捉到扩展名无效时的异常，不做中断处理
                    invalid_files.append(file)
            if invalid_files:
                return False  # 返回不合规的文件名列表
            return True

        except Exception as e:
            logger.error(f"Error accessing folder: {e}")
            return False, str(e)

    @staticmethod
    def is_required_field(value, field_name):
        """
        验证字段是否为必填项，如果为空则抛出异常
        :param value: 字段的值
        :param field_name: 字段的名称
        :return: 如果字段有效则返回 True，否则抛出 BadRequest 异常
        """
        if not value:
            raise BadRequest(f"{field_name} is required")
        return True

    @staticmethod
    def is_range_valid(value, min_value, max_value, field_name):
        """
        验证数值是否在指定的范围内
        :param value: 字段的值
        :param min_value: 最小值
        :param max_value: 最大值
        :param field_name: 字段的名称
        :return: 如果值在指定范围内返回 True，否则抛出 BadRequest 异常
        """
        if not (min_value <= value <= max_value):
            raise BadRequest(f"{field_name} must be between {min_value} and {max_value}")
        return True
