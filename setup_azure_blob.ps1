# PowerShell script to set up Azure Blob Storage using connection string
# This script will automatically configure your Azure App Service

Write-Host "🔧 Setting up Azure Blob Storage with Connection String" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

# Your Azure details
$subscriptionId = "fe8d86a5-33c7-4c0a-b192-dbfc07e9fe0f"
$resourceGroup = "hadeed"
$storageAccount = "sundarmarbles"
$appServiceName = "sundar-bnhkawbtbbhjfxbz"
$connectionString = "DefaultEndpointsProtocol=https;AccountName=sundarmarbles;AccountKey=PwoHf9IHD7u/3sHFTu3gnQvEZSpqpD/6HBhkTcW6WsBu+EnEqkjBWZSSTLjgg4XqmQYJRotuJSv4+AStKFedWg==;EndpointSuffix=core.windows.net"
$containerName = "media"

Write-Host "📋 Configuration Details:" -ForegroundColor Yellow
Write-Host "   Storage Account: $storageAccount"
Write-Host "   App Service: $appServiceName"
Write-Host "   Container: $containerName"
Write-Host "   Connection String: $($connectionString.Substring(0,50))..." -ForegroundColor Gray
Write-Host ""

# Check if Azure CLI is installed
try {
    $azVersion = az version --output tsv --query '"azure-cli"' 2>$null
    if ($azVersion) {
        Write-Host "✅ Azure CLI installed: $azVersion" -ForegroundColor Green
    } else {
        throw "Azure CLI not found"
    }
} catch {
    Write-Host "❌ Azure CLI not installed" -ForegroundColor Red
    Write-Host "   Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Yellow
    
    Write-Host ""
    Write-Host "🔧 Manual Setup Alternative:" -ForegroundColor Cyan
    Write-Host "   1. Go to Azure Portal → App Services → $appServiceName"
    Write-Host "   2. Configuration → Application Settings"
    Write-Host "   3. Add these environment variables:"
    Write-Host "      AZURE_STORAGE_CONNECTION_STRING = $connectionString"
    Write-Host "      AZURE_CONTAINER = $containerName"
    Write-Host "   4. Save and restart the App Service"
    exit 1
}

# Check if logged in
try {
    $account = az account show --query "user.name" --output tsv 2>$null
    if ($account) {
        Write-Host "✅ Logged in as: $account" -ForegroundColor Green
    } else {
        throw "Not logged in"
    }
} catch {
    Write-Host "❌ Not logged in to Azure CLI" -ForegroundColor Red
    Write-Host "   Run: az login" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🔧 Manual Setup Alternative:" -ForegroundColor Cyan
    Write-Host "   1. Go to Azure Portal → App Services → $appServiceName"
    Write-Host "   2. Configuration → Application Settings"
    Write-Host "   3. Add these environment variables:"
    Write-Host "      AZURE_STORAGE_CONNECTION_STRING = $connectionString"
    Write-Host "      AZURE_CONTAINER = $containerName"
    Write-Host "   4. Save and restart the App Service"
    exit 1
}

Write-Host ""
Write-Host "⚙️  Setting environment variables on App Service..." -ForegroundColor Cyan

try {
    # Set environment variables using connection string
    Write-Host "   📤 Setting AZURE_STORAGE_CONNECTION_STRING..." -ForegroundColor Gray
    az webapp config appsettings set --name $appServiceName --resource-group $resourceGroup --settings "AZURE_STORAGE_CONNECTION_STRING=$connectionString" --output none
    
    Write-Host "   📤 Setting AZURE_CONTAINER..." -ForegroundColor Gray
    az webapp config appsettings set --name $appServiceName --resource-group $resourceGroup --settings "AZURE_CONTAINER=$containerName" --output none
    
    Write-Host ""
    Write-Host "✅ Environment variables set successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Environment Variables Added:" -ForegroundColor Cyan
    Write-Host "   ✓ AZURE_STORAGE_CONNECTION_STRING (secured)" -ForegroundColor Green
    Write-Host "   ✓ AZURE_CONTAINER = $containerName" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "🔄 Next Steps:" -ForegroundColor Yellow
    Write-Host "   1. Restart your App Service (automatic or manual)"
    Write-Host "   2. Upload a new test image via Django admin"
    Write-Host "   3. Run: python test_azure_blob_verification.py"
    Write-Host "   4. Check if images now have blob.core.windows.net URLs"
    Write-Host ""
    
    # Offer to restart the app service
    Write-Host "🚀 Want to restart the App Service now? (y/n): " -ForegroundColor Yellow -NoNewline
    $restartResponse = Read-Host
    
    if ($restartResponse -eq 'y' -or $restartResponse -eq 'Y') {
        Write-Host ""
        Write-Host "🔄 Restarting App Service..." -ForegroundColor Cyan
        try {
            az webapp restart --name $appServiceName --resource-group $resourceGroup --output none
            Write-Host "✅ App Service restarted successfully!" -ForegroundColor Green
            Write-Host ""
            Write-Host "🎯 Ready to test! Upload a new image and run:" -ForegroundColor Green
            Write-Host "   python test_azure_blob_verification.py" -ForegroundColor White
        } catch {
            Write-Host "❌ Failed to restart App Service automatically" -ForegroundColor Red
            Write-Host "   Please restart manually in Azure Portal" -ForegroundColor Yellow
        }
    } else {
        Write-Host ""
        Write-Host "📝 Manual Restart Required:" -ForegroundColor Yellow
        Write-Host "   Go to Azure Portal → App Services → $appServiceName → Restart"
    }
    
} catch {
    Write-Host "❌ Failed to set environment variables" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Manual Setup Required:" -ForegroundColor Yellow
    Write-Host "   1. Go to: https://portal.azure.com/#@/resource/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.Web/sites/$appServiceName/configuration"
    Write-Host "   2. Click 'Application Settings'"
    Write-Host "   3. Add these environment variables:"
    Write-Host "      Name: AZURE_STORAGE_CONNECTION_STRING"
    Write-Host "      Value: $connectionString"
    Write-Host ""
    Write-Host "      Name: AZURE_CONTAINER"
    Write-Host "      Value: $containerName"
    Write-Host "   4. Save and restart the App Service"
}
}

Write-Host ""
Write-Host "🎯 After Setup - Test Commands:" -ForegroundColor Cyan
Write-Host "   python test_azure_blob_verification.py" -ForegroundColor White
Write-Host "   python test_correct_gallery.py" -ForegroundColor White
Write-Host ""
Write-Host "✅ Expected Result:" -ForegroundColor Green
Write-Host "   Image URLs will change from:" -ForegroundColor Gray
Write-Host "   https://sundar-bnhkawbtbbhjfxbz.eastasia-01.azurewebsites.net/media/..." -ForegroundColor Red
Write-Host "   To:" -ForegroundColor Gray
Write-Host "   https://sundarmarbles.blob.core.windows.net/media/..." -ForegroundColor Green
