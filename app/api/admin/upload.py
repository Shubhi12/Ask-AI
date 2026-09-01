import os
import shutil
from fastapi import APIRouter, UploadFile, Request
from starlette.datastructures import UploadFile as StarletteUploadFile
from app.core.config import settings
from app.models.document import Documents
from app.models.users import Users
from app.services.upload import UploadService
from app.schemas.requests import UploadRequest
from app.ingestion.tasks import ingest_documents

router = APIRouter()


@router.post("/", tags=["admin"])
async def upload_document(request: Request):
    """
    Upload single or multiple documents to S3 storage and store metadata in Documents table.
    1. Reads list of files and user_name from payload (taking filename directly from file object).
    2. Pre-checks for duplicate document names for the user in the database.
    3. Temporarily uploads files to /documents/<user_name> directory.
    4. Uploads files to S3 bucket.
    5. Stores metadata in database.
    6. Asynchronously calls ingest_documents(file_names, document_ids, user_name).
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
                fname = upload_req.file_name or os.path.basename(upload_req.file_path)
                items_to_process.append({"file_name": fname, "type": "path", "data": upload_req.file_path})

            if upload_req.file_paths:
                file_names_list = upload_req.file_names or []
                for idx, p in enumerate(upload_req.file_paths):
                    fname = file_names_list[idx] if idx < len(file_names_list) else os.path.basename(p)
                    items_to_process.append({"file_name": fname, "type": "path", "data": p})
        else:
            try:
                form_data = await request.form()
            except Exception as fe:
                return {"error": f"There was an error parsing the form body: {str(fe)}", "status": "error", "http_code": 400}

            for key, val in form_data.multi_items():
                if isinstance(val, (UploadFile, StarletteUploadFile)):
                    contents = await val.read()
                    # Extract file_name directly from the file itself for all cases
                    raw_filename = val.filename or "uploaded_file"
                    fname = os.path.basename(raw_filename)
                    items_to_process.append({"file_name": fname, "type": "bytes", "data": contents})
                elif key == "user_name" and val:
                    req_user_name = str(val)
                elif key in ("file_path", "file_paths") and val:
                    val_str = str(val)
                    fname = os.path.basename(val_str)
                    items_to_process.append({"file_name": fname, "type": "path", "data": val_str})

        # Check user existence
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

        # 2. Check if the files already exist in the database for the user
        for item in items_to_process:
            existing_document = Documents.get_documents_by_user_id(user_id, item["file_name"])
            if existing_document:
                return {
                    "error": f"Document with name '{item['file_name']}' already exists for this user",
                    "status": "error",
                    "http_code": 400
                }

        # 3. Temporarily upload the files to /documents/<user_name> directory
        user_doc_dir = os.path.join(settings.DOCUMENT_PATH, req_user_name)
        os.makedirs(user_doc_dir, exist_ok=True)
        local_saved_files = []

        try:
            for item in items_to_process:
                target_file_name = item["file_name"]
                local_file_path = os.path.join(user_doc_dir, target_file_name)

                if item["type"] == "bytes":
                    with open(local_file_path, "wb") as f:
                        f.write(item["data"])
                elif item["type"] == "path":
                    if os.path.exists(item["data"]):
                        shutil.copy(item["data"], local_file_path)
                    else:
                        with open(local_file_path, "w") as f:
                            f.write(str(item["data"]))

                local_saved_files.append(local_file_path)

            # 4 & 5. Upload files to S3 bucket and store metadata in database
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
                    # Rollback S3 uploads and DB metadata
                    for s3_k, doc_rec in successful_records:
                        upload_service.delete(s3_k)
                        Documents.delete(doc_rec.id)
                    # Cleanup saved local files
                    for lfp in local_saved_files:
                        if os.path.exists(lfp):
                            os.remove(lfp)
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
                    for lfp in local_saved_files:
                        if os.path.exists(lfp):
                            os.remove(lfp)
                    return {
                        "error": f"Failed to store metadata for '{target_file_name}', batch upload rolled back: {str(db_err)}",
                        "status": "error",
                        "http_code": 500
                    }

            # 6. Asynchronously call ingest_documents(file_names, document_ids, user_name)
            file_names = [r["file_name"] for r in results]
            document_ids = [r["document_id"] for r in results]
            ingest_documents.delay(file_names, document_ids, req_user_name)

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
                "documents": [
                    {
                        "file_name": r["file_name"],
                        "path": r["path"],
                        "document_id": r["document_id"]
                    }
                    for r in results
                ],
                "count": len(results),
                "http_code": 200
            }

        except Exception as proc_err:
            for lfp in local_saved_files:
                if os.path.exists(lfp):
                    os.remove(lfp)
            raise proc_err

    except FileNotFoundError as e:
        return {"error": str(e), "status": "error", "http_code": 404}
    except Exception as e:
        return {"error": str(e), "status": "error", "http_code": 500}