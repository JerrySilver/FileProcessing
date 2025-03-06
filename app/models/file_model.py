from app import db
from datetime import datetime


class FileRecord(db.Model):
    __tablename__ = 'file_records'  # 设置表名

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    processed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, file_path, processed_at=None):
        self.file_path = file_path
        if processed_at is None:
            processed_at = datetime.utcnow()
        self.processed_at = processed_at

    def __repr__(self):
        return f"<FileRecord {self.file_path}>"
