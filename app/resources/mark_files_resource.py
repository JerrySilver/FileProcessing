from flask_restful import Resource
from flask import request, jsonify
from marshmallow import ValidationError
from app.schemas.file_schema import FileListSchema  # 假设用于请求和响应的 Schema
from app.services.file_service import mark_files
from app.utils.response_container import BaseResponse
from app.logger import logger  # 引入日志记录器

class MarkFilesResource(Resource):
    def post(self):
        logger.info("MarkFilesResource POST 请求开始")
        schema = FileListSchema()
        try:
            # 使用 Schema 解析并验证请求数据（这里建议使用 request.get_json() 获取 JSON 数据）
            data = schema.load(request.get_json())
            logger.info(f"请求数据解析成功：{data}")
        except ValidationError as err:
            logger.error(f"请求数据解析失败：{err.messages}")
            response = BaseResponse(
                code=400,
                status=400,
                message="数据解析失败",
                data={"error": err.messages}
            )
            return response.to_json()

        # 从解析后的数据中获取 fileModelList
        file_list = data.get("fileModelList")
        logger.info(f"获取到的文件列表：{file_list}")

        try:
            marking_results = mark_files(file_list)
            logger.info(f"打标结果：{marking_results}")
            result = []
            # 检查打标结果数量是否与文件列表一致
            if len(marking_results) != len(file_list):
                error_msg = "打标结果与文件列表数量不匹配"
                logger.error(error_msg)
                raise Exception(error_msg)
            # 将每个文件的打标结果添加到返回数据中
            for idx, file_item in enumerate(file_list):
                # 构造一个包含文件 ID 和打标结果的字典
                marked_file = {"neid": file_item['neid'], "tag": marking_results[idx]}
                result.append(marked_file)
            logger.info(f"最终返回的打标数据：{result}")
        except Exception as e:
            logger.error(f"打标出错：{str(e)}")
            response = BaseResponse(
                code=500,
                status=500,
                message="打标出错",
                data={"error": str(e)}
            )
            return response.to_json()

        response_data = {
            # "errcode": "0",
            # "errmsg": "ok",
            "result": result,
        }
        logger.info("MarkFilesResource POST 请求处理完毕，返回数据")
        response = BaseResponse(data=response_data)
        return response.to_json()
