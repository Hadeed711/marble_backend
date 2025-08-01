#!/usr/bin/env python
"""
Test Azure Blob Storage connection for Sundar Marbles
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sundar_marbles.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def test_azure_blob_storage():
    """Test Azure Blob Storage configuration and connectivity"""
    print("🔧 Testing Azure Blob Storage Configuration...")
    print("-" * 50)
    
    # Check if Azure settings are configured
    if hasattr(settings, 'AZURE_ACCOUNT_NAME'):
        print(f"✅ Azure Account Name: {settings.AZURE_ACCOUNT_NAME}")
        print(f"✅ Azure Container: {settings.AZURE_CONTAINER}")
        print(f"✅ Media URL: {settings.MEDIA_URL}")
        print(f"✅ Storage Backend: {settings.DEFAULT_FILE_STORAGE}")
    else:
        print("❌ Azure Blob Storage not configured - using local storage")
        return False
    
    print("\n🧪 Testing Azure Blob Storage Connection...")
    
    try:
        # Test file upload
        test_content = "This is a test file for Azure Blob Storage connectivity."
        test_file = ContentFile(test_content.encode())
        
        # Save test file
        file_name = "test_connection.txt"
        saved_name = default_storage.save(file_name, test_file)
        print(f"✅ Test file uploaded successfully: {saved_name}")
        
        # Get file URL
        file_url = default_storage.url(saved_name)
        print(f"✅ File URL generated: {file_url}")
        
        # Test file exists
        if default_storage.exists(saved_name):
            print("✅ File exists in Azure Blob Storage")
        else:
            print("❌ File not found in Azure Blob Storage")
            return False
        
        # Read file content
        with default_storage.open(saved_name, 'r') as f:
            content = f.read()
            if content == test_content:
                print("✅ File content verified successfully")
            else:
                print("❌ File content verification failed")
                return False
        
        # Clean up test file
        default_storage.delete(saved_name)
        print("✅ Test file cleaned up")
        
        print("\n🎉 Azure Blob Storage test completed successfully!")
        print("📸 New uploaded images will now be stored in Azure Blob Storage")
        print("🌐 Images will be publicly accessible via Azure CDN")
        
        return True
        
    except Exception as e:
        print(f"❌ Azure Blob Storage test failed: {str(e)}")
        print("\n🔍 Troubleshooting steps:")
        print("1. Verify Azure Storage Account credentials in .env file")
        print("2. Check that the 'media' container exists and is public")
        print("3. Ensure Azure Storage Account has correct permissions")
        return False

if __name__ == "__main__":
    test_azure_blob_storage()
