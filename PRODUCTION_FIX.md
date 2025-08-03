# Azure Production Deployment Fix

## Issue: Internal Server Error on Live Admin Panel
The admin panel at https://www.sundarmarbles.live/admin/products/product/add/ shows internal server error when adding products.

## Root Cause Analysis
1. Production Django settings using deprecated `DEFAULT_FILE_STORAGE`
2. Missing proper Azure Blob Storage configuration
3. Admin panel error handling not optimized for production

## Step 1: Update Django Settings for Production

The current settings.py needs to be updated with the new `STORAGES` configuration instead of the deprecated `DEFAULT_FILE_STORAGE`.

## Step 2: Deploy Updated Code

After making the changes locally, deploy to Azure:

```bash
# From django-backend directory
git add .
git commit -m "Fix Azure Blob Storage admin panel for production"
git push origin main
```

## Step 3: Verify Azure App Service Environment Variables

Ensure these environment variables are set in Azure App Service:
- AZURE_ACCOUNT_NAME=sundarmarbles
- AZURE_ACCOUNT_KEY=[your-azure-storage-key]
- AZURE_CONTAINER=media

## Step 4: Test the Flow

1. **Admin Panel**: https://www.sundarmarbles.live/admin/products/product/add/
   - Should save products without internal server error
   - Images should upload to Azure Blob Storage

2. **Blob Storage**: https://sundarmarbles.blob.core.windows.net/media/products/
   - Product images should appear here automatically

3. **Frontend**: https://www.sundarmarbles.live/products
   - Products should render with proper Azure Blob Storage URLs
   - Images should load from https://sundarmarbles.blob.core.windows.net/media/products/[filename]

## Expected Image URL Format
After upload: https://sundarmarbles.blob.core.windows.net/media/products/product-name.jpg

## Frontend Integration
The frontend (Products.jsx) already handles both backend and Azure Blob Storage URLs correctly:

```javascript
image={product.image ? (
  product.image.startsWith('http') 
    ? product.image // Already a full URL (Azure Blob)
    : product.image.startsWith('/media') 
      ? `${BACKEND_URL}${product.image}` // Relative URL, prepend backend
      : product.image // Local import or other
) : hero}
```

This ensures images load properly from Azure Blob Storage on the live website.
