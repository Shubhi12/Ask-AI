from typing import Optional, List
from fastapi import APIRouter, UploadFile, Request
from starlette.datastructures import UploadFile as StarletteUploadFile
from app.models.document import Documents
from app.models.users import Users
from app.services.upload import UploadService
from app.schemas.requests import UploadRequest

router = APIRouter()


@router.post("/", tags=["admin"])
async def upload_document(request: Request):
    """
    This endpoint uploads single or multiple documents to S3 storage and stores metadata in the Documents table.
    If any upload fails or DB metadata creation fails, all changes in the batch are rolled back.
    Supports file uploads (multipart/form-data), form fields, as well as JSON body requests.
    """
    try:
        content_type = request.headers.get("content-type", "").lower()
        req_user_name = "default_user"
        items_to_process = []

        if "application/json" in content_type:
            try:
                body = await request.json()
            except Exception:
                return {"error": "Invalid JSON body", "status": "error", "http_code": 400}

            upload_req = UploadRequest(**body) if isinstance(body, dict) else UploadRequest()
            req_user_name = upload_req.user_name or req_user_name

            if upload_req.file_path:
                fname = upload_req.file_name or upload_req.file_path.split("/")[-1]
                items_to_process.append({"file_name": fname, "type": "path", "data": upload_req.file_path})

            if upload_req.file_paths:
                file_names_list = upload_req.file_names or []
                for idx, p in enumerate(upload_req.file_paths):
                    fname = file_names_list[idx] if idx < len(file_names_list) else p.split("/")[-1]
                    items_to_process.append({"file_name": fname, "type": "path", "data": p})
        else:
            try:
                form_data = await request.form()
            except Exception as fe:
                return {"error": f"There was an error parsing the form body: {str(fe)}", "status": "error", "http_code": 400}

            upload_files = []
            for key, val in form_data.multi_items():
                if isinstance(val, (UploadFile, StarletteUploadFile)):
                    upload_files.append(val)
                elif key in ("file_path", "file_paths") and val:
                    val_str = str(val)
                    fname = val_str.split("/")[-1]
                    items_to_process.append({"file_name": fname, "type": "path", "data": val_str})
                elif key == "user_name" and val:
                    req_user_name = str(val)
            for uf in upload_files:
                contents = await uf.read()
                fname = uf.filename or "uploaded_file"
                items_to_process.append({"file_name": fname, "type": "bytes", "data": contents})

        # TODO: implement token authentication to fetch user details
        user = Users.get_user_by_username(req_user_name)
        if not user:
            return {"error": f"User '{req_user_name}' not found", "status": "error", "http_code": 404}
        user_id = user.id

        if not items_to_process:
            return {
                "error": "No file or file_path provided",
                "status": "error",
                "http_code": 400
            }

        # Check for duplicate document names for this user before starting uploads
        for item in items_to_process:
            existing_document = Documents.get_documents_by_user_id(user_id, item["file_name"])
            if existing_document:
                return {
                    "error": f"Document with name '{item['file_name']}' already exists for this user",
                    "status": "error",
                    "http_code": 400
                }

        upload_service = UploadService()
        successful_records = []
        results = []

        for item in items_to_process:
            target_file_name = item["file_name"]
            item_type = item["type"]
            data = item["data"]

            if item_type == "bytes":
                upload_res = upload_service.upload_bytes(target_file_name, data, req_user_name)
            else:
                upload_res = upload_service.upload(data, req_user_name)

            if upload_res.get("status") != "success":
                # Rollback previously uploaded files
                for s3_k, doc_rec in successful_records:
                    upload_service.delete(s3_k)
                    Documents.delete(doc_rec.id)
                return {
                    "error": f"Failed to upload document '{target_file_name}': {upload_res.get('error', 'Upload failed')}",
                    "status": "error",
                    "http_code": upload_res.get("http_code", 500)
                }

            s3_key = upload_res.get("path")
            try:
                doc_record = Documents.create(
                    user_id=user_id,
                    request={
                        "file_name": target_file_name,
                        "file_path": s3_key
                    }
                )
                successful_records.append((s3_key, doc_record))
                results.append({
                    "file_name": target_file_name,
                    "path": s3_key,
                    "document_id": doc_record.id
                })
            except Exception as db_err:
                if s3_key:
                    upload_service.delete(s3_key)
                for s3_k, doc_rec in successful_records:
                    upload_service.delete(s3_k)
                    Documents.delete(doc_rec.id)
                return {
                    "error": f"Failed to store metadata for '{target_file_name}', batch upload rolled back: {str(db_err)}",
                    "status": "error",
                    "http_code": 500
                }

        if len(results) == 1:
            return {
                "message": "Document uploaded and metadata stored successfully",
                "status": "success",
                "path": results[0]["path"],
                "document_id": results[0]["document_id"],
                "http_code": 200
            }

        return {
            "message": f"{len(results)} documents uploaded and metadata stored successfully",
            "status": "success",
            "documents": results,
            "count": len(results),
            "http_code": 200
        }

    except FileNotFoundError as e:
        return {"error": str(e), "status": "error", "http_code": 404}
    except Exception as e:
        return {"error": str(e), "status": "error", "http_code": 500}