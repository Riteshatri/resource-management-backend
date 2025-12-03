from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceResponse
from app.api.deps import get_current_user

router = APIRouter()

# Template resources - Azure specific
TEMPLATE_RESOURCES = [
    {
        "title": "Azure Virtual Machine",
        "resource_name": "vm-prod-eastus-01",
        "description": "Windows/Linux VM for compute workloads",
        "icon": "server",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure App Service",
        "resource_name": "app-service-api-prod",
        "description": "Managed web app hosting",
        "icon": "globe",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure SQL Database",
        "resource_name": "sqldb-prod-eastus",
        "description": "Managed relational database",
        "icon": "database",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Cosmos DB",
        "resource_name": "cosmosdb-main",
        "description": "NoSQL distributed database",
        "icon": "box",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Storage Account",
        "resource_name": "stgacct-prod-eastus",
        "description": "Blob, Table, Queue storage",
        "icon": "hard_drive",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Key Vault",
        "resource_name": "keyvault-prod-eastus",
        "description": "Secrets and certificate management",
        "icon": "lock",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Load Balancer",
        "resource_name": "lb-frontend-prod",
        "description": "Network load balancing",
        "icon": "network",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure API Management",
        "resource_name": "apim-prod-eastus",
        "description": "API gateway and management",
        "icon": "link",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Container Registry",
        "resource_name": "acr-prod-eastus",
        "description": "Docker container image repository",
        "icon": "container",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Functions",
        "resource_name": "func-app-serverless",
        "description": "Serverless compute functions",
        "icon": "zap",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Service Bus",
        "resource_name": "servicebus-prod",
        "description": "Message queuing and pub/sub",
        "icon": "activity",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Application Insights",
        "resource_name": "appinsights-prod",
        "description": "Application monitoring and analytics",
        "icon": "shield",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Virtual Network",
        "resource_name": "vnet-prod-eastus",
        "description": "Virtual networking and connectivity",
        "icon": "network",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure VPN Gateway",
        "resource_name": "vpn-gateway-prod",
        "description": "Secure site-to-site connectivity",
        "icon": "lock",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure ExpressRoute",
        "resource_name": "expressroute-prod",
        "description": "Dedicated network connection",
        "icon": "link",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure CDN",
        "resource_name": "cdn-prod-eastus",
        "description": "Content delivery network",
        "icon": "globe",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Monitor",
        "resource_name": "monitor-prod",
        "description": "Comprehensive monitoring platform",
        "icon": "activity",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Log Analytics",
        "resource_name": "log-analytics-prod",
        "description": "Log collection and analysis",
        "icon": "database",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Security Center",
        "resource_name": "security-center-prod",
        "description": "Unified security management",
        "icon": "shield",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Backup",
        "resource_name": "backup-vault-prod",
        "description": "Data protection and recovery",
        "icon": "box",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Site Recovery",
        "resource_name": "site-recovery-prod",
        "description": "Disaster recovery solution",
        "icon": "zap",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure DevOps",
        "resource_name": "devops-project-prod",
        "description": "CI/CD and project management",
        "icon": "activity",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Data Factory",
        "resource_name": "data-factory-prod",
        "description": "Data integration and ETL",
        "icon": "database",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Synapse Analytics",
        "resource_name": "synapse-prod-eastus",
        "description": "Big data and analytics",
        "icon": "box",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Databricks",
        "resource_name": "databricks-prod",
        "description": "Apache Spark analytics platform",
        "icon": "zap",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Machine Learning",
        "resource_name": "ml-workspace-prod",
        "description": "ML model development and deployment",
        "icon": "cloud",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Cognitive Services",
        "resource_name": "cognitive-services-prod",
        "description": "AI APIs for vision, language, speech",
        "icon": "zap",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Bot Service",
        "resource_name": "bot-service-prod",
        "description": "Build intelligent bots",
        "icon": "globe",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Search",
        "resource_name": "search-service-prod",
        "description": "Full-text search capability",
        "icon": "box",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Redis Cache",
        "resource_name": "redis-cache-prod",
        "description": "In-memory data store",
        "icon": "database",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure IoT Hub",
        "resource_name": "iot-hub-prod",
        "description": "IoT device management and data",
        "icon": "zap",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Event Hubs",
        "resource_name": "event-hub-prod",
        "description": "Real-time data streaming",
        "icon": "activity",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Stream Analytics",
        "resource_name": "stream-analytics-prod",
        "description": "Real-time analytics processing",
        "icon": "activity",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Time Series Insights",
        "resource_name": "tsi-prod-eastus",
        "description": "Time series data storage and analysis",
        "icon": "database",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Digital Twins",
        "resource_name": "digital-twins-prod",
        "description": "Digital representation platform",
        "icon": "cloud",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Bastion",
        "resource_name": "bastion-prod-eastus",
        "description": "Secure remote access to VMs",
        "icon": "lock",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Firewall",
        "resource_name": "firewall-prod-eastus",
        "description": "Network security and threat protection",
        "icon": "shield",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure DDoS Protection",
        "resource_name": "ddos-protection-prod",
        "description": "DDoS attack mitigation",
        "icon": "shield",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Front Door",
        "resource_name": "front-door-prod",
        "description": "Global load balancer and WAF",
        "icon": "link",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Traffic Manager",
        "resource_name": "traffic-manager-prod",
        "description": "DNS-based traffic management",
        "icon": "network",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Private Link",
        "resource_name": "private-link-prod",
        "description": "Private connectivity to Azure services",
        "icon": "lock",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Notification Hubs",
        "resource_name": "notification-hub-prod",
        "description": "Push notification platform",
        "icon": "activity",
        "status": "Running",
        "region": "East US"
    },
    {
        "title": "Azure Service Fabric",
        "resource_name": "service-fabric-prod",
        "description": "Distributed systems platform",
        "icon": "boxes",
        "status": "Running",
        "region": "East US"
    }
]


