# Azure Blob Storage Admin Fix Guide

## Issue
The admin panel shows "Internal Server Error" when trying to add products with images.

## Root Cause
The issue is likely due to:
1. Deprecated `DEFAULT_FILE_STORAGE` setting in Django 4.2+
2. Missing Azure blob storage dependencies
3. Incorrect Azure storage configuration

## Fixes Applied

### 1. Updated Django Storage Settings (settings.py)
- Replaced deprecated `DEFAULT_FILE_STORAGE` with new `STORAGES` configuration
- Added proper Azure storage backend configuration
- Added connection timeout and memory size settings for better reliability

### 2. Enhanced Admin Panel (admin.py)
- Added comprehensive error handling in admin save methods
- Added file size validation (5MB limit)
- Added file type validation (.jpg, .jpeg, .png, .webp)
- Added detailed success/error messages
- Improved image preview with error handling

### 3. Updated Requirements (requirements.txt)
- Added latest Azure storage blob and identity packages
- Ensures compatibility with latest django-storages

### 4. Added Debug Tools
- Created `test_azure_storage` management command
- Added debug endpoint at `/api/products/debug/storage/`

## Testing Steps

### Step 1: Update Dependencies
```bash
cd f:\development\sundar_marbles\django-backend
pip install -r requirements.txt
```

### Step 2: Test Azure Storage Connectivity
```bash
python manage.py test_azure_storage
```

### Step 3: Check Storage Configuration
```bash
python manage.py shell
```
Then run:
```python
from django.conf import settings
from django.core.files.storage import default_storage
print("Storage backend:", default_storage.__class__.__name__)
print("Media URL:", settings.MEDIA_URL)
print("Azure configured:", hasattr(settings, 'AZURE_ACCOUNT_NAME'))
```

### Step 4: Test Local Admin Panel
```bash
python manage.py runserver 8000
```
Visit: http://localhost:8000/admin/products/product/add/

### Step 5: Test Debug Endpoint
Visit: http://localhost:8000/api/products/debug/storage/

### Step 6: Deploy to Production
After local testing works:
```bash
git add .
git commit -m "Fix Azure Blob Storage admin panel integration"
git push origin main
```

## Expected Behavior After Fix

1. **Admin Panel**: Should successfully save products with images
2. **Image Upload**: Images should upload to Azure blob storage in `products/` folder
3. **Image URLs**: Should generate proper Azure blob storage URLs
4. **Error Handling**: Should show helpful error messages instead of internal server errors
5. **File Validation**: Should validate file size and type before upload

## Troubleshooting

### If Local Testing Fails:
1. Check environment variables in `.env` file
2. Verify Azure storage account credentials
3. Run `python manage.py test_azure_storage` for detailed diagnostics

### If Production Still Fails:
1. Check Azure App Service logs
2. Verify environment variables are set in Azure App Service
3. Ensure Azure storage account allows blob access
4. Check CORS settings in Azure storage account

## Environment Variables Required
```
AZURE_ACCOUNT_NAME=sundarmarbles
AZURE_ACCOUNT_KEY=your-azure-storage-key
AZURE_CONTAINER=media
```

## File Structure After Upload
Images will be stored as:
```
https://sundarmarbles.blob.core.windows.net/media/products/image-name.jpg
```

## Additional Notes
- Maximum file size: 5MB
- Supported formats: JPG, JPEG, PNG, WEBP
- Images are automatically resized and optimized
- All uploads go to Azure blob storage, not local filesystem
