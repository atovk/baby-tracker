"""
数据映射器 - 在 SQLAlchemy 模型和 dataclasses DTO 之间转换
"""
from typing import Optional, List
from baby_tracker.models.dto import (
    BabyDTO, NursingDTO, FormulaDTO, SleepDTO, DiaperDTO,
    WeightDTO, HeightDTO, TemperatureDTO, Gender, FinishSide,
    HeadDTO, BathDTO, PlaytimeDTO, PhotoDTO, VideoDTO
)


class DataMapper:
    """数据映射器基类"""
    
    @staticmethod
    def to_dto(model_instance):
        """将 SQLAlchemy 模型实例转换为 DTO"""
        raise NotImplementedError
    
    @staticmethod
    def from_dto(dto_instance):
        """将 DTO 转换为 SQLAlchemy 模型实例"""
        raise NotImplementedError
    
    @staticmethod
    def update_model_from_dto(model_instance, dto_instance):
        """使用 DTO 更新 SQLAlchemy 模型实例"""
        raise NotImplementedError


class BabyMapper(DataMapper):
    """宝宝信息映射器"""
    
    @staticmethod
    def to_dto(baby_model) -> BabyDTO:
        """将 Baby 模型转换为 BabyDTO"""
        if not baby_model:
            return None
        
        return BabyDTO(
            id=baby_model.id,
            name=baby_model.name,
            dob=baby_model.dob,
            due_day=baby_model.due_day,
            gender=Gender(baby_model.gender),
            picture=baby_model.picture,
            timestamp=baby_model.timestamp
        )
    
    @staticmethod
    def from_dto(baby_dto: BabyDTO):
        """将 BabyDTO 转换为 Baby 模型"""
        from baby_tracker.models.baby import Baby
        
        return Baby(
            id=baby_dto.id,
            name=baby_dto.name,
            dob=baby_dto.dob,
            due_day=baby_dto.due_day,
            gender=baby_dto.gender.value,
            picture=baby_dto.picture,
            timestamp=baby_dto.timestamp
        )
    
    @staticmethod
    def update_model_from_dto(baby_model, baby_dto: BabyDTO):
        """使用 BabyDTO 更新 Baby 模型"""
        baby_model.name = baby_dto.name
        baby_model.dob = baby_dto.dob
        baby_model.due_day = baby_dto.due_day
        baby_model.gender = baby_dto.gender.value
        baby_model.picture = baby_dto.picture
        baby_model.timestamp = baby_dto.timestamp


class NursingMapper(DataMapper):
    """母乳喂养映射器"""
    
    @staticmethod
    def to_dto(nursing_model) -> NursingDTO:
        """将 Nursing 模型转换为 NursingDTO"""
        if not nursing_model:
            return None
        
        return NursingDTO(
            id=nursing_model.id,
            baby_id=nursing_model.baby_id,
            time=nursing_model.time,
            note=nursing_model.note,
            has_picture=bool(nursing_model.has_picture),
            desc_id=nursing_model.desc_id,
            finish_side=FinishSide(nursing_model.finish_side),
            left_duration=nursing_model.left_duration,
            right_duration=nursing_model.right_duration,
            both_duration=nursing_model.both_duration,
            timestamp=nursing_model.timestamp
        )
    
    @staticmethod
    def from_dto(nursing_dto: NursingDTO):
        """将 NursingDTO 转换为 Nursing 模型"""
        from baby_tracker.models.feeding import Nursing
        
        return Nursing(
            id=nursing_dto.id,
            baby_id=nursing_dto.baby_id,
            time=nursing_dto.time,
            note=nursing_dto.note,
            has_picture=int(nursing_dto.has_picture),
            desc_id=nursing_dto.desc_id,
            finish_side=nursing_dto.finish_side.value,
            left_duration=nursing_dto.left_duration,
            right_duration=nursing_dto.right_duration,
            both_duration=nursing_dto.both_duration,
            timestamp=nursing_dto.timestamp
        )


