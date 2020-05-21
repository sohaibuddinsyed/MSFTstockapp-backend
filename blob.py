
try:
    # print("Azure Blob storage v12 - Python quickstart sample")
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    # print(connect_str)
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a unique name for the container
    container_name = "datasetcontainer" 

    # Create the container
    # container_client = blob_service_client.create_container(container_name)
    # Create a file in local data directory to upload and download
    local_path = "./"
    local_file_name = "ds.csv"
    upload_file_path = os.path.join(local_path, local_file_name)


# Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
     # Instantiate a ContainerClient
    container_client = blob_service_client.get_container_client("datasetcontainer")
    container_client.delete_blob("ds.csv")

    print("\nDeleting blob from Azure Storage:\n\t" + local_file_name)

    print("\n\n Now, uploading to Azure Storage as blob:\n\t" + local_file_name)
  
# Upload the created /file
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)
  
except Exception as ex:
    print('Exception:')
    print(ex)
   