@router.get("/templates")
def get_templates():
    """Get list of available template resources"""
    return [{"id": i, **t} for i, t in enumerate(TEMPLATE_RESOURCES)]


@router.post("/import-templates", response_model=List[ResourceResponse], status_code=status.HTTP_201_CREATED)
def import_selected_templates(
    template_ids: List[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Import selected template resources - admin only"""
    from app.models.user import UserRole
    
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can import resources"
        )
    
    created_resources = []
    for template_id in template_ids:
        if 0 <= template_id < len(TEMPLATE_RESOURCES):
            template = TEMPLATE_RESOURCES[template_id]
            resource = Resource(
                user_id=current_user.id,
                title=template["title"],
                resource_name=template["resource_name"],
                description=template["description"],
                icon=template["icon"],
                status=template["status"],
                region=template["region"]
            )
            db.add(resource)
            db.flush()
            
            created_resources.append(ResourceResponse(
                id=resource.id,
                user_id=str(resource.user_id),
                icon=resource.icon,
                title=resource.title,
                resource_name=resource.resource_name,
                description=resource.description,
                status=resource.status,
                region=resource.region,
                created_at=resource.created_at,
                updated_at=resource.updated_at
            ))
    
    db.commit()
    return created_resources


@router.get("/", response_model=List[ResourceResponse])
def get_user_resources(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all resources - admin sees their own, others see admin's resources"""
    from app.models.user import UserRole
    
    if current_user.role == UserRole.admin:
        # Admin sees their own resources
        resources = db.query(Resource).filter(Resource.user_id == current_user.id).all()
    else:
        # Regular users see the admin's resources
        admin = db.query(User).filter(User.role == UserRole.admin).first()
        if admin:
            resources = db.query(Resource).filter(Resource.user_id == admin.id).all()
        else:
            resources = []
    
    # Convert UUID to string for response
    return [
        ResourceResponse(
            id=r.id,
            user_id=str(r.user_id),
            icon=r.icon,
            title=r.title,
            resource_name=r.resource_name,
            description=r.description,
            status=r.status,
            region=r.region,
            created_at=r.created_at,
            updated_at=r.updated_at
        )
        for r in resources
    ]


@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
def create_resource(
    resource_data: ResourceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new resource - admin only"""
    from app.models.user import UserRole
    
    # Only admin can create resources
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create resources"
        )
    
    resource = Resource(
        user_id=current_user.id,
        icon=resource_data.icon,
        title=resource_data.title,
        resource_name=resource_data.resource_name,
        description=resource_data.description,
        status=resource_data.status,
        region=resource_data.region
    )
    # Set custom created_at if provided
    if resource_data.created_at:
        resource.created_at = resource_data.created_at
    
    db.add(resource)
    db.commit()
    db.refresh(resource)
    
    # Convert UUID to string for response
    return ResourceResponse(
        id=resource.id,
        user_id=str(resource.user_id),
        icon=resource.icon,
        title=resource.title,
        resource_name=resource.resource_name,
        description=resource.description,
        status=resource.status,
        region=resource.region,
        created_at=resource.created_at,
        updated_at=resource.updated_at
    )


@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a resource - admin only"""
    from app.models.user import UserRole
    
    # Only admin can update resources
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update resources"
        )
    
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    resource.icon = resource_data.icon
    resource.title = resource_data.title
    resource.resource_name = resource_data.resource_name
    resource.description = resource_data.description
    resource.status = resource_data.status
    resource.region = resource_data.region
    
    # Update created_at if provided
    if resource_data.created_at:
        resource.created_at = resource_data.created_at
    
    db.commit()
    db.refresh(resource)
    
    # Convert UUID to string for response
    return ResourceResponse(
        id=resource.id,
        user_id=str(resource.user_id),
        icon=resource.icon,
        title=resource.title,
        resource_name=resource.resource_name,
        description=resource.description,
        status=resource.status,
        region=resource.region,
        created_at=resource.created_at,
        updated_at=resource.updated_at
    )




@router.post("/seed/templates", response_model=List[ResourceResponse], status_code=status.HTTP_201_CREATED)
def seed_template_resources(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Seed default template resources - admin only"""
    from app.models.user import UserRole
    
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can seed resources"
        )
    
    # Template resources - Azure specific
    templates = [
        {
            "title": "Azure Virtual Machine",
            "resource_name": "vm-prod-eastus-01",
            "description": "Windows/Linux VM for compute workloads",
            "icon": "server",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure App Service",
            "resource_name": "app-service-api-prod",
            "description": "Managed web app hosting",
            "icon": "globe",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure SQL Database",
            "resource_name": "sqldb-prod-eastus",
            "description": "Managed relational database",
            "icon": "database",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Cosmos DB",
            "resource_name": "cosmosdb-main",
            "description": "NoSQL distributed database",
            "icon": "box",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Storage Account",
            "resource_name": "stgacct-prod-eastus",
            "description": "Blob, Table, Queue storage",
            "icon": "hard_drive",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Key Vault",
            "resource_name": "keyvault-prod-eastus",
            "description": "Secrets and certificate management",
            "icon": "lock",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Load Balancer",
            "resource_name": "lb-frontend-prod",
            "description": "Network load balancing",
            "icon": "network",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure API Management",
            "resource_name": "apim-prod-eastus",
            "description": "API gateway and management",
            "icon": "link",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Container Registry",
            "resource_name": "acr-prod-eastus",
            "description": "Docker container image repository",
            "icon": "container",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Functions",
            "resource_name": "func-app-serverless",
            "description": "Serverless compute functions",
            "icon": "zap",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Service Bus",
            "resource_name": "servicebus-prod",
            "description": "Message queuing and pub/sub",
            "icon": "activity",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Application Insights",
            "resource_name": "appinsights-prod",
            "description": "Application monitoring and analytics",
            "icon": "shield",
            "status": "Running",
            "region": "East US"
        }
    ]
    
    created_resources = []
    for template in templates:
        resource = Resource(
            user_id=current_user.id,
            title=template["title"],
            resource_name=template["resource_name"],
            description=template["description"],
            icon=template["icon"],
            status=template["status"],
            region=template["region"]
        )
        db.add(resource)
        db.flush()
        
        created_resources.append(ResourceResponse(
            id=resource.id,
            user_id=str(resource.user_id),
            icon=resource.icon,
            title=resource.title,
            resource_name=resource.resource_name,
            description=resource.description,
            status=resource.status,
            region=resource.region,
            created_at=resource.created_at,
            updated_at=resource.updated_at
        ))
    
    db.commit()
    return created_resources


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a resource - admin only"""
    from app.models.user import UserRole
    
    # Only admin can delete resources
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete resources"
        )
    
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    db.delete(resource)
    db.commit()
    return None
