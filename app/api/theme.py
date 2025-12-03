from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from app.db.database import get_db
from app.schemas.user import ThemeConfigResponse, ThemeConfigUpdate
from app.models.user import ThemeConfig, User
from app.api.deps import get_current_admin_user, get_current_user

router = APIRouter()


@router.get("/")
def get_user_theme(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    config_key = f"user_theme_{current_user.id}"
    config = db.query(ThemeConfig).filter(ThemeConfig.config_key == config_key).first()
    
    if config and config.config_value:
        try:
            return json.loads(config.config_value)
        except json.JSONDecodeError:
            return {}
    
    return {}


@router.put("/")
def save_user_theme(
    theme_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    config_key = f"user_theme_{current_user.id}"
    theme_json = json.dumps(theme_data)
    
    config = db.query(ThemeConfig).filter(ThemeConfig.config_key == config_key).first()
    
    if not config:
        config = ThemeConfig(
            config_key=config_key,
            config_value=theme_json
        )
        db.add(config)
    else:
        config.config_value = theme_json
    
    db.commit()
    return theme_data


@router.get("/all", response_model=List[ThemeConfigResponse])
def get_all_theme_configs(
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    configs = db.query(ThemeConfig).all()
    return configs


@router.patch("/{config_key}", response_model=ThemeConfigResponse)
def update_theme_config(
    config_key: str,
    config_update: ThemeConfigUpdate,
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    config = db.query(ThemeConfig).filter(ThemeConfig.config_key == config_key).first()
    
    if not config:
        # Create if doesn't exist
        config = ThemeConfig(
            config_key=config_key,
            config_value=config_update.config_value
        )
        db.add(config)
    else:
        config.config_value = config_update.config_value
    
    db.commit()
    db.refresh(config)
    return config
