from app import ma

class FolderSchema(ma.Schema):
    class Meta:
        fields = ("folder_path",)
