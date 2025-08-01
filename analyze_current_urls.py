#!/usr/bin/env python
"""
Test current image URLs from your API
"""
import requests

def analyze_current_image_urls():
    """Analyze the current image URLs from your API"""
    BACKEND_URL = 'https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net'
    
    print("🔍 ANALYZING CURRENT IMAGE URLs")
    print("=" * 50)
    print(f"API Base: {BACKEND_URL}")
    print("=" * 50)
    
    # Test endpoints that might work
    endpoints = [
        ('/api/products/categories/', 'Product Categories'),
        ('/api/gallery/categories/', 'Gallery Categories'),
    ]
    
    for endpoint, name in endpoints:
        print(f"\n📋 Testing {name}: {endpoint}")
        try:
            response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ SUCCESS: {len(data)} items")
                
                # Look for any image fields
                for item in data[:3]:  # First 3 items
                    print(f"   📝 {item.get('name', 'Unknown')}")
                    
                    # Check all fields for potential image URLs
                    for key, value in item.items():
                        if isinstance(value, str) and ('media' in value or 'http' in value or '.jpg' in value or '.png' in value):
                            print(f"      🖼️  {key}: {value}")
                        
            else:
                print(f"   ❌ FAILED: Status {response.status_code}")
                
        except Exception as e:
            print(f"   💥 ERROR: {str(e)}")
    
    print(f"\n" + "=" * 50)
    print("📊 URL ANALYSIS")
    print("=" * 50)
    
    example_current_url = "https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net/media/gallery/IAAC_logo-01.png"
    example_target_url = "https://sundarmarbles.blob.core.windows.net/media/gallery/IAAC_logo-01.png"
    
    print(f"🔍 CURRENT FORMAT:")
    print(f"   {example_current_url}")
    print(f"   ❌ This means: Using local Azure App Service storage")
    print(f"   ⚠️  Problem: Files might not persist, slow loading")
    
    print(f"\n🎯 TARGET FORMAT:")
    print(f"   {example_target_url}")
    print(f"   ✅ This means: Using Azure Blob Storage")
    print(f"   🚀 Benefits: Fast loading, persistent storage, CDN")
    
    print(f"\n💡 TO FIX:")
    print(f"   1. Add Azure environment variables to App Service")
    print(f"   2. Deploy django-storages package")
    print(f"   3. Restart App Service")
    print(f"   4. New uploads will use Azure Blob Storage URLs")

if __name__ == "__main__":
    analyze_current_image_urls()
