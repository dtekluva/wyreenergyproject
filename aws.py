# import boto3

# session = boto3.session.Session()
# client = session.client('s3',
#                         region_name='nyc3',
#                         endpoint_url='https://flemmer.sfo2.digitaloceanspaces.com/',
#                         aws_access_key_id='3JHFXKKQGUSMJIJVJVOF',
#                         aws_secret_access_key='T8z1k9sSb/L1sD+OzMg6CFBkonXnCmr8Hp8p4exog2k')

# client.upload_file('avatar-4.jpg',  # Path to local file
#                    'flemmer',  # Name of Space
#                    'avatar-4.jpg')  # Name for remote file


# import boto3
# from botocore.client import Config

# # Initialize a session using DigitalOcean Spaces.
# session = boto3.session.Session()
# client = session.client('s3',
#                         region_name='nyc3',
#                         endpoint_url='https://flemmer.sfo2.digitaloceanspaces.com',
#                         aws_access_key_id='3JHFXKKQGUSMJIJVJVOF',
#                         aws_secret_access_key='T8z1k9sSb/L1sD+OzMg6CFBkonXnCmr8Hp8p4exog2k')

# # Create a new Space.
# client.create_bucket(Bucket='my-new-space')

# # List all buckets on your account.
# response = client.list_buckets()
# spaces = [space['Name'] for space in response['Buckets']]
# print("Spaces List: %s" % spaces)


from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print('File {} uploaded to {}.'.format(source_file_name,destination_blob_name))

upload_blob("inyang_bucket", "requirements.txt", "a.txt")