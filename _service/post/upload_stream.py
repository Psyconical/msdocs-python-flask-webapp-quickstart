from azure.storage.blob import BlobServiceClient

def upload_to_blob_dtb(data,connect_str, Database, Links):  # Upload a text content in a file from azure storage
    print(connect_str)
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(Database, Links)
    blob_client.upload_blob(data, overwrite=True)