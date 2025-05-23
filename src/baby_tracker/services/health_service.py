"""
健康服务 - 提供健康相关的业务逻辑
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
from sqlalchemy.orm import Session
from baby_tracker.models.dto import (
    SleepDTO, DiaperDTO, WeightDTO, HeightDTO, HeadDTO, TemperatureDTO,
    GrowthStatsDTO
)
from baby_tracker.repositories import (
    SleepRepository, DiaperRepository, WeightRepository,
    HeightRepository, HeadRepository, TemperatureRepository
)


class HealthService:
    """健康服务"""
    
    def __init__(self, db_session: Optional[Session] = None):
        from baby_tracker.database import get_db
        self.db_session = db_session or next(get_db())
        self.sleep_repo = SleepRepository(self.db_session)
        self.diaper_repo = DiaperRepository(self.db_session)
        self.weight_repo = WeightRepository(self.db_session)
        self.height_repo = HeightRepository(self.db_session)
        self.head_repo = HeadRepository(self.db_session)
        self.temp_repo = TemperatureRepository(self.db_session)
    
    # Sleep 相关方法
    def add_sleep_record(self, baby_id: str, duration: int, desc_id: Optional[str] = None, 
                        note: Optional[str] = None, time: Optional[float] = None) -> SleepDTO:
        """添加睡眠记录"""
        sleep_dto = SleepDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            duration=duration,
            desc_id=desc_id,
            note=note,
            time=time or datetime.now().timestamp()
        )
        
        return self.sleep_repo.create(sleep_dto)
    
    def get_sleep_records(self, baby_id: str, limit: Optional[int] = None) -> List[SleepDTO]:
        """获取宝宝的睡眠记录"""
        return self.sleep_repo.find_by_baby_id(baby_id, limit)
    
    def get_sleep_stats(self, baby_id: str, days: int = 7) -> Dict[str, Any]:
        """获取睡眠统计数据"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取日期范围内的所有睡眠记录
        sleep_records = self.sleep_repo.find_by_date_range(baby_id, start_date, end_date)
        
        # 计算每天的睡眠时长
        daily_sleep = {}
        for record in sleep_records:
            day = datetime.fromtimestamp(record.time).strftime('%Y-%m-%d')
            daily_sleep[day] = daily_sleep.get(day, 0) + record.duration
        
        # 计算统计数据
        total_sleep = sum(daily_sleep.values())
        avg_sleep = total_sleep / len(daily_sleep) if daily_sleep else 0
        
        return {
            'daily_sleep': daily_sleep,
            'total_sleep_minutes': total_sleep,
            'avg_sleep_minutes': avg_sleep,
            'record_count': len(sleep_records)
        }
    
    # Diaper 相关方法
    def add_diaper_record(self, baby_id: str, desc_id: Optional[str] = None,
                         note: Optional[str] = None, time: Optional[float] = None) -> DiaperDTO:
        """添加尿布记录"""
        diaper_dto = DiaperDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            desc_id=desc_id,
            note=note,
            time=time or datetime.now().timestamp()
        )
        
        return self.diaper_repo.create(diaper_dto)
    
    def get_diaper_records(self, baby_id: str, limit: Optional[int] = None) -> List[DiaperDTO]:
        """获取宝宝的尿布记录"""
        return self.diaper_repo.find_by_baby_id(baby_id, limit)
    
    def get_diaper_stats(self, baby_id: str, days: int = 7) -> Dict[str, Any]:
        """获取尿布统计数据"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取日期范围内的所有尿布记录
        diaper_records = self.diaper_repo.find_by_date_range(baby_id, start_date, end_date)
        
        # 按日期和类型分组
        daily_diapers = {}
        for record in diaper_records:
            day = datetime.fromtimestamp(record.time).strftime('%Y-%m-%d')
            if day not in daily_diapers:
                daily_diapers[day] = {'total': 0, 'by_type': {}}
            
            daily_diapers[day]['total'] += 1
            
            desc_id = record.desc_id or 'unknown'
            daily_diapers[day]['by_type'][desc_id] = daily_diapers[day]['by_type'].get(desc_id, 0) + 1
        
        # 计算统计数据
        total_count = len(diaper_records)
        avg_daily = total_count / days
        
        return {
            'daily_diapers': daily_diapers,
            'total_count': total_count,
            'avg_daily': avg_daily
        }
    
    # Weight 相关方法
    def add_weight_record(self, baby_id: str, weight: float, 
                         note: Optional[str] = None, time: Optional[float] = None) -> WeightDTO:
        """添加体重记录"""
        weight_dto = WeightDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            weight=weight,
            note=note,
            time=time or datetime.now().timestamp()
        )
        
        return self.weight_repo.create(weight_dto)
    
    def get_weight_records(self, baby_id: str, limit: Optional[int] = None) -> List[WeightDTO]:
        """获取宝宝的体重记录"""
        return self.weight_repo.find_by_baby_id(baby_id, limit)
    
    def get_weight_trend(self, baby_id: str, days: int = 90) -> Dict[str, Any]:
        """获取体重趋势"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取日期范围内的所有体重记录
        weight_records = self.weight_repo.find_by_date_range(baby_id, start_date, end_date)
        
        # 构建趋势数据
        trend_data = {}
        for record in sorted(weight_records, key=lambda r: r.time):
            day = datetime.fromtimestamp(record.time).strftime('%Y-%m-%d')
            trend_data[day] = record.weight
        
        # 计算增长情况
        weight_gain = self.weight_repo.calculate_weight_gain(baby_id, days)
        latest_weight = self.weight_repo.get_latest_weight(baby_id)
        
        return {
            'trend_data': trend_data,
            'weight_gain_grams': weight_gain,
            'weight_gain_kg': weight_gain / 1000 if weight_gain else 0,
            'latest_weight': latest_weight.weight if latest_weight else None
        }
    
    # Height 相关方法
    def add_height_record(self, baby_id: str, height: float, 
                         note: Optional[str] = None, time: Optional[float] = None) -> HeightDTO:
        """添加身高记录"""
        height_dto = HeightDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            height=height,
            note=note,
            time=time or datetime.now().timestamp()
        )
        
        return self.height_repo.create(height_dto)
    
    def get_height_records(self, baby_id: str, limit: Optional[int] = None) -> List[HeightDTO]:
        """获取宝宝的身高记录"""
        return self.height_repo.find_by_baby_id(baby_id, limit)
    
    # Head 相关方法
    def add_head_record(self, baby_id: str, head: float, 
                       note: Optional[str] = None, time: Optional[float] = None) -> HeadDTO:
        """添加头围记录"""
        head_dto = HeadDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            head=head,
            note=note,
            time=time or datetime.now().timestamp()
        )
        
        return self.head_repo.create(head_dto)
    
    def get_head_records(self, baby_id: str, limit: Optional[int] = None) -> List[HeadDTO]:
        """获取宝宝的头围记录"""
        return self.head_repo.find_by_baby_id(baby_id, limit)
    
    # Temperature 相关方法
    def add_temperature_record(self, baby_id: str, temperature: float, 
                              location: Optional[str] = None,
                              note: Optional[str] = None, 
                              time: Optional[float] = None) -> TemperatureDTO:
        """添加体温记录"""
        temp_dto = TemperatureDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            temperature=temperature,
            location=location,
            note=note,
            time=time or datetime.now().timestamp()
        )
        
        return self.temp_repo.create(temp_dto)
    
    def get_temperature_records(self, baby_id: str, limit: Optional[int] = None) -> List[TemperatureDTO]:
        """获取宝宝的体温记录"""
        return self.temp_repo.find_by_baby_id(baby_id, limit)
    
    def get_fever_history(self, baby_id: str, days: int = 90) -> List[TemperatureDTO]:
        """获取发烧历史记录"""
        return self.temp_repo.find_fever_records(baby_id, days)
    
    # 综合健康数据
    def get_growth_stats(self, baby_id: str) -> GrowthStatsDTO:
        """获取成长统计数据"""
        # 获取最新的身高、体重和头围记录
        latest_weight = self.weight_repo.get_latest_weight(baby_id)
        latest_height = self.height_repo.get_latest_height(baby_id)
        latest_head = self.head_repo.get_latest_head(baby_id)
        
        # 确定趋势（需要查询更多记录来确定）
        weight_trend = "stable"  # 默认
        if latest_weight:
            weight_gain = self.weight_repo.calculate_weight_gain(baby_id, 30)
            if weight_gain > 500:  # 一个月增长500g以上
                weight_trend = "increasing"
            elif weight_gain < 0:
                weight_trend = "decreasing"
        
        height_trend = "stable"  # 默认
        
        return GrowthStatsDTO(
            baby_id=baby_id,
            latest_weight=latest_weight.weight if latest_weight else None,
            latest_height=latest_height.height if latest_height else None,
            latest_head=latest_head.head if latest_head else None,
            weight_trend=weight_trend,
            height_trend=height_trend
        )
