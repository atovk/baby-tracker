"""
分析服务 - 使用 dataclasses 进行数据分析和统计
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from baby_tracker.services.baby_service import BabyService
from baby_tracker.services.feeding_service import FeedingService
from baby_tracker.models.dto import (
    BabyDTO, NursingDTO, FormulaDTO, WeightDTO, HeightDTO, TemperatureDTO
)


@dataclass
class FeedingAnalysis:
    """喂养分析结果"""
    period_start: datetime
    period_end: datetime
    total_sessions: int = 0
    daily_average_sessions: float = 0.0
    nursing_percentage: float = 0.0
    formula_percentage: float = 0.0
    peak_feeding_hours: List[int] = field(default_factory=list)
    weekly_trend: List[Dict[str, Any]] = field(default_factory=list)
    
    # 可视化相关数据
    daily_sessions_data: Dict[str, List[int]] = field(default_factory=dict)
    feeding_distribution_data: Dict[str, List[int]] = field(default_factory=dict)


@dataclass
class GrowthAnalysis:
    """生长发育分析结果"""
    period_start: datetime
    period_end: datetime
    weight_start: Optional[float] = None  # 克
    weight_end: Optional[float] = None
    height_start: Optional[float] = None  # 厘米
    height_end: Optional[float] = None
    weight_gain: Optional[float] = None
    height_gain: Optional[float] = None
    weight_percentile: Optional[float] = None
    height_percentile: Optional[float] = None
    
    # 可视化相关数据
    weight_data: Dict[str, List[float]] = field(default_factory=dict)
    height_data: Dict[str, List[float]] = field(default_factory=dict)
    who_standard_weight: Dict[str, List[float]] = field(default_factory=dict)
    who_standard_height: Dict[str, List[float]] = field(default_factory=dict)


@dataclass
class TemperatureAnalysis:
    """体温分析结果"""
    period_start: datetime
    period_end: datetime
    average_temperature: float = 0.0
    max_temperature: float = 0.0
    min_temperature: float = 0.0
    fever_days: int = 0
    fever_percentage: float = 0.0
    
    # 可视化相关数据
    temperature_data: Dict[str, List[float]] = field(default_factory=dict)
    is_fever_data: Dict[str, List[bool]] = field(default_factory=dict)


class AnalyticsService:
    """数据分析服务"""
    
    def __init__(self, db_session=None):
        self.baby_service = BabyService(db_session)
        self.feeding_service = FeedingService(db_session)
    
    def get_feeding_analysis(
        self, 
        baby_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> FeedingAnalysis:
        """获取喂养分析"""
        # 创建分析结果对象
        analysis = FeedingAnalysis(
            period_start=start_date,
            period_end=end_date
        )
        
        # 获取时间范围内的所有喂养记录
        nursing_records = self.feeding_service.get_nursing_records_by_date(
            baby_id, start_date, end_date
        )
        formula_records = self.feeding_service.get_formula_records_by_date(
            baby_id, start_date, end_date
        )
        
        # 基础统计
        total_nursing = len(nursing_records)
        total_formula = len(formula_records)
        total_sessions = total_nursing + total_formula
        analysis.total_sessions = total_sessions
        
        # 计算日均次数
        days = (end_date - start_date).days + 1
        analysis.daily_average_sessions = total_sessions / days if days > 0 else 0
        
        # 计算百分比
        if total_sessions > 0:
            analysis.nursing_percentage = (total_nursing / total_sessions) * 100
            analysis.formula_percentage = (total_formula / total_sessions) * 100
        
        # 分析喂养高峰时间
        feeding_hours = self._analyze_feeding_hours(nursing_records, formula_records)
        analysis.peak_feeding_hours = feeding_hours[:3]  # 取前三个高峰时段
        
        # 准备每日数据用于图表
        analysis.daily_sessions_data = self._prepare_daily_feeding_data(
            baby_id, start_date, end_date
        )
        
        # 准备喂养类型分布数据
        analysis.feeding_distribution_data = {
            'labels': ['母乳', '配方奶'],
            'values': [total_nursing, total_formula]
        }
        
        return analysis
    
    def get_growth_analysis(
        self, 
        baby_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> GrowthAnalysis:
        """获取生长发育分析"""
        # 创建分析结果对象
        analysis = GrowthAnalysis(
            period_start=start_date,
            period_end=end_date
        )
        
        # TODO: 获取体重身高记录并分析
        # 这里需要健康相关的仓储和服务来获取数据
        
        return analysis
    
    def get_temperature_analysis(
        self, 
        baby_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> TemperatureAnalysis:
        """获取体温分析"""
        # 创建分析结果对象
        analysis = TemperatureAnalysis(
            period_start=start_date,
            period_end=end_date
        )
        
        # TODO: 获取体温记录并分析
        # 这里需要健康相关的仓储和服务来获取数据
        
        return analysis
    
    def export_feeding_data(
        self, 
        baby_id: str, 
        start_date: datetime, 
        end_date: datetime, 
        format: str = 'excel'
    ) -> str:
        """导出喂养数据"""
        # 获取宝宝信息
        baby = self.baby_service.get_baby(baby_id)
        if not baby:
            return ""
        
        # 获取喂养记录
        nursing_records = self.feeding_service.get_nursing_records_by_date(
            baby_id, start_date, end_date
        )
        formula_records = self.feeding_service.get_formula_records_by_date(
            baby_id, start_date, end_date
        )
        
        # 转换为DataFrame
        nursing_data = []
        for record in nursing_records:
            nursing_data.append({
                '日期': datetime.fromtimestamp(record.time).strftime('%Y-%m-%d'),
                '时间': datetime.fromtimestamp(record.time).strftime('%H:%M'),
                '喂养类型': '母乳',
                '左侧时长(分钟)': record.left_duration,
                '右侧时长(分钟)': record.right_duration,
                '两侧时长(分钟)': record.both_duration,
                '总时长(分钟)': record.total_duration,
                '结束侧': record.finish_side_display,
                '备注': record.note or ''
            })
        
        formula_data = []
        for record in formula_records:
            formula_data.append({
                '日期': datetime.fromtimestamp(record.time).strftime('%Y-%m-%d'),
                '时间': datetime.fromtimestamp(record.time).strftime('%H:%M'),
                '喂养类型': '配方奶',
                '数量(毫升)': record.amount,
                '备注': record.note or ''
            })
        
        # 合并数据并按时间排序
        all_data = pd.DataFrame(nursing_data + formula_data)
        if not all_data.empty:
            all_data['完整时间'] = pd.to_datetime(all_data['日期'] + ' ' + all_data['时间'])
            all_data = all_data.sort_values(by='完整时间', ascending=False)
            all_data = all_data.drop(columns=['完整时间'])
        
        # 导出文件名
        filename = f"feeding_export_{baby.name}_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}"
        
        # 导出为Excel或CSV
        if format.lower() == 'excel':
            file_path = f"data/exports/{filename}.xlsx"
            try:
                all_data.to_excel(file_path, index=False, engine='openpyxl')
                return file_path
            except Exception as e:
                return f"导出错误: {str(e)}"
        else:
            file_path = f"data/exports/{filename}.csv"
            try:
                all_data.to_csv(file_path, index=False)
                return file_path
            except Exception as e:
                return f"导出错误: {str(e)}"
    
    def _analyze_feeding_hours(
        self, 
        nursing_records: List[NursingDTO], 
        formula_records: List[FormulaDTO]
    ) -> List[int]:
        """分析喂养高峰时段"""
        # 所有喂养记录的小时分布
        hour_count = [0] * 24
        
        # 统计母乳喂养的小时分布
        for record in nursing_records:
            hour = datetime.fromtimestamp(record.time).hour
            hour_count[hour] += 1
        
        # 统计配方奶喂养的小时分布
        for record in formula_records:
            hour = datetime.fromtimestamp(record.time).hour
            hour_count[hour] += 1
        
        # 找出喂养次数最多的时段
        sorted_hours = sorted(
            range(len(hour_count)), 
            key=lambda i: hour_count[i], 
            reverse=True
        )
        
        return sorted_hours
    
    def _prepare_daily_feeding_data(
        self, 
        baby_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, List[Any]]:
        """准备每日喂养数据用于图表"""
        date_labels = []
        nursing_counts = []
        formula_counts = []
        
        current_date = start_date
        while current_date <= end_date:
            # 添加日期标签
            date_labels.append(current_date.strftime('%m-%d'))
            
            # 获取当天喂养统计
            stats = self.feeding_service.get_daily_feeding_stats(baby_id, current_date)
            
            # 添加各类喂养次数
            nursing_counts.append(stats.total_nursing_sessions)
            formula_counts.append(stats.total_formula_sessions)
            
            # 递增天数
            current_date += timedelta(days=1)
        
        return {
            'dates': date_labels,
            'nursing': nursing_counts,
            'formula': formula_counts
        }
    
    def close(self):
        """关闭服务"""
        self.baby_service.close()
        self.feeding_service.close()
