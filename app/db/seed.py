from sqlalchemy.orm import Session
from app.models.resource import Resource
from app.models.user import User


def seed_default_resources(db: Session, user_id: str):
    """DO NOT auto-seed resources anymore. Admin must finalize resources explicitly."""
    return  # Resources are now manually managed by admin
    
    # Default resources to create
    default_resources = [
        {
            "icon": "flag",
            "title": "Seed Marker",
            "resource_name": "__seedmarker__",
            "description": "Internal marker (hidden from UI)",
            "status": "Hidden",
            "region": "Global"
        },
        {
            "icon": "server",
            "title": "Virtual Machine",
            "resource_name": "VM-Server-01",
            "description": "Your primary virtual machine instance",
            "status": "Running",
            "region": "East US"
        },
        {
            "icon": "globe",
            "title": "Website Name",
            "resource_name": "myawesomesite.com",
            "description": "Your main website domain",
            "status": "Running",
            "region": "East US"
        },
        {
            "icon": "link",
            "title": "Subdomain Name",
            "resource_name": "app.mysite.com",
            "description": "Application subdomain endpoint",
            "status": "Running",
            "region": "West Europe"
        },
        {
            "icon": "database",
            "title": "SQL Database",
            "resource_name": "prod-db-main",
            "description": "Production SQL database server",
            "status": "Running",
            "region": "East US"
        },
        {
            "icon": "hard_drive",
            "title": "Storage Account",
            "resource_name": "storageaccount123",
            "description": "Blob and file storage container",
            "status": "Running",
            "region": "Central US"
        },
        {
            "icon": "network",
            "title": "Virtual Network",
            "resource_name": "vnet-production",
            "description": "Azure virtual network gateway",
            "status": "Running",
            "region": "East US"
        },
        {
            "icon": "key",
            "title": "Key Vault",
            "resource_name": "keyvault-secrets",
            "description": "Secure secrets and certificates",
            "status": "Running",
            "region": "West US"
        },
        {
            "icon": "box",
            "title": "App Service",
            "resource_name": "webapp-prod-01",
            "description": "Web application hosting service",
            "status": "Running",
            "region": "East US"
        },
        {
            "icon": "folder_open",
            "title": "Resource Group",
            "resource_name": "rg-production",
            "description": "Resource group container",
            "status": "Running",
            "region": "Global"
        }
    ]
    
    # Create default resources
    for res_data in default_resources:
        resource = Resource(
            user_id=user_id,
            **res_data
        )
        db.add(resource)
    
    db.commit()
