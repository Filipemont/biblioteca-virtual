import os
from datetime import timedelta
from loguru import logger  # type: ignore
from minio import Minio  # type: ignore
from minio.error import S3Error  # type: ignore



class MinioUtil:
    minio_client = Minio(
        os.getenv('MINIO_URL'),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        region="f3",
        secure=False,
    )

    def upload_file(self, bucket_name: str, arquivo_local: str, data: object, length: int, content_type: str) -> None:
        if not self.minio_client.bucket_exists(bucket_name):
            self.minio_client.make_bucket(bucket_name)
        self.minio_client.put_object(bucket_name, arquivo_local, data, length, content_type)

    def get_minio_url(self, minio_file_name: str):
        try:
            url: str = self.minio_client.presigned_get_object("biblioteca", minio_file_name, expires=timedelta(minutes=15))
            if "minio:9000" in url:
                return url.replace("minio:9000", "localhost:9000")
            return url
        except S3Error as e:
            logger.exception(f'Erro ao gerar url do arquivo: {e}')

    def get_minio_object_data(self, filename: str):
        try:
            data: object = self.minio_client.get_object("biblioteca", filename)
            return data
        except S3Error as e:
            logger.exception(f'Erro ao coletar dados do arquivo: {e}')
            return None

    def delete_minio_file(self, bucket_name: str, object_name: str):
        try:
            objetos_para_apagar = self.minio_client.list_objects(bucket_name, prefix=object_name, recursive=True)
            for obj in objetos_para_apagar:
                logger.info(f"Apagando: {obj.object_name}")
                self.minio_client.remove_object(bucket_name, obj.object_name)
        except Exception as e:
            logger.exception(e)
        except S3Error as x:
            logger.exception(x)
