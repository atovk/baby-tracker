"""
宝宝服务层 - 使用 dataclasses DTO
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
from baby_tracker.models.dto import BabyDTO, Gender
from baby_tracker.repositories.baby_repository import BabyRepository
from baby_tracker.repositories.feeding_repository import FeedingStatsRepository


class BabyService:
    """宝宝信息服务"""
    
    def __init__(self, db_session=None):
        self.baby_repository = BabyRepository(db_session)
        self.feeding_stats_repository = FeedingStatsRepository(db_session)
    
    def create_baby(
        self, 
        name: str, 
        dob: datetime, 
        gender: Gender,
        due_day: Optional[str] = None,
        picture: Optional[str] = None
    ) -> BabyDTO:
        """创建新宝宝"""
        baby_dto = BabyDTO(
            id=str(uuid.uuid4()),
            name=name,
            dob=dob.timestamp(),
            due_day=due_day,
            gender=gender,
            picture=picture,
            timestamp=datetime.now().timestamp()
        )
        
        return self.baby_repository.create(baby_dto)
    
    def get_baby(self, baby_id: str) -> Optional[BabyDTO]:
        """获取宝宝信息"""
        return self.baby_repository.get_by_id(baby_id)
    
    def get_all_babies(self) -> List[BabyDTO]:
        """获取所有宝宝"""
        return self.baby_repository.get_all()
    
    def update_baby(
        self, 
        baby_id: str, 
        name: Optional[str] = None,
        due_day: Optional[str] = None,
        picture: Optional[str] = None
    ) -> Optional[BabyDTO]:
        """更新宝宝信息"""
        baby = self.baby_repository.get_by_id(baby_id)
        if not baby:
            return None
        
        # 更新字段
        if name is not None:
            baby.name = name
        if due_day is not None:
            baby.due_day = due_day
        if picture is not None:
            baby.picture = picture
        
        baby.timestamp = datetime.now().timestamp()
        
        return self.baby_repository.update(baby_id, baby)
    
    def delete_baby(self, baby_id: str) -> bool:
        """删除宝宝"""
        return self.baby_repository.delete(baby_id)
    
    def search_babies(self, query: str) -> List[BabyDTO]:
        """搜索宝宝"""
        return self.baby_repository.find_by_name(query)
    
    def get_babies_by_gender(self, gender: Gender) -> List[BabyDTO]:
        """根据性别获取宝宝"""
        return self.baby_repository.find_by_gender(gender.value)
    
    def get_babies_by_age_range(self, min_days: int, max_days: int) -> List[BabyDTO]:
        """根据年龄范围获取宝宝"""
        return self.baby_repository.find_babies_by_age_range(min_days, max_days)
    
    def get_baby_dashboard(self, baby_id: str) -> Dict[str, Any]:
        """获取宝宝仪表板数据"""
        baby = self.get_baby(baby_id)
        if not baby:
            return {}
        
        today = datetime.now()
        
        # 获取今日喂养统计
        today_feeding_stats = self.feeding_stats_repository.get_daily_feeding_stats(
            baby_id, today
        )
        
        # 计算基本信息
        dashboard_data = {
            'baby_info': {
                'id': baby.id,
                'name': baby.name,
                'age_days': baby.age_in_days,
                'age_weeks': baby.age_in_weeks,
                'age_months': baby.age_in_months,
                'gender': baby.gender_display,
                'birth_date': baby.birth_date.strftime('%Y-%m-%d'),
            },
            'today_stats': {
                'total_feeding_sessions': today_feeding_stats.total_feeding_sessions,
                'nursing_sessions': today_feeding_stats.total_nursing_sessions,
                'nursing_duration': today_feeding_stats.total_nursing_duration,
                'formula_sessions': today_feeding_stats.total_formula_sessions,
                'formula_amount': today_feeding_stats.total_formula_amount,
                'average_session_duration': today_feeding_stats.average_session_duration,
            },
            'milestones': self._calculate_milestones(baby),
        }
        
        return dashboard_data
    
    def _calculate_milestones(self, baby: BabyDTO) -> Dict[str, Any]:
        """计算宝宝里程碑"""
        age_days = baby.age_in_days
        
        milestones = {
            'age_category': self._get_age_category(age_days),
            'upcoming_milestones': self._get_upcoming_milestones(age_days),
            'development_stage': self._get_development_stage(age_days),
        }
        
        return milestones
    
    def _get_age_category(self, age_days: int) -> str:
        """获取年龄分类"""
        if age_days < 0:
            return "未出生"
        elif age_days <= 28:
            return "新生儿期"
        elif age_days <= 365:
            return "婴儿期"
        elif age_days <= 1095:  # 3年
            return "幼儿期"
        else:
            return "学前期"
    
    def _get_upcoming_milestones(self, age_days: int) -> List[str]:
        """获取即将到来的里程碑"""
        milestones = []
        
        milestone_map = {
            7: "一周大了！",
            14: "两周大了！",
            30: "满月了！",
            60: "两个月大了！",
            90: "三个月大了！",
            180: "半岁了！",
            365: "一岁生日！",
            730: "两岁生日！",
        }
        
        for days, milestone in milestone_map.items():
            if age_days < days <= age_days + 7:  # 接下来一周内的里程碑
                milestones.append(f"{days - age_days}天后：{milestone}")
        
        return milestones
    
    def _get_development_stage(self, age_days: int) -> str:
        """获取发育阶段"""
        if age_days < 0:
            return "胎儿期"
        elif age_days <= 7:
            return "新生儿早期"
        elif age_days <= 28:
            return "新生儿晚期"
        elif age_days <= 90:
            return "婴儿早期"
        elif age_days <= 180:
            return "婴儿中期"
        elif age_days <= 365:
            return "婴儿晚期"
        elif age_days <= 730:
            return "幼儿早期"
        else:
            return "幼儿期"
    
    def get_baby_statistics(self, baby_id: str, days: int = 30) -> Dict[str, Any]:
        """获取宝宝统计数据"""
        baby = self.get_baby(baby_id)
        if not baby:
            return {}
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 收集指定时间段的统计数据
        daily_stats = []
        current_date = start_date
        
        while current_date <= end_date:
            daily_feeding_stats = self.feeding_stats_repository.get_daily_feeding_stats(
                baby_id, current_date
            )
            daily_stats.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'feeding_sessions': daily_feeding_stats.total_feeding_sessions,
                'nursing_duration': daily_feeding_stats.total_nursing_duration,
                'formula_amount': daily_feeding_stats.total_formula_amount,
            })
            current_date += timedelta(days=1)
        
        # 计算总体统计
        total_sessions = sum(day['feeding_sessions'] for day in daily_stats)
        total_nursing_duration = sum(day['nursing_duration'] for day in daily_stats)
        total_formula_amount = sum(day['formula_amount'] for day in daily_stats)
        
        return {
            'period': f"{days}天",
            'daily_stats': daily_stats,
            'summary': {
                'total_feeding_sessions': total_sessions,
                'average_daily_sessions': total_sessions / days,
                'total_nursing_duration': total_nursing_duration,
                'average_daily_nursing': total_nursing_duration / days,
                'total_formula_amount': total_formula_amount,
                'average_daily_formula': total_formula_amount / days,
            }
        }
    
    def close(self):
        """关闭服务"""
        self.baby_repository.close()
        self.feeding_stats_repository.db_session.close()
