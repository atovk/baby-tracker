"""
数据访问测试：测试 DataClasses DTO 和 Repository 实现的基本功能
"""
import unittest
import os
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from baby_tracker.models.dto import (
    BabyDTO, NursingDTO, FormulaDTO, SleepDTO, DiaperDTO, 
    WeightDTO, HeightDTO, HeadDTO, TemperatureDTO, Gender, FinishSide,
    PlaytimeDTO, BathDTO, PhotoDTO, VideoDTO
)
from baby_tracker.repositories import (
    BabyRepository, NursingRepository, FormulaRepository, SleepRepository, 
    DiaperRepository, WeightRepository, HeightRepository, HeadRepository,
    TemperatureRepository, PlaytimeRepository, BathRepository,
    PhotoRepository, VideoRepository
)
from baby_tracker.services import (
    BabyService, FeedingService, HealthService, ActivityService
)


class DataClassesRepositoryTest(unittest.TestCase):
    """测试 DataClasses 和 Repository 实现"""
    
    @classmethod
    def setUpClass(cls):
        """设置测试环境"""
        # 创建内存中的SQLite数据库
        cls.engine = create_engine('sqlite:///:memory:')
        
        # 创建数据库表
        from baby_tracker.models.base import Base
        Base.metadata.create_all(cls.engine)
        
        # 创建会话工厂
        cls.Session = sessionmaker(bind=cls.engine)
    
    def setUp(self):
        """每个测试前执行"""
        self.session = self.Session()
        self.baby_repo = BabyRepository(self.session)
        
        # 创建一个测试宝宝
        self.test_baby = BabyDTO(
            id=str(uuid.uuid4()),
            name="测试宝宝",
            dob=(datetime.now() - timedelta(days=30)).timestamp(),
            gender=Gender.FEMALE
        )
        self.test_baby = self.baby_repo.create(self.test_baby)
    
    def tearDown(self):
        """每个测试后执行"""
        self.session.rollback()
        self.session.close()
    
    def test_baby_repository(self):
        """测试宝宝仓储"""
        # 查询宝宝
        baby = self.baby_repo.find_by_id(self.test_baby.id)
        self.assertIsNotNone(baby)
        self.assertEqual(baby.name, "测试宝宝")
        
        # 更新宝宝信息
        baby.name = "新名字"
        updated_baby = self.baby_repo.update(baby)
        self.assertEqual(updated_baby.name, "新名字")
        
        # 重新查询确认更新
        baby = self.baby_repo.find_by_id(self.test_baby.id)
        self.assertEqual(baby.name, "新名字")
    
    def test_nursing_repository(self):
        """测试母乳喂养仓储"""
        nursing_repo = NursingRepository(self.session)
        
        # 创建母乳喂养记录
        nursing = NursingDTO(
            id=str(uuid.uuid4()),
            baby_id=self.test_baby.id,
            time=datetime.now().timestamp(),
            left_duration=10,
            right_duration=15,
            both_duration=0,
            finish_side=FinishSide.RIGHT
        )
        created_nursing = nursing_repo.create(nursing)
        self.assertIsNotNone(created_nursing)
        
        # 查询母乳喂养记录
        found_nursing = nursing_repo.find_by_id(created_nursing.id)
        self.assertIsNotNone(found_nursing)
        self.assertEqual(found_nursing.left_duration, 10)
        self.assertEqual(found_nursing.right_duration, 15)
        
        # 查询宝宝的所有母乳喂养记录
        nursing_records = nursing_repo.find_by_baby_id(self.test_baby.id)
        self.assertEqual(len(nursing_records), 1)
    
    def test_formula_repository(self):
        """测试配方奶仓储"""
        formula_repo = FormulaRepository(self.session)
        
        # 创建配方奶记录
        formula = FormulaDTO(
            id=str(uuid.uuid4()),
            baby_id=self.test_baby.id,
            time=datetime.now().timestamp(),
            amount=120.0
        )
        created_formula = formula_repo.create(formula)
        self.assertIsNotNone(created_formula)
        
        # 查询配方奶记录
        found_formula = formula_repo.find_by_id(created_formula.id)
        self.assertIsNotNone(found_formula)
        self.assertEqual(found_formula.amount, 120.0)
    
    def test_health_repositories(self):
        """测试健康相关仓储"""
        # 测试睡眠仓储
        sleep_repo = SleepRepository(self.session)
        sleep = SleepDTO(
            id=str(uuid.uuid4()),
            baby_id=self.test_baby.id,
            time=datetime.now().timestamp(),
            duration=120
        )
        created_sleep = sleep_repo.create(sleep)
        self.assertEqual(created_sleep.duration, 120)
        
        # 测试尿布仓储
        diaper_repo = DiaperRepository(self.session)
        diaper = DiaperDTO(
            id=str(uuid.uuid4()),
            baby_id=self.test_baby.id,
            time=datetime.now().timestamp()
        )
        created_diaper = diaper_repo.create(diaper)
        self.assertIsNotNone(created_diaper)
        
        # 测试体重仓储
        weight_repo = WeightRepository(self.session)
        weight = WeightDTO(
            id=str(uuid.uuid4()),
            baby_id=self.test_baby.id,
            time=datetime.now().timestamp(),
            weight=3500.0
        )
        created_weight = weight_repo.create(weight)
        self.assertEqual(created_weight.weight, 3500.0)
    
    def test_activity_repositories(self):
        """测试活动相关仓储"""
        # 测试洗澡仓储
        bath_repo = BathRepository(self.session)
        bath = BathDTO(
            id=str(uuid.uuid4()),
            baby_id=self.test_baby.id,
            time=datetime.now().timestamp(),
            duration=15,
            water_temperature=38.0
        )
        created_bath = bath_repo.create(bath)
        self.assertEqual(created_bath.water_temperature, 38.0)
        
        # 测试游戏仓储
        playtime_repo = PlaytimeRepository(self.session)
        playtime = PlaytimeDTO(
            id=str(uuid.uuid4()),
            baby_id=self.test_baby.id,
            time=datetime.now().timestamp(),
            duration=30,
            play_type="积木"
        )
        created_playtime = playtime_repo.create(playtime)
        self.assertEqual(created_playtime.play_type, "积木")
    
    def test_services_basic_functionality(self):
        """测试服务层的基本功能"""
        # 测试宝宝服务
        baby_service = BabyService(self.session)
        baby = baby_service.get_baby_by_id(self.test_baby.id)
        self.assertEqual(baby.name, "测试宝宝")
        
        # 测试喂养服务
        feeding_service = FeedingService(self.session)
        nursing_id = feeding_service.add_nursing(
            baby_id=self.test_baby.id,
            left_duration=8,
            right_duration=10
        ).id
        formula_id = feeding_service.add_formula(
            baby_id=self.test_baby.id,
            amount=90.0
        ).id
        
        # 验证添加的记录
        nursing = feeding_service.nursing_repo.find_by_id(nursing_id)
        self.assertEqual(nursing.left_duration, 8)
        
        formula = feeding_service.formula_repo.find_by_id(formula_id)
        self.assertEqual(formula.amount, 90.0)
        
        # 测试健康服务
        health_service = HealthService(self.session)
        weight_id = health_service.add_weight_record(
            baby_id=self.test_baby.id,
            weight=3600.0
        ).id
        
        # 验证添加的记录
        weight = health_service.weight_repo.find_by_id(weight_id)
        self.assertEqual(weight.weight, 3600.0)


if __name__ == '__main__':
    unittest.main()
