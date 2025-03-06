from flask_restful import Resource
from flask import request

from app.logger import logger
from app.schemas.file_schema import FileListSchema
from app.services.rabbitmq_service import send_to_rabbitmq
from app.utils.response_container import BaseResponse  # 导入统一的响应类
from app.services.file_service import process_files_in_folder, folder_exists
from app.utils.validators import Validators  #验证工具类


class FileResource(Resource):
    def post(self):
        folder_schema = FileListSchema()

        try:
            # 验证并加载请求数据
            data = folder_schema.load(request.json)
        except Exception as e:
            # 使用统一的错误返回格式
            response = BaseResponse(code=400, status=400, message="Invalid input", data={"error": str(e)})
            return response.to_json()

        folder_path = data.get('folder_path')

        # 将任务发送到队列
        try:
            result = process_files_in_folder(folder_path)
        except Exception as e:
            response = BaseResponse(code=500, status=500, message="Error sending message to RabbitMQ",
                                    data={"error": str(e)})
            return response.to_json()

        # 返回任务接收成功的响应
        response = BaseResponse(code=200, status=200, message="文件正在处理中",
                                data={"files_path": result})
        return response.to_json()


class RenameFilesResource(Resource):
    def post(self):
        folder_path = request.json.get('folder_path')

        # 检查文件夹路径是否合法
        if not folder_exists(folder_path) or not folder_path:
            response = BaseResponse(code=400, status=400, message="Invalid input",
                                    data={"error": "Folder path is wrong"})
            return response.to_json()

        if not Validators.are_files_in_folder_valid(folder_path):
            logger.warning(f"路径下文件存在非法扩展名")
            response = BaseResponse(code=400, status=400, message="Invalid input",
                                    data={"error": "非法文件扩展名"})
            return response.to_json()

        # 将任务发送到 RabbitMQ 队列，返回 task_id
        try:
            task_id = send_to_rabbitmq(folder_path, "rename")
        except Exception as e:
            response = BaseResponse(code=500, status=500, message="Error", data={"error": str(e)})
            return response.to_json()

        # 返回任务已提交的响应，包含 task_id
        response = BaseResponse(code=200, status=200, message="Files are being processed",
                                data={"folder_path": folder_path, "task_id": task_id})
        return response.to_json()
