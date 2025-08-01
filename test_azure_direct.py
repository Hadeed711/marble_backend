#!/usr/bin/env python
"""
Simple Azure Blob Storage connectivity test
"""
from azure.storage.blob import BlobServiceClient
import os

def test_azure_blob_direct():
    """Test Azure Blob Storage directly without Django"""
    print("🔧 Direct Azure Blob Storage Test")
    print("=" * 40)
    
    # Azure credentials
    account_name = "sundarmarbles"
    account_key = "PwoHf9IHD7u/3sHFTu3gnQvEZSpqpD/6HBhkTcW6WsBu+EnEqkjBWZSSTLjgg4XqmQYJRotuJSv4+AStKFedWg=="
    container_name = "media"
    
    try:
        # Create blob service client
        blob_service_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=account_key
        )
        
        print(f"✅ Account: {account_name}")
        print(f"✅ Container: {container_name}")
        
        # Test container access
        container_client = blob_service_client.get_container_client(container_name)
        
        # List some blobs to test connectivity
        blob_list = list(container_client.list_blobs())
        print(f"✅ Connection successful!")
        print(f"📁 Found {len(blob_list)} files in container")
        
        if blob_list:
            print("📋 Recent files:")
            for blob in blob_list[:5]:  # Show first 5 files
                blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob.name}"
                print(f"   - {blob.name}")
                print(f"     URL: {blob_url}")
        
        # Test upload
        test_content = "Azure connectivity test file"
        test_blob_name = "test_connectivity.txt"
        
        blob_client = container_client.get_blob_client(test_blob_name)
        blob_client.upload_blob(test_content, overwrite=True)
        
        print(f"✅ Test upload successful!")
        
        # Get URL
        test_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{test_blob_name}"
        print(f"✅ Test file URL: {test_url}")
        
        # Clean up
        blob_client.delete_blob()
        print(f"✅ Test file cleaned up")
        
        print("\n🎉 Azure Blob Storage is fully functional!")
        print("🔧 The issue is not with Azure - it's with the deployment.")
        
        return True
        
    except Exception as e:
        print(f"❌ Azure Blob Storage test failed: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        test_azure_blob_direct()
    except ImportError:
        print("❌ Azure SDK not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "azure-storage-blob"])
        print("✅ Azure SDK installed. Run the test again.")
