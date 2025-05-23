"""
Baby Tracker 使用示例

这个脚本展示了如何使用 Baby Tracker 的分层架构和 dataclasses
"""
from datetime import datetime, timedelta
import uuid

# 导入服务和DTO
from baby_tracker.models.dto import (
    BabyDTO, NursingDTO, FormulaDTO, Gender, FinishSide
)
from baby_tracker.services.baby_service import BabyService
from baby_tracker.services.feeding_service import FeedingService
from baby_tracker.services.analytics_service import AnalyticsService
from baby_tracker.services.export_service import ExportService, ExportRequest


def demo_baby_creation():
    """演示如何创建宝宝记录"""
    baby_service = BabyService()
    
    # 使用服务层创建宝宝
    baby = baby_service.create_baby(
        name="小明",
        dob=datetime(2024, 5, 1),  # 出生日期
        gender=Gender.MALE,        # 使用枚举值
    )
    
    print(f"\n创建了宝宝记录: {baby.name}")
    print(f"出生日期: {datetime.fromtimestamp(baby.dob).strftime('%Y-%m-%d')}")
    print(f"性别: {baby.gender_display}")
    print(f"年龄: {baby.age_in_days}天 ({baby.age_in_weeks}周)")
    
    # 不要忘记关闭服务
    baby_service.close()
    
    return baby.id


def demo_feeding_records(baby_id: str):
    """演示如何创建和查询喂养记录"""
    feeding_service = FeedingService()
    
    # 添加一些母乳喂养记录
    now = datetime.now()
    
    # 前天的喂养记录
    two_days_ago = now - timedelta(days=2)
    for hour in [8, 11, 14, 17, 20, 23]:
        feeding_time = two_days_ago.replace(hour=hour, minute=0)
        feeding_service.add_nursing_record(
            baby_id=baby_id,
            feeding_time=feeding_time,
            finish_side=FinishSide.LEFT if hour % 2 == 0 else FinishSide.RIGHT,
            left_duration=10 if hour % 2 == 0 else 5,
            right_duration=5 if hour % 2 == 0 else 10,
            note=f"喂养记录 {feeding_time.strftime('%H:%M')}"
        )
    
    # 昨天的喂养记录
    yesterday = now - timedelta(days=1)
    for hour in [8, 11, 14, 17, 20, 23]:
        feeding_time = yesterday.replace(hour=hour, minute=0)
        
        # 偶数小时添加母乳喂养
        if hour % 2 == 0:
            feeding_service.add_nursing_record(
                baby_id=baby_id,
                feeding_time=feeding_time,
                finish_side=FinishSide.BOTH_UNKNOWN,
                left_duration=8,
                right_duration=8,
                note=f"两侧喂养 {feeding_time.strftime('%H:%M')}"
            )
        # 奇数小时添加配方奶
        else:
            feeding_service.add_formula_record(
                baby_id=baby_id,
                feeding_time=feeding_time,
                amount=100.0,  # 毫升
                note=f"配方奶 {feeding_time.strftime('%H:%M')}"
            )
    
    # 今天的喂养记录
    for hour in range(8, 18, 3):
        feeding_time = now.replace(hour=hour, minute=0)
        if hour < 12:
            feeding_service.add_nursing_record(
                baby_id=baby_id,
                feeding_time=feeding_time,
                finish_side=FinishSide.LEFT,
                left_duration=12,
                right_duration=8,
                note=f"今日喂养 {feeding_time.strftime('%H:%M')}"
            )
        else:
            feeding_service.add_formula_record(
                baby_id=baby_id,
                feeding_time=feeding_time,
                amount=120.0,  # 毫升
                note=f"今日配方奶 {feeding_time.strftime('%H:%M')}"
            )
    
    # 查询最近的喂养记录
    nursing_records = feeding_service.get_nursing_records(baby_id, limit=5)
    formula_records = feeding_service.get_formula_records(baby_id, limit=5)
    
    print("\n最近的母乳喂养记录:")
    for record in nursing_records:
        time_str = datetime.fromtimestamp(record.time).strftime('%Y-%m-%d %H:%M')
        print(f"- {time_str}: 左侧 {record.left_duration}分钟, 右侧 {record.right_duration}分钟")
    
    print("\n最近的配方奶喂养记录:")
    for record in formula_records:
        time_str = datetime.fromtimestamp(record.time).strftime('%Y-%m-%d %H:%M')
        print(f"- {time_str}: {record.amount}毫升")
    
    # 获取今日喂养统计
    today_stats = feeding_service.get_daily_feeding_stats(baby_id, now)
    print(f"\n今日喂养统计:")
    print(f"- 母乳次数: {today_stats.total_nursing_sessions}")
    print(f"- 母乳总时长: {today_stats.total_nursing_duration}分钟")
    print(f"- 配方奶次数: {today_stats.total_formula_sessions}")
    print(f"- 配方奶总量: {today_stats.total_formula_amount}毫升")
    
    # 不要忘记关闭服务
    feeding_service.close()


