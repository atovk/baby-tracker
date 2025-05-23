"""
喂养相关仓储 - 使用 dataclasses DTO
"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from baby_tracker.models.dto import NursingDTO, FormulaDTO, FeedingStatsDTO
from baby_tracker.models.mappers import NursingMapper, FormulaMapper
from baby_tracker.repositories.base_repository import BaseRepository


class NursingRepository(BaseRepository[NursingDTO, 'Nursing']):
    """母乳喂养仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.feeding import Nursing
        return Nursing
    
    def _get_mapper(self):
        return NursingMapper
    
    def find_by_baby_id(self, baby_id: str, limit: Optional[int] = None) -> List[NursingDTO]:
        """根据宝宝ID查找喂养记录"""
        query = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc())
        
        if limit:
            query = query.limit(limit)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def find_by_date_range(self, baby_id: str, start_date: datetime, end_date: datetime) -> List[NursingDTO]:
        """根据日期范围查找喂养记录"""
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
        
        model_instances = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).order_by(self.model_class.time.desc()).all()
        
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def get_daily_stats(self, baby_id: str, date: datetime) -> dict:
        """获取指定日期的喂养统计"""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        start_timestamp = start_of_day.timestamp()
        end_timestamp = end_of_day.timestamp()
        
        # 查询当日喂养记录
        records = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).all()
        
        total_sessions = len(records)
        total_duration = sum(
            record.left_duration + record.right_duration + record.both_duration 
            for record in records
        )
        
        return {
            'date': date.date(),
            'total_sessions': total_sessions,
            'total_duration': total_duration,
            'average_duration': total_duration / total_sessions if total_sessions > 0 else 0,
            'records': [self.mapper.to_dto(record) for record in records]
        }
    
    def get_latest_session(self, baby_id: str) -> Optional[NursingDTO]:
        """获取最新的喂养记录"""
        model_instance = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc()).first()
        
        return self.mapper.to_dto(model_instance) if model_instance else None


class FormulaRepository(BaseRepository[FormulaDTO, 'Formula']):
    """配方奶喂养仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.feeding import Formula
        return Formula
    
    def _get_mapper(self):
        return FormulaMapper
    
    def find_by_baby_id(self, baby_id: str, limit: Optional[int] = None) -> List[FormulaDTO]:
        """根据宝宝ID查找配方奶记录"""
        query = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc())
        
        if limit:
            query = query.limit(limit)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def find_by_date_range(self, baby_id: str, start_date: datetime, end_date: datetime) -> List[FormulaDTO]:
        """根据日期范围查找配方奶记录"""
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
        
        model_instances = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).order_by(self.model_class.time.desc()).all()
        
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def get_daily_total_amount(self, baby_id: str, date: datetime) -> float:
        """获取指定日期的配方奶总量"""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        start_timestamp = start_of_day.timestamp()
        end_timestamp = end_of_day.timestamp()
        
        result = self.db_session.query(func.sum(self.model_class.amount)).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).scalar()
        
        return result or 0.0
    
    def get_weekly_average(self, baby_id: str, end_date: datetime) -> float:
        """获取一周内的平均配方奶量"""
        start_date = end_date - timedelta(days=7)
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
        
        result = self.db_session.query(func.avg(self.model_class.amount)).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).scalar()
        
        return result or 0.0


class FeedingStatsRepository:
    """喂养统计仓储"""
    
    def __init__(self, db_session: Optional[Session] = None):
        from baby_tracker.database import get_db
        self.db_session = db_session or next(get_db())
        self.nursing_repo = NursingRepository(self.db_session)
        self.formula_repo = FormulaRepository(self.db_session)
    
    def get_daily_feeding_stats(self, baby_id: str, date: datetime) -> FeedingStatsDTO:
        """获取指定日期的喂养统计"""
        # 获取母乳喂养统计
        nursing_stats = self.nursing_repo.get_daily_stats(baby_id, date)
        
        # 获取配方奶统计
        formula_records = self.formula_repo.find_by_date_range(
            baby_id, 
            date.replace(hour=0, minute=0, second=0, microsecond=0),
            date.replace(hour=23, minute=59, second=59, microsecond=999999)
        )
        
        total_formula_amount = sum(record.amount for record in formula_records)
        total_formula_sessions = len(formula_records)
        
        return FeedingStatsDTO(
            baby_id=baby_id,
            date=date,
            total_nursing_sessions=nursing_stats['total_sessions'],
            total_nursing_duration=nursing_stats['total_duration'],
            total_formula_amount=total_formula_amount,
            total_formula_sessions=total_formula_sessions,
            average_session_duration=nursing_stats['average_duration']
        )
