# Azure Blob Storage Setup
Write-Host "Setting up Azure Blob Storage..." -ForegroundColor Cyan

$appService = "sundar-bnhkawbtbbhjfxbz"
$resourceGroup = "hadeed"
$connectionString = "DefaultEndpointsProtocol=https;AccountName=sundarmarbles;AccountKey=PwoHf9IHD7u/3sHFTu3gnQvEZSpqpD/6HBhkTcW6WsBu+EnEqkjBWZSSTLjgg4XqmQYJRotuJSv4+AStKFedWg==;EndpointSuffix=core.windows.net"

try {
    az webapp config appsettings set --name $appService --resource-group $resourceGroup --settings "AZURE_STORAGE_CONNECTION_STRING=$connectionString" --output none
    az webapp config appsettings set --name $appService --resource-group $resourceGroup --settings "AZURE_CONTAINER=media" --output none
    
    Write-Host "Success! Environment variables set." -ForegroundColor Green
    Write-Host "Restart your App Service in Azure Portal" -ForegroundColor Yellow
    
} catch {
    Write-Host "Failed. Set manually in Azure Portal" -ForegroundColor Red
}
