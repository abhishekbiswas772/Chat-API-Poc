from minio import Minio
from minio.error import S3Error
import os
import base64


minio_client = Minio(
    os.getenv('MINIO_URL', 'localhost:9000'),
    access_key=os.getenv("ACCESS_KEY"),
    secret_key=os.getenv("SECRET_KEY"),
    secure=False
)

class UploadManager:
    def postImageUpload(self, image_data, object_name, bucket_name) -> bool:
        try:
            if not minio_client.bucket_exists(bucket_name=bucket_name):
                minio_client.make_bucket(bucket_name=bucket_name)
            image_data = base64.b64decode(image_data)
            minio_client.put_object(
                bucket_name,
                object_name,
                image_data,
                len(image_data),
                "image/jpeg"
            )
            return True
        except S3Error as err:
            print(err)
            return False
        except Exception as e:
            print(err)
            return False
        

    def getImageUploadURL(self, bucket_name, object_name) -> str:
        try:
            image_url = minio_client.presigned_get_object(
                bucket_name,
                object_name
            )
            return image_url
        except S3Error as err:
            print(err)
            return ""
        except Exception as err:
            print(err)
            return ""