def demo_analytics(baby_id: str):
    """演示如何使用分析服务"""
    analytics_service = AnalyticsService()
    
    # 分析最近3天的喂养数据
    now = datetime.now()
    start_date = now - timedelta(days=3)
    end_date = now
    
    print(f"\n分析 {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} 的喂养数据")
    
    # 获取喂养分析
    feeding_analysis = analytics_service.get_feeding_analysis(baby_id, start_date, end_date)
    
    print(f"\n喂养分析结果:")
    print(f"- 总喂养次数: {feeding_analysis.total_sessions}")
    print(f"- 日均喂养次数: {feeding_analysis.daily_average_sessions:.1f}")
    print(f"- 母乳占比: {feeding_analysis.nursing_percentage:.1f}%")
    print(f"- 配方奶占比: {feeding_analysis.formula_percentage:.1f}%")
    
    # 打印高峰喂养时段
    peak_hours = [f"{hour:02d}:00" for hour in feeding_analysis.peak_feeding_hours[:3]]
    print(f"- 高峰喂养时段: {', '.join(peak_hours)}")
    
    # 导出喂养数据
    export_path = analytics_service.export_feeding_data(
        baby_id, start_date, end_date, format='excel'
    )
    print(f"\n喂养数据已导出到: {export_path}")
    
    # 不要忘记关闭服务
    analytics_service.close()


def demo_export(baby_id: str):
    """演示如何使用导出服务"""
    export_service = ExportService()
    
    # 创建导出请求
    now = datetime.now()
    export_request = ExportRequest(
        baby_id=baby_id,
        start_date=now - timedelta(days=3),
        end_date=now,
        format="excel",
        include_feeding=True,
        include_sleep=True,
        include_diaper=True,
        include_growth=True,
        filename="宝宝数据完整导出"
    )
    
    # 执行导出
    result = export_service.export_baby_data(export_request)
    
    if result.success:
        print(f"\n导出成功:")
        print(f"- 文件路径: {result.file_path}")
        print(f"- 文件大小: {result.file_size} 字节")
        print(f"- 记录数量: {result.record_count}")
        print(f"- 导出时间: {result.export_date.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"\n导出失败: {result.error_message}")
    
    # 不要忘记关闭服务
    export_service.close()


def run_demo():
    """运行完整示例"""
    print("=" * 50)
    print("Baby Tracker 使用示例")
    print("=" * 50)
    
    # 创建宝宝记录
    baby_id = demo_baby_creation()
    
    # 添加喂养记录
    demo_feeding_records(baby_id)
    
    # 分析数据
    demo_analytics(baby_id)
    
    # 导出数据
    demo_export(baby_id)
    
    print("\n" + "=" * 50)
    print("示例结束")
    print("=" * 50)


if __name__ == "__main__":
    run_demo()
