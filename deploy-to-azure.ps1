# Azure Container Deployment Script for Car API
# Run this script in PowerShell after logging into Azure CLI

# Variables - customize these
$resourceGroup = "carapi-rg"
$location = "eastus"
$acrName = "carapiacr"  # Must be globally unique - change if needed
$containerName = "car-api-container"
$imageName = "carapi:latest"
$dnsLabel = "carapi-demo"  # Must be globally unique - change if needed

# Check if logged in
Write-Host "Checking Azure login status..."
try {
    $account = az account show --query name -o tsv
    Write-Host "Logged in as: $account"
} catch {
    Write-Host "Not logged in to Azure. Please run 'az login' first."
    exit 1
}

# Create resource group
Write-Host "Creating resource group: $resourceGroup"
az group create --name $resourceGroup --location $location

# Create Azure Container Registry
Write-Host "Creating Azure Container Registry: $acrName"
az acr create --resource-group $resourceGroup --name $acrName --sku Basic

# Build and push the Docker image to ACR
Write-Host "Building and pushing Docker image to ACR..."
az acr build --registry $acrName --image $imageName .

# Deploy to Azure Container Instances
Write-Host "Deploying to Azure Container Instances..."
az container create `
  --resource-group $resourceGroup `
  --name $containerName `
  --image "$acrName.azurecr.io/$imageName" `
  --dns-name-label $dnsLabel `
  --ports 8000 `
  --cpu 1 `
  --memory 1

# Get the public FQDN
Write-Host "Getting container details..."
$fqdn = az container show --resource-group $resourceGroup --name $containerName --query ipAddress.fqdn -o tsv

Write-Host "Deployment complete! Your API will be available at: https://$fqdn"
Write-Host "API Docs: https://$fqdn/docs"