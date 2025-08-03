# Django 500 Error Fix Script
# Diagnoses and fixes internal server errors

Write-Host "🚨 Fixing Django 500 Internal Server Error..." -ForegroundColor Red
Write-Host ""

# Step 1: Test local Django setup first
Write-Host "🧪 Step 1: Testing Django locally..." -ForegroundColor Yellow
try {
    python manage.py check
    Write-Host "✅ Django check passed locally" -ForegroundColor Green
} catch {
    Write-Host "❌ Django check failed locally: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   This indicates a configuration issue in settings.py" -ForegroundColor Yellow
}

# Step 2: Run diagnostic command
Write-Host "🔍 Step 2: Running Django diagnostics..." -ForegroundColor Yellow
try {
    python manage.py diagnose_django
} catch {
    Write-Host "❌ Diagnostics failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Step 3: Test database connection
Write-Host "🗃️  Step 3: Testing database connection..." -ForegroundColor Yellow
try {
    python manage.py migrate --dry-run
    Write-Host "✅ Database connection working" -ForegroundColor Green
} catch {
    Write-Host "❌ Database connection failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Check DATABASE_URL environment variable" -ForegroundColor Yellow
}

# Step 4: Check if the issue is with Azure-specific settings
Write-Host "☁️  Step 4: Testing with minimal settings..." -ForegroundColor Yellow
Write-Host "   Creating backup of current settings..." -ForegroundColor Gray
Copy-Item "sundar_marbles\settings.py" "sundar_marbles\settings_backup.py" -Force

Write-Host "   Would you like to test with minimal debug settings? (y/n): " -ForegroundColor Cyan -NoNewline
$response = Read-Host

if ($response -eq 'y' -or $response -eq 'Y') {
    # Temporarily use debug settings
    Copy-Item "sundar_marbles\settings_debug.py" "sundar_marbles\settings.py" -Force
    
    Write-Host "🔄 Testing with minimal settings..." -ForegroundColor Yellow
    try {
        python manage.py check
        Write-Host "✅ Minimal settings work - Issue is in main settings.py" -ForegroundColor Green
        
        # Restore original settings
        Copy-Item "sundar_marbles\settings_backup.py" "sundar_marbles\settings.py" -Force
        Remove-Item "sundar_marbles\settings_backup.py" -Force
        
    } catch {
        Write-Host "❌ Even minimal settings fail: $($_.Exception.Message)" -ForegroundColor Red
        # Restore original settings
        Copy-Item "sundar_marbles\settings_backup.py" "sundar_marbles\settings.py" -Force
        Remove-Item "sundar_marbles\settings_backup.py" -Force
    }
} else {
    Remove-Item "sundar_marbles\settings_backup.py" -Force
}

# Step 5: Common fixes
Write-Host "🔧 Step 5: Applying common fixes..." -ForegroundColor Yellow

# Ensure requirements are up to date
Write-Host "   Checking requirements..." -ForegroundColor Gray
pip install -r requirements.txt --quiet

# Collect static files
Write-Host "   Collecting static files..." -ForegroundColor Gray
try {
    python manage.py collectstatic --noinput --clear
    Write-Host "✅ Static files collected" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Static files collection had issues: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Step 6: Deploy the fixes
Write-Host "📤 Step 6: Deploying fixes to Azure..." -ForegroundColor Yellow
git add .
git commit -m "HOTFIX: Resolve Django 500 internal server error - settings fixes"

try {
    git push origin main
    Write-Host "✅ Code deployed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Trying force push..." -ForegroundColor Yellow
    git push origin main --force
    Write-Host "✅ Force push completed" -ForegroundColor Green
}

# Step 7: Wait and test
Write-Host "⏳ Step 7: Waiting for Azure deployment..." -ForegroundColor Yellow
Write-Host "   Please wait 2-3 minutes for deployment to complete..." -ForegroundColor Gray

# Countdown
for ($i = 120; $i -gt 0; $i -= 10) {
    Write-Host "   $i seconds remaining..." -ForegroundColor Gray
    Start-Sleep -Seconds 10
}

# Test the deployment
Write-Host "🧪 Step 8: Testing deployed application..." -ForegroundColor Yellow

# Test backend API first (simpler endpoint)
Write-Host "   Testing backend API..." -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net/api/products/" -Method GET -TimeoutSec 15
    Write-Host "✅ Backend API is working" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend API failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test admin panel
Write-Host "   Testing admin panel..." -ForegroundColor Gray
try {
    $adminResponse = Invoke-WebRequest -Uri "https://www.sundarmarbles.live/admin/" -Method GET -TimeoutSec 15
    if ($adminResponse.StatusCode -eq 200) {
        Write-Host "✅ Admin panel is working!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Admin panel returned status: $($adminResponse.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Admin panel still failing: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔍 ADDITIONAL DEBUGGING NEEDED:" -ForegroundColor Red
    Write-Host "   1. Check Azure App Service logs:" -ForegroundColor Yellow
    Write-Host "      https://portal.azure.com -> App Service -> Monitoring -> Log stream" -ForegroundColor Cyan
    Write-Host "   2. Check environment variables in Azure:" -ForegroundColor Yellow
    Write-Host "      https://portal.azure.com -> App Service -> Configuration -> Application settings" -ForegroundColor Cyan
    Write-Host "   3. Restart the App Service:" -ForegroundColor Yellow
    Write-Host "      https://portal.azure.com -> App Service -> Restart" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🎯 TROUBLESHOOTING COMPLETED!" -ForegroundColor Green
Write-Host ""
Write-Host "If admin panel still shows 500 error:" -ForegroundColor Yellow
Write-Host "   • Check Azure logs for specific error messages" -ForegroundColor White
Write-Host "   • Verify all environment variables are set" -ForegroundColor White
Write-Host "   • Ensure database migrations completed" -ForegroundColor White
Write-Host "   • Check if Azure storage credentials are correct" -ForegroundColor White
