from app.resources.file_resource import FileResource, RenameFilesResource
from app.resources.mark_files_resource import MarkFilesResource
from app import api  # 导入已经初始化的 api 实例

# 确保正确添加资源路由
api.add_resource(FileResource, '/files/process')
api.add_resource(RenameFilesResource, '/files/rename')
api.add_resource(MarkFilesResource, '/files/mark')
