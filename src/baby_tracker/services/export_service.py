"""
导出服务 - 使用 dataclasses 进行数据导出
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, BinaryIO
from datetime import datetime, timedelta
import os
import pandas as pd
from baby_tracker.services.baby_service import BabyService
from baby_tracker.services.feeding_service import FeedingService
from baby_tracker.models.dto import BabyDTO


@dataclass
class ExportRequest:
    """导出请求"""
    baby_id: str
    start_date: datetime
    end_date: datetime
    format: str = "excel"  # excel, csv, pdf
    include_feeding: bool = True
    include_sleep: bool = True
    include_diaper: bool = True
    include_growth: bool = True
    include_temperature: bool = False
    include_photos: bool = False
    filename: Optional[str] = None


@dataclass
class ExportResult:
    """导出结果"""
    success: bool
    file_path: Optional[str] = None
    error_message: Optional[str] = None
    export_date: datetime = field(default_factory=datetime.now)
    file_size: Optional[int] = None
    record_count: Optional[int] = None


class ExportService:
    """数据导出服务"""
    
    def __init__(self, db_session=None):
        self.baby_service = BabyService(db_session)
        self.feeding_service = FeedingService(db_session)
        self.export_dir = "data/exports"
        
        # 确保导出目录存在
        os.makedirs(self.export_dir, exist_ok=True)
    
    def export_baby_data(self, request: ExportRequest) -> ExportResult:
        """导出宝宝数据"""
        # 获取宝宝信息
        baby = self.baby_service.get_baby(request.baby_id)
        if not baby:
            return ExportResult(
                success=False,
                error_message=f"未找到ID为{request.baby_id}的宝宝记录"
            )
        
        # 生成默认文件名
        if not request.filename:
            date_range = f"{request.start_date.strftime('%Y%m%d')}-{request.end_date.strftime('%Y%m%d')}"
            request.filename = f"{baby.name}_数据导出_{date_range}"
        
        try:
            # 根据请求格式调用对应的导出方法
            if request.format.lower() == "excel":
                return self._export_to_excel(request, baby)
            elif request.format.lower() == "csv":
                return self._export_to_csv(request, baby)
            elif request.format.lower() == "pdf":
                return self._export_to_pdf(request, baby)
            else:
                return ExportResult(
                    success=False,
                    error_message=f"不支持的导出格式: {request.format}"
                )
        except Exception as e:
            return ExportResult(
                success=False,
                error_message=f"导出过程中发生错误: {str(e)}"
            )
    
    def _export_to_excel(self, request: ExportRequest, baby: BabyDTO) -> ExportResult:
        """导出为Excel格式"""
        # Excel文件路径
        file_path = os.path.join(self.export_dir, f"{request.filename}.xlsx")
        
        # 创建Excel写入器，支持多个工作表
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            record_count = 0
            
            # 添加宝宝基本信息表
            baby_info = pd.DataFrame([{
                "名称": "宝宝姓名",
                "值": baby.name
            }, {
                "名称": "出生日期",
                "值": datetime.fromtimestamp(baby.dob).strftime('%Y-%m-%d')
            }, {
                "名称": "性别",
                "值": baby.gender_display
            }, {
                "名称": "年龄(天)",
                "值": baby.age_in_days
            }, {
                "名称": "年龄(周)",
                "值": baby.age_in_weeks
            }, {
                "名称": "年龄(月)",
                "值": baby.age_in_months
            }, {
                "名称": "导出时间范围",
                "值": f"{request.start_date.strftime('%Y-%m-%d')} 至 {request.end_date.strftime('%Y-%m-%d')}"
            }])
            baby_info.to_excel(writer, sheet_name='宝宝信息', index=False)
            
            # 添加喂养记录表
            if request.include_feeding:
                feeding_data = self._get_feeding_data(request.baby_id, request.start_date, request.end_date)
                if feeding_data:
                    feeding_df = pd.DataFrame(feeding_data)
                    feeding_df.to_excel(writer, sheet_name='喂养记录', index=False)
                    record_count += len(feeding_data)
            
            # TODO: 添加其他记录表（睡眠、尿布、生长发育等）
            # 这里需要健康相关的仓储和服务来获取数据
        
        # 获取文件大小
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        
        return ExportResult(
            success=True,
            file_path=file_path,
            file_size=file_size,
            record_count=record_count,
            export_date=datetime.now()
        )
    
    def _export_to_csv(self, request: ExportRequest, baby: BabyDTO) -> ExportResult:
        """导出为CSV格式"""
        # 由于CSV不支持多表，我们将创建多个CSV文件并打包
        files_created = []
        record_count = 0
        
        try:
            # 导出宝宝基本信息
            baby_info_path = os.path.join(self.export_dir, f"{request.filename}_宝宝信息.csv")
            baby_info = pd.DataFrame([{
                "名称": "宝宝姓名",
                "值": baby.name
            }, {
                "名称": "出生日期",
                "值": datetime.fromtimestamp(baby.dob).strftime('%Y-%m-%d')
            }, {
                "名称": "性别",
                "值": baby.gender_display
            }, {
                "名称": "年龄(天)",
                "值": baby.age_in_days
            }])
            baby_info.to_csv(baby_info_path, index=False)
            files_created.append(baby_info_path)
            
            # 导出喂养记录
            if request.include_feeding:
                feeding_data = self._get_feeding_data(request.baby_id, request.start_date, request.end_date)
                if feeding_data:
                    feeding_path = os.path.join(self.export_dir, f"{request.filename}_喂养记录.csv")
                    feeding_df = pd.DataFrame(feeding_data)
                    feeding_df.to_csv(feeding_path, index=False)
                    files_created.append(feeding_path)
                    record_count += len(feeding_data)
            
            # TODO: 导出其他记录（睡眠、尿布、生长发育等）
            # 这里需要健康相关的仓储和服务来获取数据
            
            # 创建导出结果
            # 在实际应用中可能需要将CSV文件打包为ZIP
            return ExportResult(
                success=True,
                file_path=", ".join(files_created),
                file_size=sum(os.path.getsize(f) for f in files_created),
                record_count=record_count,
                export_date=datetime.now()
            )
            
        except Exception as e:
            # 清理已创建的文件
            for file_path in files_created:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except:
                        pass
            
            raise e
    
    def _export_to_pdf(self, request: ExportRequest, baby: BabyDTO) -> ExportResult:
        """导出为PDF格式"""
        try:
            import reportlab
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            
            # PDF文件路径
            file_path = os.path.join(self.export_dir, f"{request.filename}.pdf")
            
            # 创建PDF文档
            doc = SimpleDocTemplate(file_path, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []
            
            # 添加标题
            title_style = styles["Title"]
            title = Paragraph(f"{baby.name} 的宝宝记录", title_style)
            elements.append(title)
            elements.append(Spacer(1, 12))
            
            # 添加基本信息表格
            data = [
                ["宝宝姓名", baby.name],
                ["出生日期", datetime.fromtimestamp(baby.dob).strftime('%Y-%m-%d')],
                ["性别", baby.gender_display],
                ["年龄(天)", str(baby.age_in_days)],
                ["年龄(周)", str(baby.age_in_weeks)],
                ["年龄(月)", str(baby.age_in_months)],
                ["导出时间范围", f"{request.start_date.strftime('%Y-%m-%d')} 至 {request.end_date.strftime('%Y-%m-%d')}"],
            ]
            
            info_table = Table(data, colWidths=[100, 300])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 20))
            
            record_count = 0
            
            # 添加喂养记录表格
            if request.include_feeding:
                feeding_data = self._get_feeding_data(request.baby_id, request.start_date, request.end_date)
                if feeding_data:
                    elements.append(Paragraph("喂养记录", styles["Heading2"]))
                    elements.append(Spacer(1, 10))
                    
                    # 转换数据为表格格式
                    table_data = [["日期", "时间", "类型", "详情", "备注"]]
                    for item in feeding_data:
                        if item.get('喂养类型') == '母乳':
                            details = f"左侧: {item.get('左侧时长(分钟)', 0)}分钟, 右侧: {item.get('右侧时长(分钟)', 0)}分钟"
                        else:
                            details = f"{item.get('数量(毫升)', 0)}毫升"
                        
                        table_data.append([
                            item.get('日期', ''),
                            item.get('时间', ''),
                            item.get('喂养类型', ''),
                            details,
                            item.get('备注', '')
                        ])
                    
                    feeding_table = Table(table_data, colWidths=[60, 50, 50, 120, 150])
                    feeding_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ]))
                    elements.append(feeding_table)
                    elements.append(Spacer(1, 20))
                    
                    record_count += len(feeding_data)
            
            # TODO: 添加其他记录表格（睡眠、尿布、生长发育等）
            # 这里需要健康相关的仓储和服务来获取数据
            
            # 构建PDF文档
            doc.build(elements)
            
            # 获取文件大小
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            
            return ExportResult(
                success=True,
                file_path=file_path,
                file_size=file_size,
                record_count=record_count,
                export_date=datetime.now()
            )
            
        except ImportError:
            return ExportResult(
                success=False,
                error_message="导出PDF需要安装reportlab库。请使用命令: pip install reportlab"
            )
    
    def _get_feeding_data(self, baby_id: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """获取喂养数据"""
        # 获取喂养记录
        nursing_records = self.feeding_service.get_nursing_records_by_date(
            baby_id, start_date, end_date
        )
        formula_records = self.feeding_service.get_formula_records_by_date(
            baby_id, start_date, end_date
        )
        
        # 转换为统一格式
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
        all_data = nursing_data + formula_data
        all_data.sort(key=lambda x: x['日期'] + ' ' + x['时间'], reverse=True)
        
        return all_data
    
    def close(self):
        """关闭服务"""
        self.baby_service.close()
        self.feeding_service.close()
