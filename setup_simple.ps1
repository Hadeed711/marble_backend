# Simple Azure Blob} catch {
    Write-Host "❌ Failed. Set manually in Azure Portal:" -ForegroundColor Red
    Write-Host "AZURE_STORAGE_CONNECTION_STRING = $connectionString"
    Write-Host "AZURE_CONTAINER = media"
}rage Setup Script
Write-Host "🔧 Setting up Azure Blob Storage" -ForegroundColor Cyan

$appServiceName = "sundar-bnhkawbtbbhjfxbz"
$resourceGroup = "hadeed"
$connectionString = "DefaultEndpointsProtocol=https;AccountName=sundarmarbles;AccountKey=PwoHf9IHD7u/3sHFTu3gnQvEZSpqpD/6HBhkTcW6WsBu+EnEqkjBWZSSTLjgg4XqmQYJRotuJSv4+AStKFedWg==;EndpointSuffix=core.windows.net"

Write-Host "Setting environment variables..." -ForegroundColor Yellow

try {
    # Set connection string
    az webapp config appsettings set --name $appServiceName --resource-group $resourceGroup --settings "AZURE_STORAGE_CONNECTION_STRING=$connectionString" --output none
    
    # Set container name
    az webapp config appsettings set --name $appServiceName --resource-group $resourceGroup --settings "AZURE_CONTAINER=media" --output none
    
    Write-Host "✅ Success! Environment variables set." -ForegroundColor Green
    Write-Host "Now restart your App Service in Azure Portal" -ForegroundColor Yellow
    
} catch {
    Write-Host "❌ Failed. Set manually in Azure Portal:" -ForegroundColor Red
    Write-Host "AZURE_STORAGE_CONNECTION_STRING = $connectionString"
    Write-Host "AZURE_CONTAINER = media"
}