class FormulaMapper(DataMapper):
    """配方奶喂养映射器"""
    
    @staticmethod
    def to_dto(formula_model) -> FormulaDTO:
        """将 Formula 模型转换为 FormulaDTO"""
        if not formula_model:
            return None
        
        return FormulaDTO(
            id=formula_model.id,
            baby_id=formula_model.baby_id,
            time=formula_model.time,
            note=formula_model.note,
            has_picture=bool(formula_model.has_picture),
            desc_id=formula_model.desc_id,
            amount=formula_model.amount,
            timestamp=formula_model.timestamp
        )
    
    @staticmethod
    def from_dto(formula_dto: FormulaDTO):
        """将 FormulaDTO 转换为 Formula 模型"""
        from baby_tracker.models.feeding import Formula
        
        return Formula(
            id=formula_dto.id,
            baby_id=formula_dto.baby_id,
            time=formula_dto.time,
            note=formula_dto.note,
            has_picture=int(formula_dto.has_picture),
            desc_id=formula_dto.desc_id,
            amount=formula_dto.amount,
            timestamp=formula_dto.timestamp
        )


class SleepMapper(DataMapper):
    """睡眠记录映射器"""
    
    @staticmethod
    def to_dto(sleep_model) -> SleepDTO:
        """将 Sleep 模型转换为 SleepDTO"""
        if not sleep_model:
            return None
        
        return SleepDTO(
            id=sleep_model.id,
            baby_id=sleep_model.baby_id,
            time=sleep_model.time,
            note=sleep_model.note,
            has_picture=bool(sleep_model.has_picture),
            desc_id=sleep_model.desc_id,
            duration=sleep_model.duration,
            timestamp=sleep_model.timestamp
        )
    
    @staticmethod
    def from_dto(sleep_dto: SleepDTO):
        """将 SleepDTO 转换为 Sleep 模型"""
        from baby_tracker.models.health import Sleep
        
        return Sleep(
            id=sleep_dto.id,
            baby_id=sleep_dto.baby_id,
            time=sleep_dto.time,
            note=sleep_dto.note,
            has_picture=int(sleep_dto.has_picture),
            desc_id=sleep_dto.desc_id,
            duration=sleep_dto.duration,
            timestamp=sleep_dto.timestamp
        )


class WeightMapper(DataMapper):
    """体重记录映射器"""
    
    @staticmethod
    def to_dto(weight_model) -> WeightDTO:
        """将 Weight 模型转换为 WeightDTO"""
        if not weight_model:
            return None
        
        return WeightDTO(
            id=weight_model.id,
            baby_id=weight_model.baby_id,
            time=weight_model.time,
            note=weight_model.note,
            has_picture=bool(weight_model.has_picture),
            weight=weight_model.weight,
            timestamp=weight_model.timestamp
        )
    
    @staticmethod
    def from_dto(weight_dto: WeightDTO):
        """将 WeightDTO 转换为 Weight 模型"""
        from baby_tracker.models.health import Weight
        
        return Weight(
            id=weight_dto.id,
            baby_id=weight_dto.baby_id,
            time=weight_dto.time,
            note=weight_dto.note,
            has_picture=int(weight_dto.has_picture),
            weight=weight_dto.weight,
            timestamp=weight_dto.timestamp
        )


class TemperatureMapper(DataMapper):
    """体温记录映射器"""
    
    @staticmethod
    def to_dto(temp_model) -> TemperatureDTO:
        """将 Temperature 模型转换为 TemperatureDTO"""
        if not temp_model:
            return None
        
        return TemperatureDTO(
            id=temp_model.id,
            baby_id=temp_model.baby_id,
            time=temp_model.time,
            note=temp_model.note,
            has_picture=bool(temp_model.has_picture),
            temperature=temp_model.temperature,
            location=getattr(temp_model, 'location', None),
            timestamp=temp_model.timestamp
        )
    
    @staticmethod
    def from_dto(temp_dto: TemperatureDTO):
        """将 TemperatureDTO 转换为 Temperature 模型"""
        from baby_tracker.models.health import Temperature
        
        return Temperature(
            id=temp_dto.id,
            baby_id=temp_dto.baby_id,
            time=temp_dto.time,
            note=temp_dto.note,
            has_picture=int(temp_dto.has_picture),
            temperature=temp_dto.temperature,
            location=temp_dto.location,
            timestamp=temp_dto.timestamp
        )


