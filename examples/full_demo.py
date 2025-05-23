#!/usr/bin/env python
"""
全功能演示脚本 - 展示宝宝追踪器的完整功能
"""
import sys
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from baby_tracker.database import engine, get_db
from baby_tracker.models.dto import (
    BabyDTO, NursingDTO, FormulaDTO, SleepDTO, DiaperDTO, 
    WeightDTO, HeightDTO, HeadDTO, TemperatureDTO, Gender, FinishSide,
    PlaytimeDTO, BathDTO, PhotoDTO, VideoDTO
)
from baby_tracker.services import (
    BabyService, FeedingService, HealthService, ActivityService, 
    AnalyticsService, ExportService, ExportRequest
)


def create_demo_data():
    """创建演示数据"""
    db = next(get_db())
    
    try:
        # 创建服务实例
        baby_service = BabyService(db)
        feeding_service = FeedingService(db)
        health_service = HealthService(db)
        activity_service = ActivityService(db)
        analytics_service = AnalyticsService(db)
        export_service = ExportService(db)
        
        print("===== 创建宝宝记录 =====")
        # 创建宝宝记录
        baby_id = str(uuid.uuid4())
        dob = (datetime.now() - timedelta(days=60)).timestamp()
        baby = baby_service.create_baby(
            name="小明",
            dob=datetime.fromtimestamp(dob),
            gender=Gender.MALE
        )
        print(f"创建宝宝记录: {baby.name}, ID: {baby.id}, 年龄: {baby.age_in_days} 天")
        baby_id = baby.id
        
        print("\n===== 创建喂养记录 =====")
        # 创建一周的喂养记录
        now = datetime.now()
        
        # 每天8次母乳喂养，4次配方奶
        for day in range(7):
            day_date = now - timedelta(days=day)
            
            # 母乳喂养
            for hour in [2, 5, 8, 11, 14, 17, 20, 23]:
                feed_time = day_date.replace(hour=hour, minute=0)
                left_duration = 5 + (day % 3)  # 5-7分钟
                right_duration = 6 + (day % 4)  # 6-9分钟
                
                nursing = feeding_service.add_nursing(
                    baby_id=baby_id,
                    left_duration=left_duration,
                    right_duration=right_duration,
                    time=feed_time.timestamp(),
                    note=f"{feed_time.strftime('%Y-%m-%d %H:%M')} 的喂养记录"
                )
                print(f"添加母乳喂养记录: {feed_time.strftime('%Y-%m-%d %H:%M')}, 左侧: {left_duration}分钟, 右侧: {right_duration}分钟")
            
            # 配方奶
            for hour in [6, 12, 18, 24]:
                feed_time = day_date.replace(hour=hour if hour < 24 else 0, minute=30)
                if hour == 24:
                    feed_time += timedelta(days=1)
                
                amount = 90 + (day % 4) * 10  # 90-120ml
                
                formula = feeding_service.add_formula(
                    baby_id=baby_id,
                    amount=amount,
                    time=feed_time.timestamp(),
                    note=f"{feed_time.strftime('%Y-%m-%d %H:%M')} 的配方奶"
                )
                print(f"添加配方奶记录: {feed_time.strftime('%Y-%m-%d %H:%M')}, 数量: {amount}ml")
        
        print("\n===== 创建健康记录 =====")
        # 创建健康记录
        
        # 睡眠记录 - 每天5次
        for day in range(7):
            day_date = now - timedelta(days=day)
            
            # 夜间长睡
            sleep_start = day_date.replace(hour=0, minute=0)
            sleep_duration = 360  # 6小时
            sleep = health_service.add_sleep_record(
                baby_id=baby_id,
                duration=sleep_duration,
                time=sleep_start.timestamp(),
                note="夜间长睡"
            )
            print(f"添加睡眠记录: {sleep_start.strftime('%Y-%m-%d %H:%M')}, 时长: {sleep_duration}分钟")
            
            # 白天小睡4次
            for hour in [9, 13, 16, 19]:
                sleep_time = day_date.replace(hour=hour, minute=30)
                sleep_duration = 30 + (day % 3) * 15  # 30-60分钟
                
                sleep = health_service.add_sleep_record(
                    baby_id=baby_id,
                    duration=sleep_duration,
                    time=sleep_time.timestamp(),
                    note="白天小睡"
                )
                print(f"添加睡眠记录: {sleep_time.strftime('%Y-%m-%d %H:%M')}, 时长: {sleep_duration}分钟")
        
        # 尿布记录 - 每天8次
        for day in range(7):
            day_date = now - timedelta(days=day)
            
            for hour in [3, 6, 9, 12, 15, 18, 21, 24]:
                diaper_time = day_date.replace(hour=hour if hour < 24 else 0, minute=15)
                if hour == 24:
                    diaper_time += timedelta(days=1)
                
                diaper = health_service.add_diaper_record(
                    baby_id=baby_id,
                    time=diaper_time.timestamp(),
                    desc_id=str((day + hour) % 3 + 1),  # 1-3
                    note=f"尿布更换 {diaper_time.strftime('%H:%M')}"
                )
                print(f"添加尿布记录: {diaper_time.strftime('%Y-%m-%d %H:%M')}")
        
        # 体重记录 - 每周2次
        for day in [1, 4]:
            weight_time = now - timedelta(days=day)
            weight_value = 4200 + day * 30  # 从4200克开始，每次增加30克
            
            weight = health_service.add_weight_record(
                baby_id=baby_id,
                weight=weight_value,
                time=weight_time.timestamp(),
                note=f"体重测量: {weight_value}克"
            )
            print(f"添加体重记录: {weight_time.strftime('%Y-%m-%d')}, 体重: {weight_value}克")
        
        # 身高记录 - 每周1次
        height_time = now - timedelta(days=3)
        height_value = 58.5  # 厘米
        
        height = health_service.add_height_record(
            baby_id=baby_id,
            height=height_value,
            time=height_time.timestamp(),
            note=f"身高测量: {height_value}厘米"
        )
        print(f"添加身高记录: {height_time.strftime('%Y-%m-%d')}, 身高: {height_value}厘米")
        
        # 体温记录 - 每天2次
        for day in range(3):
            day_date = now - timedelta(days=day)
            
            for hour in [8, 20]:
                temp_time = day_date.replace(hour=hour, minute=0)
                temp_value = 36.5 + (day * 0.1) if day < 2 else 37.6  # 第三天发烧
                
                temp = health_service.add_temperature_record(
                    baby_id=baby_id,
                    temperature=temp_value,
                    location="腋下",
                    time=temp_time.timestamp(),
                    note="正常体温" if temp_value < 37.5 else "发烧了！"
                )
                print(f"添加体温记录: {temp_time.strftime('%Y-%m-%d %H:%M')}, 体温: {temp_value}°C")
        
        print("\n===== 创建活动记录 =====")
        # 创建活动记录
        
        # 游戏记录
        for day in range(5):
            day_date = now - timedelta(days=day)
            play_time = day_date.replace(hour=10, minute=30)
            play_duration = 20 + day * 5  # 20-40分钟
            
            play = activity_service.add_playtime_record(
                baby_id=baby_id,
                duration=play_duration,
                play_type="积木" if day % 2 == 0 else "玩具",
                time=play_time.timestamp(),
                note=f"快乐游戏时间，玩了{play_duration}分钟"
            )
            print(f"添加游戏记录: {play_time.strftime('%Y-%m-%d %H:%M')}, 时长: {play_duration}分钟, 类型: {'积木' if day % 2 == 0 else '玩具'}")
        
        # 洗澡记录
        for day in [0, 2, 4, 6]:
            day_date = now - timedelta(days=day)
            bath_time = day_date.replace(hour=19, minute=0)
            
            bath = activity_service.add_bath_record(
                baby_id=baby_id,
                duration=15,
                water_temperature=38.5,
                time=bath_time.timestamp(),
                note="愉快的洗澡时间"
            )
            print(f"添加洗澡记录: {bath_time.strftime('%Y-%m-%d %H:%M')}, 水温: 38.5°C")
        
        print("\n===== 分析数据 =====")
        # 数据分析
        
        # 喂养分析
        feeding_analysis = analytics_service.analyze_feeding(baby_id, days=7)
        print(f"喂养分析结果:")
        print(f"- 平均每日母乳次数: {feeding_analysis.avg_nursing_sessions_per_day}")
        print(f"- 平均每日奶量: {feeding_analysis.avg_formula_per_day}ml")
        print(f"- 总奶量: {feeding_analysis.total_formula_amount}ml")
        
        # 成长分析
        growth_analysis = analytics_service.analyze_growth(baby_id, days=30)
        print(f"\n成长分析结果:")
        print(f"- 当前体重: {growth_analysis.current_weight}克")
        print(f"- 当前身高: {growth_analysis.current_height}厘米")
        print(f"- 30天体重增长: {growth_analysis.weight_gain}克")
        
        # 健康分析
        health_analysis = analytics_service.analyze_health(baby_id, days=7)
        print(f"\n健康分析结果:")
        print(f"- 平均每日睡眠: {health_analysis.avg_daily_sleep_minutes}分钟")
        print(f"- 平均每日尿布次数: {health_analysis.avg_daily_diaper_count}次")
        print(f"- 是否有发烧: {'是' if health_analysis.has_fever else '否'}")
        
        print("\n===== 导出数据 =====")
        # 导出数据
        export_dir = os.path.join(project_root, "data", "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # 定义导出请求
        export_req = ExportRequest(
            baby_id=baby_id,
            start_date=now - timedelta(days=7),
            end_date=now,
            format="csv",
            output_dir=export_dir,
            include_feeding=True,
            include_health=True,
            include_activity=True
        )
        
        # 导出数据
        export_result = export_service.export_data(export_req)
        print(f"数据已导出到: {export_result.file_path}")
        
        db.commit()
        print("\n示例数据创建成功！")
        
    except Exception as e:
        db.rollback()
        print(f"创建示例数据时出错: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_data()
