from app import ma
from marshmallow import fields, validate

# 用于响应中单个文件的 Schema
class FileModelSchema(ma.Schema):
    desc = fields.Str(allow_none=True, missing="")
    dir = fields.Bool(
        required=True,
        error_messages={"required": "This field is required.", "validator_failed": "Not a valid boolean."}
    )
    modified = fields.Str(required=True)
    neid = fields.Str(required=True)
    nsid = fields.Int(required=True)
    path = fields.Str(required=True)
    pathType = fields.Str(required=True)
    rev = fields.Str(required=True)
    size = fields.Str(required=True)
    creator = fields.Str(required=True)
    creatorUid = fields.Str(required=True)
    updator = fields.Str(required=True)
    updatorUid = fields.Str(required=True)
    isTeam = fields.Bool(required=True)
    bookmarkId = fields.Int(required=True)
    supportPreview = fields.Bool(required=True)
    deliveryCode = fields.Str(required=True)
    isBookmark = fields.Bool(required=True)

# 用于文件列表响应的 Schema
class FileListSchema(ma.Schema):
    errcode = fields.Str(required=True)
    errmsg = fields.Str(required=True)
    fileModelList = fields.List(fields.Nested(FileModelSchema), required=True)
    total = fields.Int(required=True)


class GetFileListRequestSchema(ma.Schema):
    path = fields.Str(required=True, error_messages={"required": "Path is required."})
    path_type = fields.Str(
        required=True,
        validate=validate.OneOf(["ent", "self"]),
        error_messages={"required": "Path type is required.", "validator_failed": "Path type must be 'ent' or 'self'."}
    )
    sort = fields.Str(
        missing="desc",
        validate=validate.OneOf(["asc", "desc"]),
        error_messages={"validator_failed": "Sort must be either 'asc' or 'desc'."}
    )
    order_by = fields.Str(
        missing="mtime",
        validate=validate.OneOf(["name", "size", "mtime"]),
        error_messages={"validator_failed": "order_by must be 'name', 'size', or 'mtime'."}
    )
    page_num = fields.Int(
        missing=0,
        validate=validate.Range(min=0),
        error_messages={"invalid": "page_num must be a non-negative integer."}
    )
    page_size = fields.Int(
        missing=10,
        validate=validate.Range(min=0, max=999),
        error_messages={"invalid": "page_size must be between 0 and 999."}
    )
