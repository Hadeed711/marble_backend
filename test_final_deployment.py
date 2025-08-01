#!/usr/bin/env python
"""
Quick test to verify Azure deployment after manual fixes
"""
import requests
import json

def test_azure_deployment():
    """Test if Azure deployment is working after manual fixes"""
    BACKEND_URL = 'https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net'
    
    print("🧪 Testing Azure Deployment After Manual Fixes")
    print("=" * 50)
    
    # Test critical endpoints
    tests = [
        ('/api/products/', 'Products API'),
        ('/api/gallery/', 'Gallery API'),
    ]
    
    all_working = True
    azure_blob_detected = False
    
    for endpoint, name in tests:
        print(f"\n🔍 Testing {name}: {endpoint}")
        
        try:
            response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS: Status 200")
                
                try:
                    data = response.json()
                    items = data.get('results', data) if isinstance(data, dict) else data
                    
                    if isinstance(items, list) and len(items) > 0:
                        print(f"   📊 Found {len(items)} items")
                        
                        # Check first item for Azure Blob Storage URL
                        first_item = items[0]
                        image_url = first_item.get('image', '')
                        
                        if image_url:
                            print(f"   🖼️  First image URL: {image_url}")
                            
                            if 'sundarmarbles.blob.core.windows.net' in image_url:
                                print(f"   🎉 AZURE BLOB STORAGE DETECTED!")
                                azure_blob_detected = True
                            elif image_url.startswith('/media/'):
                                print(f"   ⚠️  Still using local media URLs")
                            else:
                                print(f"   ❓ Unknown URL format")
                        else:
                            print(f"   ℹ️  No image in first item")
                    else:
                        print(f"   ℹ️  No items found (empty database)")
                        
                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON response")
                    all_working = False
                    
            elif response.status_code == 500:
                print(f"   ❌ FAILED: Status 500 - Database migration still needed")
                all_working = False
            elif response.status_code == 404:
                print(f"   ❌ FAILED: Status 404 - Endpoint configuration issue")
                all_working = False
            else:
                print(f"   ❌ FAILED: Status {response.status_code}")
                all_working = False
                
        except requests.exceptions.Timeout:
            print(f"   ⏱️  TIMEOUT: Request took too long")
            all_working = False
        except Exception as e:
            print(f"   💥 ERROR: {str(e)}")
            all_working = False
    
    print("\n" + "=" * 50)
    print("📋 FINAL RESULTS")
    print("=" * 50)
    
    if all_working:
        print("✅ ALL API ENDPOINTS WORKING!")
        
        if azure_blob_detected:
            print("🎉 AZURE BLOB STORAGE ACTIVE!")
            print("📸 New images will appear instantly on website!")
            print("\n🧪 Test Process:")
            print("   1. Go to Django Admin")
            print("   2. Add a new product/gallery image")
            print("   3. Check your website - image should appear immediately!")
        else:
            print("⚠️  APIs working but Azure Blob Storage not detected")
            print("💡 Check Azure environment variables are set correctly")
            
    else:
        print("❌ SOME ISSUES STILL EXIST")
        print("\n🔧 Next Steps:")
        print("   1. Ensure database migrations are applied on Azure")
        print("   2. Verify all environment variables are set")
        print("   3. Check Django settings.py is updated")
        print("   4. Restart Azure App Service")
        print("   5. Run this test again")
    
    return all_working and azure_blob_detected

if __name__ == "__main__":
    success = test_azure_deployment()
    if success:
        print("\n🎯 DEPLOYMENT SUCCESSFUL - Ready to test image uploads!")
    else:
        print("\n❌ DEPLOYMENT NEEDS MORE WORK - Check the steps above")
