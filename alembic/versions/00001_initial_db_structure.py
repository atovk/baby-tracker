"""Initial db structure

Revision ID: 00001
Revises: 
Create Date: 2025-05-23 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建 Baby 表
    op.create_table(
        'Baby',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('Name', sa.String(), nullable=False),
        sa.Column('DOB', sa.Float(), nullable=False),
        sa.Column('DueDay', sa.String(), nullable=True),
        sa.Column('Gender', sa.Integer(), nullable=True),
        sa.Column('Picture', sa.String(), nullable=True),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建 Nursing 表
    op.create_table(
        'Nursing',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('BabyID', sa.String(), nullable=False),
        sa.Column('Time', sa.Float(), nullable=False),
        sa.Column('Note', sa.Text(), nullable=True),
        sa.Column('HasPicture', sa.Integer(), nullable=True, default=0),
        sa.Column('DescID', sa.String(), nullable=True),
        sa.Column('FinishSide', sa.Integer(), nullable=True),
        sa.Column('LeftDuration', sa.Integer(), nullable=True),
        sa.Column('RightDuration', sa.Integer(), nullable=True),
        sa.Column('BothDuration', sa.Integer(), nullable=True),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['BabyID'], ['Baby.ID'], ),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建 Formula 表
    op.create_table(
        'Formula',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('BabyID', sa.String(), nullable=False),
        sa.Column('Time', sa.Float(), nullable=False),
        sa.Column('Note', sa.Text(), nullable=True),
        sa.Column('HasPicture', sa.Integer(), nullable=True, default=0),
        sa.Column('DescID', sa.String(), nullable=True),
        sa.Column('Amount', sa.Float(), nullable=True),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['BabyID'], ['Baby.ID'], ),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建 Sleep 表
    op.create_table(
        'Sleep',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('BabyID', sa.String(), nullable=False),
        sa.Column('Time', sa.Float(), nullable=False),
        sa.Column('Note', sa.Text(), nullable=True),
        sa.Column('HasPicture', sa.Integer(), nullable=True, default=0),
        sa.Column('DescID', sa.String(), nullable=True),
        sa.Column('Duration', sa.Integer(), nullable=True),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['BabyID'], ['Baby.ID'], ),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建 Diaper 表
    op.create_table(
        'Diaper',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('BabyID', sa.String(), nullable=False),
        sa.Column('Time', sa.Float(), nullable=False),
        sa.Column('Note', sa.Text(), nullable=True),
        sa.Column('HasPicture', sa.Integer(), nullable=True, default=0),
        sa.Column('DescID', sa.String(), nullable=True),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['BabyID'], ['Baby.ID'], ),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建 Weight 表
    op.create_table(
        'Weight',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('BabyID', sa.String(), nullable=False),
        sa.Column('Time', sa.Float(), nullable=False),
        sa.Column('Note', sa.Text(), nullable=True),
        sa.Column('HasPicture', sa.Integer(), nullable=True, default=0),
        sa.Column('Weight', sa.Float(), nullable=False),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['BabyID'], ['Baby.ID'], ),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建 Height 表
    op.create_table(
        'Height',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('BabyID', sa.String(), nullable=False),
        sa.Column('Time', sa.Float(), nullable=False),
        sa.Column('Note', sa.Text(), nullable=True),
        sa.Column('HasPicture', sa.Integer(), nullable=True, default=0),
        sa.Column('Height', sa.Float(), nullable=False),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['BabyID'], ['Baby.ID'], ),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建 Head 表
    op.create_table(
        'Head',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('BabyID', sa.String(), nullable=False),
        sa.Column('Time', sa.Float(), nullable=False),
        sa.Column('Note', sa.Text(), nullable=True),
        sa.Column('HasPicture', sa.Integer(), nullable=True, default=0),
        sa.Column('Head', sa.Float(), nullable=False),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['BabyID'], ['Baby.ID'], ),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建 Temperature 表
    op.create_table(
        'Temperature',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('BabyID', sa.String(), nullable=False),
        sa.Column('Time', sa.Float(), nullable=False),
        sa.Column('Note', sa.Text(), nullable=True),
        sa.Column('HasPicture', sa.Integer(), nullable=True, default=0),
        sa.Column('Temperature', sa.Float(), nullable=False),
        sa.Column('Location', sa.String(), nullable=True),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['BabyID'], ['Baby.ID'], ),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建 Playtime 表
    op.create_table(
        'Playtime',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('BabyID', sa.String(), nullable=False),
        sa.Column('Time', sa.Float(), nullable=False),
        sa.Column('Note', sa.Text(), nullable=True),
        sa.Column('HasPicture', sa.Integer(), nullable=True, default=0),
        sa.Column('Duration', sa.Integer(), nullable=True),
        sa.Column('PlayType', sa.String(), nullable=True),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['BabyID'], ['Baby.ID'], ),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建 Bath 表
    op.create_table(
        'Bath',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('BabyID', sa.String(), nullable=False),
        sa.Column('Time', sa.Float(), nullable=False),
        sa.Column('Note', sa.Text(), nullable=True),
        sa.Column('HasPicture', sa.Integer(), nullable=True, default=0),
        sa.Column('Duration', sa.Integer(), nullable=True),
        sa.Column('WaterTemperature', sa.Float(), nullable=True),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['BabyID'], ['Baby.ID'], ),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建 Photo 表
    op.create_table(
        'Photo',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('BabyID', sa.String(), nullable=False),
        sa.Column('Time', sa.Float(), nullable=False),
        sa.Column('Note', sa.Text(), nullable=True),
        sa.Column('HasPicture', sa.Integer(), nullable=True, default=0),
        sa.Column('FilePath', sa.String(), nullable=False),
        sa.Column('Description', sa.Text(), nullable=True),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['BabyID'], ['Baby.ID'], ),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建 Video 表
    op.create_table(
        'Video',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('BabyID', sa.String(), nullable=False),
        sa.Column('Time', sa.Float(), nullable=False),
        sa.Column('Note', sa.Text(), nullable=True),
        sa.Column('HasPicture', sa.Integer(), nullable=True, default=0),
        sa.Column('FilePath', sa.String(), nullable=False),
        sa.Column('Duration', sa.Integer(), nullable=True),
        sa.Column('Description', sa.Text(), nullable=True),
        sa.Column('Timestamp', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['BabyID'], ['Baby.ID'], ),
        sa.PrimaryKeyConstraint('ID')
    )
    
    # 创建查找表
    op.create_table(
        'DiaperDesc',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('Name', sa.String(), nullable=False),
        sa.Column('DisplayOrder', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('ID')
    )
    
    op.create_table(
        'NursingDesc',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('Name', sa.String(), nullable=False),
        sa.Column('DisplayOrder', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('ID')
    )
    
    op.create_table(
        'FormulaDesc',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('Name', sa.String(), nullable=False),
        sa.Column('DisplayOrder', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('ID')
    )
    
    op.create_table(
        'SleepDesc',
        sa.Column('ID', sa.String(), nullable=False),
        sa.Column('Name', sa.String(), nullable=False),
        sa.Column('DisplayOrder', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('ID')
    )


def downgrade() -> None:
    # 删除表
    op.drop_table('Video')
    op.drop_table('Photo')
    op.drop_table('Bath')
    op.drop_table('Playtime')
    op.drop_table('Temperature')
    op.drop_table('Head')
    op.drop_table('Height')
    op.drop_table('Weight')
    op.drop_table('Diaper')
    op.drop_table('Sleep')
    op.drop_table('Formula')
    op.drop_table('Nursing')
    op.drop_table('SleepDesc')
    op.drop_table('FormulaDesc')
    op.drop_table('NursingDesc')
    op.drop_table('DiaperDesc')
    op.drop_table('Baby')
