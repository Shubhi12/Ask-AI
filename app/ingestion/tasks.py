import os
import shutil
from app.workers.celery_app import celery_app
from app.ingestion.pipeline import IngesionPipeline
from app.models.document import Documents
from app.core.storage import get_storage_client
from app.core.config import settings


@celery_app.task(rate_limit="1/m")
def ingest_documents(file_names: list[str], document_ids: list[int], user_name: str):
    """
    Celery task to ingest documents into KnowledgeBase vector table.
    - Accepts file_names, document_ids, user_name.
    - Reads files from /documents/<user_name> directory.
    - Deletes files from /documents/<user_name> directory after ingestion is completed.
    """
    user_doc_dir = os.path.join(settings.DOCUMENT_PATH, user_name)
    processed_paths = []
    storage_client = None

    try:
        for doc_id, fname in zip(document_ids, file_names):
            local_path = os.path.join(user_doc_dir, fname)

            # Check if file exists in /documents/<user_name>/ directory
            if not os.path.exists(local_path):
                # Download from S3 if file is not locally present on worker
                doc = Documents.get_document_by_id(doc_id)
                if doc and doc.file_path:
                    os.makedirs(user_doc_dir, exist_ok=True)
                    if not storage_client:
                        storage_client = get_storage_client()
                    storage_client.download_file(settings.S3_BUCKET_NAME, doc.file_path, local_path)

            if os.path.exists(local_path):
                processed_paths.append(local_path)
        if processed_paths:
            ingestion_pipeline = IngesionPipeline()
            ingestion_pipeline.run(processed_paths, document_ids)
        # Delete files from /documents/<user_name> directory after ingestion
        for fname in file_names:
            target_path = os.path.join(user_doc_dir, fname)
            if os.path.exists(target_path):
                try:
                    os.remove(target_path)
                except Exception as del_err:
                    print(f"Error deleting file '{target_path}' after ingestion: {del_err}")

        # Remove directory if empty
        if os.path.exists(user_doc_dir) and not os.listdir(user_doc_dir):
            try:
                os.rmdir(user_doc_dir)
            except Exception:
                pass
    except Exception as e:
        print(f"ERROR in ingest_documents Celery task for user '{user_name}': {e}")
        raise e
        