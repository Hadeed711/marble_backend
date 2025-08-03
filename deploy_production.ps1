# Azure Production Deployment Script (PowerShell)
# Fixes admin panel internal server error and ensures proper blob storage integration

Write-Host "🚀 Starting Azure Production Deployment..." -ForegroundColor Green

# Step 1: Commit and push the fixes
Write-Host "📤 Deploying code changes to Azure..." -ForegroundColor Yellow
git add .
git commit -m "Fix Azure Blob Storage admin panel for production - updated STORAGES configuration"
git push origin main

Write-Host "⏳ Waiting for Azure deployment to complete..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Step 2: Test the deployment
Write-Host "🧪 Testing deployed application..." -ForegroundColor Yellow

# Test API endpoint
try {
    $response = Invoke-RestMethod -Uri "https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net/api/products/" -Method GET
    Write-Host "✅ Backend API is working" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend API test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test debug endpoint
try {
    $debugResponse = Invoke-RestMethod -Uri "https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net/api/products/debug/storage/" -Method GET
    Write-Host "✅ Storage debug endpoint working" -ForegroundColor Green
    Write-Host "Storage backend: $($debugResponse.debug_info.storage_backend)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Debug endpoint test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 DEPLOYMENT COMPLETED!" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Test these URLs now:" -ForegroundColor Yellow
Write-Host "   1. Admin Panel: https://www.sundarmarbles.live/admin/products/product/add/" -ForegroundColor Cyan
Write-Host "   2. Products Page: https://www.sundarmarbles.live/products" -ForegroundColor Cyan
Write-Host "   3. Backend API: https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net/api/products/" -ForegroundColor Cyan
Write-Host "   4. Blob Storage: https://sundarmarbles.blob.core.windows.net/media/products/" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Expected Results:" -ForegroundColor Green
Write-Host "   • Admin panel should work without internal server error" -ForegroundColor White
Write-Host "   • Product images upload to Azure Blob Storage automatically" -ForegroundColor White
Write-Host "   • Products render on live website with proper image URLs" -ForegroundColor White
Write-Host "   • All images load from https://sundarmarbles.blob.core.windows.net/media/products/" -ForegroundColor White
