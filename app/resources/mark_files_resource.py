import json
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError

from app.logger import get_logger
from app.schemas.file_schema import FileListSchema
from app.utils.response_container import BaseResponse
from app.services.rabbitmq_service import rabbitmq_rpc

# 获取日志记录器
logger = get_logger()


class MarkFilesResource(Resource):
    def post(self):
        schema = FileListSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            response = BaseResponse(
                code=400,
                status=400,
                message="文件数据参数有错",
                data={"error": err.messages}
            )
            logger.error("文件数据参数有误，请检查: %s", err.messages)
            return response.to_json()

        # 组装 RPC 请求消息：包含任务类型、文件列表和路径类型
        task_message = {
            "task_type": "mark_files",
            "fileModelList": data.get("fileModelList"),
        }
        try:
            rpc_response = rabbitmq_rpc.call(json.dumps(task_message))
            result_data = json.loads(rpc_response)
        except Exception as e:
            response = BaseResponse(
                code=500,
                status=500,
                message="打标任务处理出错",
                data={"error": str(e)}
            )
            logger.error("打标任务处理出错", e)
            return response.to_json()

        # response_data = {
        #     # "errcode": "0",
        #     # "errmsg": "ok",
        #     "result": result_data
        # }
        response = BaseResponse(data=result_data)
        logger.info("成功完成文件打标: %s", result_data)
        return response.to_json()