class DiaperMapper(DataMapper):
    """尿布记录映射器"""
    
    @staticmethod
    def to_dto(diaper_model) -> DiaperDTO:
        """将 Diaper 模型转换为 DiaperDTO"""
        if not diaper_model:
            return None
        
        return DiaperDTO(
            id=diaper_model.id,
            baby_id=diaper_model.baby_id,
            time=diaper_model.time,
            note=diaper_model.note,
            has_picture=bool(diaper_model.has_picture),
            desc_id=diaper_model.desc_id,
            timestamp=diaper_model.timestamp
        )
    
    @staticmethod
    def from_dto(diaper_dto: DiaperDTO):
        """将 DiaperDTO 转换为 Diaper 模型"""
        from baby_tracker.models.health import Diaper
        
        return Diaper(
            id=diaper_dto.id,
            baby_id=diaper_dto.baby_id,
            time=diaper_dto.time,
            note=diaper_dto.note,
            has_picture=int(diaper_dto.has_picture),
            desc_id=diaper_dto.desc_id,
            timestamp=diaper_dto.timestamp
        )


class HeightMapper(DataMapper):
    """身高记录映射器"""
    
    @staticmethod
    def to_dto(height_model) -> HeightDTO:
        """将 Height 模型转换为 HeightDTO"""
        if not height_model:
            return None
        
        return HeightDTO(
            id=height_model.id,
            baby_id=height_model.baby_id,
            time=height_model.time,
            note=height_model.note,
            has_picture=bool(height_model.has_picture),
            height=height_model.height,
            timestamp=height_model.timestamp
        )
    
    @staticmethod
    def from_dto(height_dto: HeightDTO):
        """将 HeightDTO 转换为 Height 模型"""
        from baby_tracker.models.health import Height
        
        return Height(
            id=height_dto.id,
            baby_id=height_dto.baby_id,
            time=height_dto.time,
            note=height_dto.note,
            has_picture=int(height_dto.has_picture),
            height=height_dto.height,
            timestamp=height_dto.timestamp
        )


class HeadMapper(DataMapper):
    """头围记录映射器"""
    
    @staticmethod
    def to_dto(head_model) -> HeadDTO:
        """将 Head 模型转换为 HeadDTO"""
        if not head_model:
            return None
        
        return HeadDTO(
            id=head_model.id,
            baby_id=head_model.baby_id,
            time=head_model.time,
            note=head_model.note,
            has_picture=bool(head_model.has_picture),
            head=head_model.head,
            timestamp=head_model.timestamp
        )
    
    @staticmethod
    def from_dto(head_dto: HeadDTO):
        """将 HeadDTO 转换为 Head 模型"""
        from baby_tracker.models.health import Head
        
        return Head(
            id=head_dto.id,
            baby_id=head_dto.baby_id,
            time=head_dto.time,
            note=head_dto.note,
            has_picture=int(head_dto.has_picture),
            head=head_dto.head,
            timestamp=head_dto.timestamp
        )


