from flask import Blueprint, Response, stream_with_context
from utils.minio_utils import MinioUtil



minio_view = Blueprint("minio_view", __name__, url_prefix="/media")


@minio_view.route("/<path:filename>")
def get_file_url(filename):
    minio_util = MinioUtil()
    try:
        response = minio_util.minio_client.get_object("biblioteca", filename)
        
        return Response(
            stream_with_context(response.stream(32*1024)),
            headers={
                "Content-Type": response.headers.get('content-type', 'application/octet-stream'),
                "Content-Disposition": f"inline; filename={filename}"
            }
        )
    except Exception as e:
        return "File not found", 404