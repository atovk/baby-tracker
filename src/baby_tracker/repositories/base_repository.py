"""
基础仓储类 - 使用 dataclasses DTO
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar, Dict, Any
from sqlalchemy.orm import Session
from baby_tracker.database import get_db

# 泛型类型
T = TypeVar('T')  # DTO type
M = TypeVar('M')  # Model type


class BaseRepository(ABC, Generic[T, M]):
    """基础仓储抽象类"""
    
    def __init__(self, db_session: Optional[Session] = None):
        self.db_session = db_session or next(get_db())
        self.model_class = self._get_model_class()
        self.mapper = self._get_mapper()
    
    @abstractmethod
    def _get_model_class(self):
        """获取对应的 SQLAlchemy 模型类"""
        pass
    
    @abstractmethod
    def _get_mapper(self):
        """获取对应的数据映射器"""
        pass
    
    def create(self, dto: T) -> T:
        """创建新记录"""
        model_instance = self.mapper.from_dto(dto)
        self.db_session.add(model_instance)
        self.db_session.commit()
        self.db_session.refresh(model_instance)
        return self.mapper.to_dto(model_instance)
    
    def get_by_id(self, record_id: str) -> Optional[T]:
        """根据ID获取记录"""
        model_instance = self.db_session.query(self.model_class).filter(
            self.model_class.id == record_id
        ).first()
        return self.mapper.to_dto(model_instance) if model_instance else None
    
    def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[T]:
        """获取所有记录"""
        query = self.db_session.query(self.model_class)
        if limit:
            query = query.limit(limit).offset(offset)
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def update(self, record_id: str, dto: T) -> Optional[T]:
        """更新记录"""
        model_instance = self.db_session.query(self.model_class).filter(
            self.model_class.id == record_id
        ).first()
        
        if not model_instance:
            return None
        
        self.mapper.update_model_from_dto(model_instance, dto)
        self.db_session.commit()
        self.db_session.refresh(model_instance)
        return self.mapper.to_dto(model_instance)
    
    def delete(self, record_id: str) -> bool:
        """删除记录"""
        model_instance = self.db_session.query(self.model_class).filter(
            self.model_class.id == record_id
        ).first()
        
        if not model_instance:
            return False
        
        self.db_session.delete(model_instance)
        self.db_session.commit()
        return True
    
    def count(self) -> int:
        """获取记录总数"""
        return self.db_session.query(self.model_class).count()
    
    def find_by(self, **kwargs) -> List[T]:
        """根据条件查找记录"""
        query = self.db_session.query(self.model_class)
        
        for field, value in kwargs.items():
            if hasattr(self.model_class, field):
                query = query.filter(getattr(self.model_class, field) == value)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def exists(self, record_id: str) -> bool:
        """检查记录是否存在"""
        return self.db_session.query(self.model_class).filter(
            self.model_class.id == record_id
        ).first() is not None
    
    def bulk_create(self, dtos: List[T]) -> List[T]:
        """批量创建记录"""
        model_instances = [self.mapper.from_dto(dto) for dto in dtos]
        self.db_session.add_all(model_instances)
        self.db_session.commit()
        
        for instance in model_instances:
            self.db_session.refresh(instance)
        
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def close(self):
        """关闭数据库会话"""
        if self.db_session:
            self.db_session.close()
