#!/usr/bin/env python
"""
Simple test to check Azure Blob Storage status
"""
import requests
import sys

def test_azure_status():
    print("🔍 TESTING AZURE BLOB STORAGE STATUS")
    print("=" * 50)
    
    # Test gallery API
    api_url = "https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net/api/gallery/images/"
    
    try:
        print(f"📡 Testing: {api_url}")
        response = requests.get(api_url, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if results:
                print(f"   ✅ Found {len(results)} images")
                
                # Check first image URL
                first_image = results[0]
                image_url = first_image.get('image', '')
                print(f"   📷 Sample image URL: {image_url}")
                
                if 'blob.core.windows.net' in image_url:
                    print("   ✅ AZURE BLOB STORAGE CONFIGURED!")
                    print("   🎉 Images are using Azure Blob Storage URLs")
                elif 'azurewebsites.net/media/' in image_url:
                    print("   ❌ AZURE BLOB STORAGE NOT CONFIGURED")
                    print("   ⚠️  Images are on temporary App Service storage")
                    print("   💡 Solution: Set environment variables on Azure App Service")
                else:
                    print(f"   ❓ Unknown URL format: {image_url}")
            else:
                print("   ⚠️  No images found in gallery")
        else:
            print(f"   ❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"   💥 ERROR: {str(e)}")
    
    print("\n" + "=" * 50)
    print("📋 NEXT STEPS:")
    print("1. Set Azure environment variables:")
    print("   AZURE_STORAGE_CONNECTION_STRING = [your connection string]")
    print("   AZURE_CONTAINER = media")
    print("2. Restart Azure App Service")
    print("3. Upload a new test image")
    print("4. Run this test again")

if __name__ == "__main__":
    test_azure_status()
