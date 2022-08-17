import logging
import boto3
from botocore.exceptions import ClientError
import os
from os.path import exists as file_exists

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_to_s3(recent_uploaded):

    files_to_upload = []
    if file_exists(recent_uploaded):
        with open(recent_uploaded, 'r') as f:
            files_to_upload = [line.replace('\n','') for line in f]
    
    files_uploaded = 0
    files_with_error = []
    for file in files_to_upload:

        path_in_s3 = file.replace("/LUSTRE/sacmod/SIPECAM/","")

        uploaded = upload_file(file,os.getenv("BUCKET_S3"),path_in_s3)

        if uploaded:
            files_uploaded += 1
        else:
            files_with_error.append(file)
    
    if len(files_with_error) > 0:
        print("Could not upload this files: \n")
        print(files_with_error)
    
    return "%d files uploaded to s3" % files_uploaded