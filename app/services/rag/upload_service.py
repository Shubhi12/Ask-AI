import os
from core.config import settings
from core.storage import get_storage_client

class UploadService:
    def __init__(self):

        self.storage_client = get_storage_client()
    
    def upload(self, file_path: str, user_name: str):
        try:
            file_name = self.get_file_name(file_path)
            if not file_name:
                raise ValueError("Invalid file path")

            if not os.path.exists(file_path):
                raise FileNotFoundError("File not found")
            
            temp_file_path = self.move_file_to_temp_directory(file_path)
            if not temp_file_path:
                raise Exception("Failed to move file to temp directory")            
            with open(temp_file_path, "rb") as f:
                file_bytes = f.read()

            return self.upload_bytes(file_name, file_bytes, user_name)
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }

    def upload_bytes(self, file_name: str, file_bytes: bytes, user_name: str = "default_user"):
        try:
            bucket_name = settings.S3_BUCKET_NAME or "upload_company_docs"
            key = f"user_uploads/{user_name}/{file_name}"
            content_type = self.get_content_type(file_name)

            self.storage_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=file_bytes,
                ContentType=content_type
            )

            return {
                "message": "Document uploaded successfully",
                "status": "success",
                "path": key
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }

    
    def get_content_type(self, file_path: str):
        file_extension = file_path.split(".")[-1]
        if file_extension == "pdf":
            content_type = "application/pdf"
        elif file_extension == "txt":
            content_type = "text/plain"
        elif file_extension == "csv":
            content_type = "text/csv"
        elif file_extension == "json":
            content_type = "application/json"
        elif file_extension == "xml":
            content_type = "application/xml"
        elif file_extension == "docx":
            content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif file_extension == "html":
            content_type = "text/html"
        elif file_extension == "htm":
            content_type = "text/html"
        elif file_extension == "css":
            content_type = "text/css"
        elif file_extension == "js":
            content_type = "application/javascript"
        elif file_extension == "py":
            content_type = "text/x-python"
        else:
            content_type = "application/octet-stream"
        return content_type
    
    def get_file_name(self, file_path: str):
        return file_path.split("/")[-1]

    def move_file_to_temp_directory(self, file_path: str):
        os.makedirs("temp", exist_ok=True)
        temp_file_path = f"temp/{self.get_file_name(file_path)}"
        os.rename(file_path, temp_file_path)
        return temp_file_path