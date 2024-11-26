import boto3
import os
from dotenv import load_dotenv
from PIL import Image
load_dotenv()


class FileBaseStorage:
    def __init__(self):
        """
        Initializes the MongoDB helper class.
        :param db_name: Database name.
        :param collection_name: Collection name.
        """

        FILEBASE_KEY = os.getenv('FILEBASE_KEY')
        FILEBASE_SECRET = os.getenv('FILEBASE_SECRET')
        FILEBASE_API_ENDPOINT = os.getenv('FILEBASE_API_ENDPOINT')
        self.FILEBASE_BUCKET_NAME = os.getenv('FILEBASE_BUCKET_NAME', "test")

        self.s3 = boto3.client('s3',
                          endpoint_url=FILEBASE_API_ENDPOINT,
                          aws_access_key_id=FILEBASE_KEY,
                          aws_secret_access_key=FILEBASE_SECRET)

    def upload(self, file_path):
        key_name = file_path.split('/')[-1]
        data = open(file_path, 'rb')
        response = self.s3.put_object(Body=data, Bucket=self.FILEBASE_BUCKET_NAME, Key=key_name)
        return response

    def delete(self, key_name):
        self.s3.delete_object(Key=key_name, Bucket=self.FILEBASE_BUCKET_NAME)

    def list_all_files(self):
        files = []
        continuation_token = None
        while True:
            if continuation_token:
                response = self.s3.list_objects_v2(Bucket=self.FILEBASE_BUCKET_NAME, ContinuationToken=continuation_token)
            else:
                response = self.s3.list_objects_v2(Bucket=self.FILEBASE_BUCKET_NAME)
            if 'Contents' in response:
                files.extend(response['Contents'])
            if response.get('IsTruncated'):  # More files exist
                continuation_token = response['NextContinuationToken']
            else:
                break
        return files
