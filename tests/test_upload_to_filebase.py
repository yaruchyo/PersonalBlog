import boto3
import os
from dotenv import load_dotenv
load_dotenv()




def test_main():
	FILEBASE_KEY = os.getenv('FILEBASE_KEY')
	FILEBASE_SECRET = os.getenv('FILEBASE_SECRET')
	FILEBASE_API_ENDPOINT = os.getenv('FILEBASE_API_ENDPOINT')


	s3 = boto3.client('s3',
					  endpoint_url=FILEBASE_API_ENDPOINT,
					  aws_access_key_id=FILEBASE_KEY,
					  aws_secret_access_key=FILEBASE_SECRET)

	data = open('test_upload_to_filebase.py', 'rb')

	bucket_name = "storageforpersonalblog"
	key_name = "test_upload_to_filebase.py"
	responce = s3.put_object(Body=data, Bucket=bucket_name, Key=key_name)
	s3.delete_object(Bucket=bucket_name, Key=key_name)
