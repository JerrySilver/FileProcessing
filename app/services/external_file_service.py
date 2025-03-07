import requests
from app.logger import logger
from app.config import Config

def get_file_list_from_external(params: dict) -> dict:
    """
    调用外部接口（例如 /v2/getFileList）获取文件列表数据。
    :param params: 请求参数字典，包含 path、path_type、sort、order_by、page_num、page_size 等字段
    :return: 返回文件列表数据的字典，格式应为：
             {
                 "errcode": "0",
                 "errmsg": "ok",
                 "fileModelList": [...],
                 "total": <int>
             }
    """
    # 示例：使用 requests.post 调用外部接口
    try:
        # 这里假设外部接口地址配置在 Config 中
        url = Config.EXTERNAL_FILE_LIST_URL  # 比如 "http://external-service/v2/getFileList"
        response = requests.post(url, json=params, timeout=10)
        #raise_for_status() 方法会检查 HTTP 响应状态码，如果状态码表示错误（如 4xx 或 5xx），将自动抛出异常。这样可以及时捕获请求失败的情况。
        response.raise_for_status()
        data = response.json()
        logger.info(f"外部接口返回数据：{data}")
        return data
    except Exception as e:
        logger.error(f"调用外部接口获取文件列表失败: {e}")
        raise e
