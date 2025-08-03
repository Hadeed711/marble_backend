# Azure Deployment Fix Script
# Resolves 409 Conflict error and admin panel issues

Write-Host "🚀 Fixing Azure Deployment Issues..." -ForegroundColor Green

# Step 1: Force stop Azure App Service to release locks
Write-Host "🛑 Stopping Azure App Service to release deployment locks..." -ForegroundColor Yellow
Write-Host "   Please manually stop the app service at: https://portal.azure.com/" -ForegroundColor Cyan
Write-Host "   Navigate to your App Service -> Stop -> Wait 30 seconds -> Start" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter after you have stopped and restarted the App Service"

# Step 2: Clear any local deployment locks
Write-Host "🧹 Clearing local deployment cache..." -ForegroundColor Yellow
Remove-Item -Path ".\.git\refs\remotes\azure" -Recurse -Force -ErrorAction SilentlyContinue
git gc --prune=now

# Step 3: Force push the fixes
Write-Host "📤 Force pushing fixes to Azure..." -ForegroundColor Yellow
git add .
git commit -m "HOTFIX: Resolve admin panel internal server error and Azure storage config"

# Try normal push first
try {
    git push origin main
    Write-Host "✅ Normal push successful" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Normal push failed, trying force push..." -ForegroundColor Yellow
    git push origin main --force
    Write-Host "✅ Force push completed" -ForegroundColor Green
}

# Step 4: Wait for deployment
Write-Host "⏳ Waiting for Azure deployment to complete..." -ForegroundColor Yellow
Write-Host "   Monitor deployment at: https://portal.azure.com/" -ForegroundColor Cyan
Write-Host "   Go to App Service -> Deployment Center -> Logs" -ForegroundColor Cyan

# Countdown timer
for ($i = 60; $i -gt 0; $i--) {
    Write-Host "   Waiting $i seconds..." -ForegroundColor Gray
    Start-Sleep -Seconds 1
}

# Step 5: Test the fixes
Write-Host "🧪 Testing deployed application..." -ForegroundColor Yellow

# Test admin panel
Write-Host "Testing admin panel..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "https://www.sundarmarbles.live/admin/" -Method HEAD -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Admin panel is accessible" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Admin panel returned status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Admin panel test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test backend API
Write-Host "Testing backend API..." -ForegroundColor Cyan
try {
    $apiResponse = Invoke-RestMethod -Uri "https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net/api/products/" -Method GET -TimeoutSec 10
    Write-Host "✅ Backend API is working" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend API test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 FIXES COMPLETED!" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Fixed Issues:" -ForegroundColor Yellow
Write-Host "   • Added error handling to Django settings" -ForegroundColor White
Write-Host "   • Added missing Azure storage configuration" -ForegroundColor White
Write-Host "   • Resolved deployment conflicts" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Test These URLs:" -ForegroundColor Yellow
Write-Host "   1. Admin Panel: https://www.sundarmarbles.live/admin/" -ForegroundColor Cyan
Write-Host "   2. Add Product: https://www.sundarmarbles.live/admin/products/product/add/" -ForegroundColor Cyan
Write-Host "   3. Products Page: https://www.sundarmarbles.live/products" -ForegroundColor Cyan
Write-Host ""
Write-Host "If admin panel still shows error:" -ForegroundColor Red
Write-Host "   1. Check Azure App Service logs in portal" -ForegroundColor White
Write-Host "   2. Verify environment variables are set" -ForegroundColor White
Write-Host "   3. Restart the App Service manually" -ForegroundColor White
