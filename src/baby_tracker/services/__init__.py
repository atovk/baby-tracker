"""
Baby Tracker 服务层

这个包包含所有业务逻辑服务：
- 宝宝服务：管理宝宝基本信息
- 喂养服务：管理喂养记录和统计
- 健康服务：管理健康记录和统计
- 活动服务：管理活动记录和统计
- 分析服务：数据分析和可视化
- 导出服务：数据导出功能
"""

# 导入各个服务
try:
    from .baby_service import BabyService
except ImportError:
    pass

try:
    from .feeding_service import FeedingService
except ImportError:
    pass

try:
    from .health_service import HealthService
except ImportError:
    pass

try:
    from .activity_service import ActivityService
except ImportError:
    pass

try:
    from .analytics_service import AnalyticsService, FeedingAnalysis, GrowthAnalysis, TemperatureAnalysis
except ImportError:
    pass

try:
    from .export_service import ExportService, ExportRequest, ExportResult
except ImportError:
    pass

__all__ = []

# 添加可用的服务到导出列表
if 'BabyService' in globals():
    __all__.append('BabyService')
if 'FeedingService' in globals():
    __all__.append('FeedingService')
if 'HealthService' in globals():
    __all__.append('HealthService')
if 'ActivityService' in globals():
    __all__.append('ActivityService')
if 'AnalyticsService' in globals():
    __all__.extend(['AnalyticsService', 'FeedingAnalysis', 'GrowthAnalysis', 'TemperatureAnalysis'])
if 'ExportService' in globals():
    __all__.extend(['ExportService', 'ExportRequest', 'ExportResult'])