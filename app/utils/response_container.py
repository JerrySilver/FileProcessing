from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List
from flask import jsonify

@dataclass
class Base:
    """基础类，提供将对象转换为字典或 JSON 格式的方法"""

    def asdict(self):
        return asdict(self)

    def to_json(self):
        return jsonify(asdict(self))


@dataclass
class BaseResponse(Base):
    """基础响应类，包含 code, status, message 和 data"""
    code: int = 200
    status: int = 200
    message: str = "请求成功"
    data: Any = field(default_factory=lambda: None)  # 使用 default_factory 解决可变默认值问题

    __annotations__ = {
        "code": int,
        "status": int,
        "message": str,
        "data": Any,
    }


@dataclass
class ListData(Base):
    """用于返回列表数据的结构"""
    total: int
    items: List[Dict]

    __annotations__ = {
        "total": int,
        "items": List[Dict],
    }


@dataclass
class ListResponse(BaseResponse):
    """返回包含列表数据的响应"""
    data: ListData = field(default_factory=lambda: ListData(0, []))  # 使用 default_factory 解决可变默认值问题

    __annotations__ = {
        "data": ListData,
    }


# 可用于测试是否返回期望的格式
if __name__ == "__main__":
    import json
    print(json.dumps(BaseResponse(data=dict()).asdict()))
    print(json.dumps(ListResponse(data=ListData(total=0, items=[])).asdict()))
