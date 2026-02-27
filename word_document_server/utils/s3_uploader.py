"""
S3 uploader utility for Word documents.
"""
import os
import boto3
from botocore.exceptions import ClientError

def upload_to_s3(filename: str) -> dict:
    """Upload a file to S3 and return a presigned URL.
    
    Args:
        filename: Path to the file to upload
        
    Returns:
        dict with 'success', 'url', and 'message' keys
    """
    bucket_name = os.getenv('S3_BUCKET_NAME')
    region = os.getenv('AWS_REGION', 'us-east-1')
    url_expiration = int(os.getenv('S3_URL_EXPIRATION', '3600'))
    
    if not bucket_name:
        return {'success': False, 'url': None, 'message': 'S3_BUCKET_NAME not configured'}
    
    if not os.path.exists(filename):
        return {'success': False, 'url': None, 'message': f'File {filename} does not exist'}
    
    try:
        s3_client = boto3.client('s3', region_name=region)
        object_name = os.path.basename(filename)
        
        s3_client.upload_file(filename, bucket_name, object_name)
        
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=url_expiration
        )
        
        return {
            'success': True,
            'url': url,
            'message': f'Uploaded to s3://{bucket_name}/{object_name}'
        }
    except ClientError as e:
        return {'success': False, 'url': None, 'message': f'S3 upload failed: {str(e)}'}
    except Exception as e:
        return {'success': False, 'url': None, 'message': f'Upload error: {str(e)}'}
