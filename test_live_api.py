#!/usr/bin/env python
"""
Test Azure API and image deployment for Sundar Marbles
"""
import requests
import json
from datetime import datetime

def test_azure_api_and_images():
    """Test Azure API and check image URLs"""
    BACKEND_URL = 'https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net'
    
    print("🔧 Testing Azure API and Image Configuration...")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test endpoints
    endpoints = [
        ('/api/products/', 'Products'),
        ('/api/gallery/', 'Gallery'),
        ('/api/products/categories/', 'Product Categories'),
        ('/api/gallery/categories/', 'Gallery Categories')
    ]
    
    results = {}
    
    for endpoint, name in endpoints:
        print(f"\n🧪 Testing {name} endpoint: {endpoint}")
        try:
            response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=10)
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    results[endpoint] = data
                    
                    # Handle paginated responses
                    items = data.get('results', data) if isinstance(data, dict) else data
                    
                    if isinstance(items, list):
                        print(f"   ✅ SUCCESS: {len(items)} items found")
                        
                        # Check image URLs in the data
                        if items and len(items) > 0:
                            print(f"   📋 Sample items:")
                            for i, item in enumerate(items[:3]):  # Show first 3 items
                                print(f"      {i+1}. {item.get('name', item.get('title', 'Unnamed'))}")
                                
                                # Check for image fields
                                image_url = item.get('image', None)
                                if image_url:
                                    print(f"         Image URL: {image_url}")
                                    
                                    # Check if it's Azure Blob Storage URL
                                    if 'sundarmarbles.blob.core.windows.net' in image_url:
                                        print(f"         ✅ Azure Blob Storage URL detected!")
                                    elif image_url.startswith('/media/'):
                                        print(f"         ⚠️  Local media URL - Azure not configured on server")
                                    elif image_url.startswith('http'):
                                        print(f"         🔍 External URL detected")
                                    else:
                                        print(f"         ❓ Unknown URL format")
                                else:
                                    print(f"         ❌ No image URL found")
                    else:
                        print(f"   ✅ SUCCESS: Response received")
                        
                except json.JSONDecodeError:
                    print(f"   ❌ FAILED: Invalid JSON response")
            else:
                print(f"   ❌ FAILED: HTTP {response.status_code}")
                if response.status_code == 500:
                    print(f"   💡 Possible issues:")
                    print(f"      - Database migration not applied")
                    print(f"      - Azure environment variables not set")
                    print(f"      - Django settings configuration error")
                elif response.status_code == 404:
                    print(f"   💡 Endpoint may not exist or be properly configured")
                    
        except requests.exceptions.Timeout:
            print(f"   ❌ TIMEOUT: Request took longer than 10 seconds")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ CONNECTION ERROR: Could not connect to server")
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY AND RECOMMENDATIONS")
    print("=" * 60)
    
    # Analyze results
    working_endpoints = []
    failed_endpoints = []
    
    for endpoint, name in endpoints:
        if endpoint in results:
            working_endpoints.append(name)
        else:
            failed_endpoints.append(name)
    
    print(f"✅ Working endpoints: {len(working_endpoints)}")
    for name in working_endpoints:
        print(f"   - {name}")
    
    print(f"❌ Failed endpoints: {len(failed_endpoints)}")
    for name in failed_endpoints:
        print(f"   - {name}")
    
    # Check if Azure Blob Storage is being used
    azure_blob_detected = False
    local_media_detected = False
    
    for endpoint, data in results.items():
        items = data.get('results', data) if isinstance(data, dict) else data
        if isinstance(items, list):
            for item in items:
                image_url = item.get('image', '')
                if 'sundarmarbles.blob.core.windows.net' in str(image_url):
                    azure_blob_detected = True
                elif '/media/' in str(image_url):
                    local_media_detected = True
    
    print(f"\n🔍 IMAGE STORAGE ANALYSIS:")
    if azure_blob_detected:
        print(f"   ✅ Azure Blob Storage URLs detected - Configuration working!")
    elif local_media_detected:
        print(f"   ⚠️  Local media URLs detected - Azure Blob Storage not deployed")
    else:
        print(f"   ❓ No image URLs found in API responses")
    
    print(f"\n💡 NEXT STEPS:")
    if failed_endpoints:
        print(f"   1. Fix failed API endpoints (likely database migration needed)")
        print(f"   2. Run: python manage.py migrate products")
        print(f"   3. Run: python manage.py migrate gallery")
    
    if not azure_blob_detected and working_endpoints:
        print(f"   4. Deploy Azure Blob Storage configuration to Azure App Service:")
        print(f"      - Add environment variables to Azure Portal")
        print(f"      - Update requirements.txt with django-storages[azure]")
        print(f"      - Deploy updated settings.py")
        print(f"      - Restart Azure App Service")
    
    if azure_blob_detected:
        print(f"   🎉 Azure Blob Storage is working! New images should appear instantly.")
    
    return results

if __name__ == "__main__":
    test_azure_api_and_images()
