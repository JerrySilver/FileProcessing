from app import ma
from marshmallow import fields, validate

# 用于响应中单个文件的 Schema
class FileModelSchema(ma.Schema):
    desc = fields.Str(allow_none=True, missing="")
    dir = fields.Bool(required=True)
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
