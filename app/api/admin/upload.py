from typing import Optional
from fastapi import APIRouter, File, UploadFile, Form, Request
from app.services.rag.upload_service import UploadService
from app.schemas.requests import UploadRequest

router = APIRouter()




@router.post("/", tags=["admin"])
async def upload_document(
    request: Request,
    file: Optional[UploadFile] = File(None),
    file_name: Optional[UploadFile] = File(None),
    file_path: Optional[str] = Form(None),
    user_name: Optional[str] = Form("default_user"),
):
    """
    This endpoint uploads a document to S3 storage.
    Supports file uploads (multipart/form-data) with any form field name (file, file_name, etc.),
    form fields (file_path, user_name), as well as JSON body requests.
    """
    try:
        content_type = request.headers.get("content-type", "")

        # 1. Handle JSON request body if Content-Type is application/json
        if "application/json" in content_type:
            body = await request.json()
            upload_req = UploadRequest(**body)
            uname = upload_req.user_name or "default_user"
            if not upload_req.file_path:
                return {"error": "file_path is required for JSON upload", "status": "error", "http_code": 400}
            return UploadService().upload(upload_req.file_path, uname)

        # 2. Handle multipart/form-data or form upload
        actual_file = file or file_name
        if actual_file is None:
            form_data = await request.form()
            for key, val in form_data.items():
                if isinstance(val, UploadFile):
                    actual_file = val
                    break
                elif key == "file_path" and not file_path:
                    file_path = str(val)
                elif key == "user_name" and user_name == "default_user":
                    user_name = str(val)

        uname = user_name or "default_user"

        if actual_file:
            contents = await actual_file.read()
            filename = actual_file.filename or "uploaded_file"
            return UploadService().upload_bytes(filename, contents, uname)

        if file_path:
            return UploadService().upload(file_path, uname)

        return {
            "error": "No file or file_path provided",
            "status": "error",
            "http_code": 400
        }
    except FileNotFoundError as e:
        return {"error": str(e), "status": "error", "http_code": 404}
    except Exception as e:
        return {"error": str(e), "status": "error", "http_code": 500}