class PlaytimeMapper(DataMapper):
    """游戏时间记录映射器"""
    
    @staticmethod
    def to_dto(playtime_model) -> PlaytimeDTO:
        """将 Playtime 模型转换为 PlaytimeDTO"""
        if not playtime_model:
            return None
        
        return PlaytimeDTO(
            id=playtime_model.id,
            baby_id=playtime_model.baby_id,
            time=playtime_model.time,
            note=playtime_model.note,
            has_picture=bool(playtime_model.has_picture),
            duration=playtime_model.duration,
            play_type=playtime_model.play_type,
            timestamp=playtime_model.timestamp
        )
    
    @staticmethod
    def from_dto(playtime_dto: PlaytimeDTO):
        """将 PlaytimeDTO 转换为 Playtime 模型"""
        from baby_tracker.models.activity import Playtime
        
        return Playtime(
            id=playtime_dto.id,
            baby_id=playtime_dto.baby_id,
            time=playtime_dto.time,
            note=playtime_dto.note,
            has_picture=int(playtime_dto.has_picture),
            duration=playtime_dto.duration,
            play_type=playtime_dto.play_type,
            timestamp=playtime_dto.timestamp
        )


class BathMapper(DataMapper):
    """洗澡记录映射器"""
    
    @staticmethod
    def to_dto(bath_model) -> BathDTO:
        """将 Bath 模型转换为 BathDTO"""
        if not bath_model:
            return None
        
        return BathDTO(
            id=bath_model.id,
            baby_id=bath_model.baby_id,
            time=bath_model.time,
            note=bath_model.note,
            has_picture=bool(bath_model.has_picture),
            duration=bath_model.duration,
            water_temperature=bath_model.water_temperature,
            timestamp=bath_model.timestamp
        )
    
    @staticmethod
    def from_dto(bath_dto: BathDTO):
        """将 BathDTO 转换为 Bath 模型"""
        from baby_tracker.models.activity import Bath
        
        return Bath(
            id=bath_dto.id,
            baby_id=bath_dto.baby_id,
            time=bath_dto.time,
            note=bath_dto.note,
            has_picture=int(bath_dto.has_picture),
            duration=bath_dto.duration,
            water_temperature=bath_dto.water_temperature,
            timestamp=bath_dto.timestamp
        )


class PhotoMapper(DataMapper):
    """照片记录映射器"""
    
    @staticmethod
    def to_dto(photo_model) -> PhotoDTO:
        """将 Photo 模型转换为 PhotoDTO"""
        if not photo_model:
            return None
        
        return PhotoDTO(
            id=photo_model.id,
            baby_id=photo_model.baby_id,
            time=photo_model.time,
            note=photo_model.note,
            has_picture=bool(photo_model.has_picture),
            file_path=photo_model.file_path,
            description=photo_model.description,
            timestamp=photo_model.timestamp
        )
    
    @staticmethod
    def from_dto(photo_dto: PhotoDTO):
        """将 PhotoDTO 转换为 Photo 模型"""
        from baby_tracker.models.activity import Photo
        
        return Photo(
            id=photo_dto.id,
            baby_id=photo_dto.baby_id,
            time=photo_dto.time,
            note=photo_dto.note,
            has_picture=int(photo_dto.has_picture),
            file_path=photo_dto.file_path,
            description=photo_dto.description,
            timestamp=photo_dto.timestamp
        )


class VideoMapper(DataMapper):
    """视频记录映射器"""
    
    @staticmethod
    def to_dto(video_model) -> VideoDTO:
        """将 Video 模型转换为 VideoDTO"""
        if not video_model:
            return None
        
        return VideoDTO(
            id=video_model.id,
            baby_id=video_model.baby_id,
            time=video_model.time,
            note=video_model.note,
            has_picture=bool(video_model.has_picture),
            file_path=video_model.file_path,
            duration=video_model.duration,
            description=video_model.description,
            timestamp=video_model.timestamp
        )
    
    @staticmethod
    def from_dto(video_dto: VideoDTO):
        """将 VideoDTO 转换为 Video 模型"""
        from baby_tracker.models.activity import Video
        
        return Video(
            id=video_dto.id,
            baby_id=video_dto.baby_id,
            time=video_dto.time,
            note=video_dto.note,
            has_picture=int(video_dto.has_picture),
            file_path=video_dto.file_path,
            duration=video_dto.duration,
            description=video_dto.description,
            timestamp=video_dto.timestamp
        )
