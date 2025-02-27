from flask import jsonify
from app.utils.response_container import BaseResponse  # 引入之前定义的统一返回格式


def register_error_handlers(app):
    """注册全局异常捕获器"""

    # 捕获所有未处理的异常
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """处理所有未预料到的异常"""
        response = BaseResponse(
            code=500,
            status=500,
            message="服务器内部错误",
            data={"error": str(error)}
        )
        return response.to_json()

    # 捕获 404 错误
    @app.errorhandler(404)
    def handle_not_found(error):
        """处理 404 错误"""
        response = BaseResponse(
            code=404,
            status=404,
            message="请求的资源未找到",
            data={"error": str(error)}
        )
        return response.to_json()

    # 捕获 400 错误
    @app.errorhandler(400)
    def handle_bad_request(error):
        """处理 400 错误"""
        response = BaseResponse(
            code=400,
            status=400,
            message="请求错误",
            data={"error": str(error)}
        )
        return response.to_json()
