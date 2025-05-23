"""
喂养服务层 - 使用 dataclasses DTO
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
from baby_tracker.models.dto import (
    NursingDTO, FormulaDTO, FeedingStatsDTO, FinishSide
)
from baby_tracker.repositories.feeding_repository import (
    NursingRepository, FormulaRepository, FeedingStatsRepository
)


class FeedingService:
    """喂养服务"""
    
    def __init__(self, db_session=None):
        self.nursing_repository = NursingRepository(db_session)
        self.formula_repository = FormulaRepository(db_session)
        self.feeding_stats_repository = FeedingStatsRepository(db_session)
    
    # ==================== 母乳喂养相关 ====================
    
    def start_nursing_session(
        self,
        baby_id: str,
        start_time: Optional[datetime] = None,
        note: Optional[str] = None
    ) -> NursingDTO:
        """开始母乳喂养"""
        if start_time is None:
            start_time = datetime.now()
        
        nursing_dto = NursingDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            time=start_time.timestamp(),
            note=note,
            has_picture=False,
            finish_side=FinishSide.BOTH_UNKNOWN,
            left_duration=0,
            right_duration=0,
            both_duration=0,
            timestamp=datetime.now().timestamp()
        )
        
        return self.nursing_repository.create(nursing_dto)
    
    def complete_nursing_session(
        self,
        session_id: str,
        finish_side: FinishSide,
        left_duration: int = 0,
        right_duration: int = 0,
        both_duration: int = 0,
        note: Optional[str] = None
    ) -> Optional[NursingDTO]:
        """完成母乳喂养"""
        session = self.nursing_repository.get_by_id(session_id)
        if not session:
            return None
        
        # 更新喂养信息
        session.finish_side = finish_side
        session.left_duration = left_duration
        session.right_duration = right_duration
        session.both_duration = both_duration
        if note:
            session.note = note
        session.timestamp = datetime.now().timestamp()
        
        return self.nursing_repository.update(session_id, session)
    
    def add_nursing_record(
        self,
        baby_id: str,
        feeding_time: datetime,
        finish_side: FinishSide,
        left_duration: int = 0,
        right_duration: int = 0,
        both_duration: int = 0,
        note: Optional[str] = None,
        desc_id: Optional[str] = None
    ) -> NursingDTO:
        """添加母乳喂养记录"""
        nursing_dto = NursingDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            time=feeding_time.timestamp(),
            note=note,
            has_picture=False,
            desc_id=desc_id,
            finish_side=finish_side,
            left_duration=left_duration,
            right_duration=right_duration,
            both_duration=both_duration,
            timestamp=datetime.now().timestamp()
        )
        
        return self.nursing_repository.create(nursing_dto)
    
    def get_nursing_records(
        self, 
        baby_id: str, 
        limit: Optional[int] = None
    ) -> List[NursingDTO]:
        """获取母乳喂养记录"""
        return self.nursing_repository.find_by_baby_id(baby_id, limit)
    
    def get_nursing_records_by_date(
        self,
        baby_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[NursingDTO]:
        """根据日期范围获取母乳喂养记录"""
        return self.nursing_repository.find_by_date_range(baby_id, start_date, end_date)
    
    def get_latest_nursing(self, baby_id: str) -> Optional[NursingDTO]:
        """获取最新的母乳喂养记录"""
        return self.nursing_repository.get_latest_session(baby_id)
    
    # ==================== 配方奶喂养相关 ====================
    
    def add_formula_record(
        self,
        baby_id: str,
        feeding_time: datetime,
        amount: float,
        note: Optional[str] = None,
        desc_id: Optional[str] = None
    ) -> FormulaDTO:
        """添加配方奶喂养记录"""
        formula_dto = FormulaDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            time=feeding_time.timestamp(),
            note=note,
            has_picture=False,
            desc_id=desc_id,
            amount=amount,
            timestamp=datetime.now().timestamp()
        )
        
        return self.formula_repository.create(formula_dto)
    
    def get_formula_records(
        self,
        baby_id: str,
        limit: Optional[int] = None
    ) -> List[FormulaDTO]:
        """获取配方奶喂养记录"""
        return self.formula_repository.find_by_baby_id(baby_id, limit)
    
    def get_formula_records_by_date(
        self,
        baby_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[FormulaDTO]:
        """根据日期范围获取配方奶喂养记录"""
        return self.formula_repository.find_by_date_range(baby_id, start_date, end_date)
    
    def get_daily_formula_amount(self, baby_id: str, date: datetime) -> float:
        """获取指定日期的配方奶总量"""
        return self.formula_repository.get_daily_total_amount(baby_id, date)
    
    # ==================== 喂养统计相关 ====================
    
    def get_daily_feeding_stats(self, baby_id: str, date: datetime) -> FeedingStatsDTO:
        """获取指定日期的喂养统计"""
        return self.feeding_stats_repository.get_daily_feeding_stats(baby_id, date)
    
    def get_weekly_feeding_summary(self, baby_id: str, end_date: datetime) -> Dict[str, Any]:
        """获取一周的喂养总结"""
        start_date = end_date - timedelta(days=7)
        
        # 收集一周的数据
        daily_stats = []
        current_date = start_date
        
        while current_date <= end_date:
            daily_stat = self.get_daily_feeding_stats(baby_id, current_date)
            daily_stats.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'day_of_week': current_date.strftime('%A'),
                'nursing_sessions': daily_stat.total_nursing_sessions,
                'nursing_duration': daily_stat.total_nursing_duration,
                'formula_sessions': daily_stat.total_formula_sessions,
                'formula_amount': daily_stat.total_formula_amount,
                'total_sessions': daily_stat.total_feeding_sessions,
            })
            current_date += timedelta(days=1)
        
        # 计算周总结
        total_nursing_sessions = sum(day['nursing_sessions'] for day in daily_stats)
        total_nursing_duration = sum(day['nursing_duration'] for day in daily_stats)
        total_formula_sessions = sum(day['formula_sessions'] for day in daily_stats)
        total_formula_amount = sum(day['formula_amount'] for day in daily_stats)
        total_sessions = sum(day['total_sessions'] for day in daily_stats)
        
        return {
            'period': f"{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}",
            'daily_breakdown': daily_stats,
            'weekly_summary': {
                'total_nursing_sessions': total_nursing_sessions,
                'average_daily_nursing_sessions': total_nursing_sessions / 7,
                'total_nursing_duration': total_nursing_duration,
                'average_daily_nursing_duration': total_nursing_duration / 7,
                'total_formula_sessions': total_formula_sessions,
                'average_daily_formula_sessions': total_formula_sessions / 7,
                'total_formula_amount': total_formula_amount,
                'average_daily_formula_amount': total_formula_amount / 7,
                'total_feeding_sessions': total_sessions,
                'average_daily_sessions': total_sessions / 7,
            }
        }
    
    def get_feeding_patterns(self, baby_id: str, days: int = 7) -> Dict[str, Any]:
        """分析喂养模式"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取所有喂养记录
        nursing_records = self.get_nursing_records_by_date(baby_id, start_date, end_date)
        formula_records = self.get_formula_records_by_date(baby_id, start_date, end_date)
        
        # 分析喂养时间模式
        nursing_hours = [datetime.fromtimestamp(record.time).hour for record in nursing_records]
        formula_hours = [datetime.fromtimestamp(record.time).hour for record in formula_records]
        
        # 统计每小时的喂养次数
        hourly_nursing = {hour: nursing_hours.count(hour) for hour in range(24)}
        hourly_formula = {hour: formula_hours.count(hour) for hour in range(24)}
        
        # 找出最常见的喂养时间
        peak_nursing_hours = sorted(hourly_nursing.keys(), key=lambda x: hourly_nursing[x], reverse=True)[:3]
        peak_formula_hours = sorted(hourly_formula.keys(), key=lambda x: hourly_formula[x], reverse=True)[:3]
        
        # 计算喂养间隔
        nursing_intervals = []
        for i in range(1, len(nursing_records)):
            interval = nursing_records[i-1].time - nursing_records[i].time
            nursing_intervals.append(abs(interval) / 3600)  # 转换为小时
        
        avg_nursing_interval = sum(nursing_intervals) / len(nursing_intervals) if nursing_intervals else 0
        
        return {
            'analysis_period': f"{days}天",
            'total_nursing_sessions': len(nursing_records),
            'total_formula_sessions': len(formula_records),
            'peak_nursing_hours': [f"{hour:02d}:00" for hour in peak_nursing_hours],
            'peak_formula_hours': [f"{hour:02d}:00" for hour in peak_formula_hours],
            'average_nursing_interval_hours': round(avg_nursing_interval, 2),
            'hourly_nursing_distribution': hourly_nursing,
            'hourly_formula_distribution': hourly_formula,
        }
    
    def update_feeding_record(
        self,
        record_id: str,
        record_type: str,  # 'nursing' or 'formula'
        **kwargs
    ) -> Optional[Any]:
        """更新喂养记录"""
        if record_type == 'nursing':
            record = self.nursing_repository.get_by_id(record_id)
            if record:
                for key, value in kwargs.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                record.timestamp = datetime.now().timestamp()
                return self.nursing_repository.update(record_id, record)
        elif record_type == 'formula':
            record = self.formula_repository.get_by_id(record_id)
            if record:
                for key, value in kwargs.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                record.timestamp = datetime.now().timestamp()
                return self.formula_repository.update(record_id, record)
        
        return None
    
    def delete_feeding_record(self, record_id: str, record_type: str) -> bool:
        """删除喂养记录"""
        if record_type == 'nursing':
            return self.nursing_repository.delete(record_id)
        elif record_type == 'formula':
            return self.formula_repository.delete(record_id)
        return False
    
    def close(self):
        """关闭服务"""
        self.nursing_repository.close()
        self.formula_repository.close()
        self.feeding_stats_repository.db_session.close()
