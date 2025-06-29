from tk_db_utils import DbOrmBaseMixedIn
from sqlalchemy import String, Integer, Boolean, Text,UniqueConstraint,DateTime, false
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime


class GaokaoBase(DbOrmBaseMixedIn):
    __abstract__ = True
   
    key_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now,nullable=True, comment="更新时间")

class SchoolInfoTable(GaokaoBase):
    __tablename__ = 'school_info'
    
    # 学校代码1
    yxdm: Mapped[str] = mapped_column(String(20), comment="学校代码")
    # 学校名称1
    yxmc: Mapped[str] = mapped_column(String(100), nullable=False, comment="学校名称")
    # 学校代号1
    yxdh: Mapped[Optional[str]] = mapped_column(String(20), comment="学校代号")
    # 是否9851
    sf985: Mapped[Optional[bool]] = mapped_column(Boolean, comment="是否985")
    # 是否2111
    sf211: Mapped[Optional[bool]] = mapped_column(Boolean, comment="是否211")
    # 是否双一流1
    sfsyl: Mapped[Optional[str]] = mapped_column(String(50), comment="是否双一流")
    # 是否公办1
    sfgb: Mapped[Optional[str]] = mapped_column(String(10), comment="是否公办")
    # 所属地区代码1
    ssdm: Mapped[Optional[str]] = mapped_column(String(50), comment="所属地区代码")
    # 地级市代码1
    djsdm: Mapped[Optional[str]] = mapped_column(String(50), comment="地级市代码")
    # 主页地址1
    zydz: Mapped[Optional[str]] = mapped_column(String(200), comment="主页地址")
    # 计划人数1
    jhrs: Mapped[Optional[int]] = mapped_column(Integer, comment="计划人数")
    # 专业数量1
    zysl: Mapped[Optional[int]] = mapped_column(Integer, comment="专业数量")
    # 专业组数量1
    zyzsl: Mapped[Optional[int]] = mapped_column(Integer, comment="专业组数量")

    __table_args__ = (
        UniqueConstraint('yxdm','yxdh','yxmc',name='unique_yxdm_yxdh_yxmc'),
        {'schema': 'gaokao'}
    )

class ZyzInfoTable(GaokaoBase):
    __tablename__ = 'zyz_info'

    # 主键字段
    zyzdm: Mapped[str] = mapped_column(String(20), comment="专业组代码")  # 专业组代码
    sf985: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="是否985院校")  # 是否985院校
    sf211: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="是否211院校")  # 是否211院校
    zyzmc: Mapped[str] = mapped_column(String(50), nullable=False, comment="专业组名称")  # 专业组名称
    zysl: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="专业数量")  # 专业数量
    tbrcdm: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="填报批次代码")  # 填报批次代码
    djsdm: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="等级水平代码")  # 等级水平代码
    pcdm: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="批次代码")  # 批次代码
    zydz: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="专业地址")  # 专业地址
    yxmc: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="院校名称")  # 院校名称
    jhrs: Mapped[int|None] = mapped_column(Integer, nullable=True, comment="计划人数")  # 计划人数
    yxdm: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="院校代码")  # 院校代码
    jhlbdm: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="计划类别代码")  # 计划类别代码
    zyzbh: Mapped[str] = mapped_column(String(20), nullable=False, comment="专业组编号")  # 专业组编号
    sfysc: Mapped[bool] = mapped_column(Boolean, nullable=False, comment="是否艺术类")  # 是否艺术类
    sfyjtjzycgk: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="是否依据特殊政策招生")  # 是否依据特殊政策招生
    sfsyl: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="是否双一流")  # 是否双一流
    kldm: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="科类代码")  # 科类代码
    jhxzdm: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="计划性质代码")  # 计划性质代码
    yxdh: Mapped[str] = mapped_column(String(20), nullable=False, comment="院校代号")  # 院校代号
    sfgb: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="是否公办院校")  # 是否公办院校
    kskmyq: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="考试科目要求")  # 考试科目要求
    ssdm: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="省市代码")  # 省市代码


    __table_args__=(
        UniqueConstraint('zyzdm','yxdh','zyzbh',name='unique_zyzdm_yxdh_zyzbh'),
        {'schema': 'gaokao'}
    )


class ZyInfoTable(GaokaoBase):
    __tablename__ = 'zy_info'
    skkmyq: Mapped[str] = mapped_column(String(50), nullable=True,comment='未知')
    zymc: Mapped[str] = mapped_column(String(100), nullable=False,comment='专业名称')
    sfks: Mapped[bool] = mapped_column(Boolean, default=False,comment='是否口试')
    jhrs: Mapped[int|None] = mapped_column(Integer, nullable=True,comment='计划人数')
    yxdm: Mapped[str] = mapped_column(String(20), nullable=False,comment='院校代码')
    zydm: Mapped[str] = mapped_column(String(20), nullable=False,comment='专业代码')
    bxddbb: Mapped[bool] = mapped_column(Boolean, default=True,comment='未知')
    xzdm: Mapped[str] = mapped_column(String(10), nullable=False,comment='学制代码')
    zyzdm: Mapped[str] = mapped_column(String(50), nullable=False,comment='专业组代码')
    zyxh: Mapped[str] = mapped_column(String(50), nullable=True,comment='未知')
    bxdd: Mapped[str|None] = mapped_column(String(50), nullable=True,comment='办学地点')
    bz: Mapped[str] = mapped_column(Text, nullable=True,comment='备注')
    zydh: Mapped[str] = mapped_column(String(10), nullable=False,comment='专业代号')
    yxdh: Mapped[str] = mapped_column(String(10), nullable=False,comment='学院代号')
    wyyzdm: Mapped[str] = mapped_column(String(50), nullable=True,comment='外语语种要求')
    sfbz: Mapped[str|None] = mapped_column(String(20), nullable=True,comment='收费标注')
    kskmyq: Mapped[str] = mapped_column(String(100), nullable=False,comment='考试科目要求')




    __table_args__ = (
        UniqueConstraint('yxdh','zyzdm','zydm','zydh',name='unique_yxdh_zyzdm_zydm_zydh'),
        {'schema':'gaokao'}
    )


class LsZyzInfoTable(GaokaoBase):
    __tablename__ = 'ls_zyz_info'
    # 唯一索引字段
    nf: Mapped[str] = mapped_column(String(10), nullable=False, comment="年份.")
    yxdm: Mapped[str] = mapped_column(String(10),nullable=False, comment="院校代码.")
    zyzdm: Mapped[str] = mapped_column(String(20), nullable=False, comment="专业组代码.")
    zyzbh: Mapped[str] = mapped_column(String(20), nullable=False, comment="专业组编号.")

    
    # 院校基本信息
    yxdh: Mapped[str] = mapped_column(String(20), nullable=False, comment="院校代号.")
    yxmc: Mapped[str | None] = mapped_column(String(100), comment="院校名称.")
    ssdm: Mapped[str | None] = mapped_column(String(20), comment="省市代码.")
    ssmc: Mapped[str | None] = mapped_column(String(50), comment="省市名称.")
    djsdm: Mapped[str | None] = mapped_column(String(20), comment="地级市代码.")
    djsmc: Mapped[str | None] = mapped_column(String(50), comment="地级市名称.")
    yxjbzdm: Mapped[str | None] = mapped_column(String(20), comment="院校举办者代码.")
    
    # 院校属性标识
    sf985: Mapped[bool | None] = mapped_column(Boolean, comment="是否985院校.")
    sf211: Mapped[bool | None] = mapped_column(Boolean, comment="是否211院校.")
    sfsyl: Mapped[str | None] = mapped_column(String(20), comment="是否双一流.")

    # 招生信息
    jhsxdm: Mapped[str | None] = mapped_column(String(20), comment="计划属性代码.")
    
    # 专业组信息
    zyzmc: Mapped[str] = mapped_column(String(50), nullable=False, comment="专业组名称.")
    zymcStr: Mapped[str | None] = mapped_column(Text, comment="专业名称字符串.")
    lqrs: Mapped[int | None] = mapped_column(Integer, comment="录取人数.")
    
    # 排名信息
    zdmc: Mapped[str | None] = mapped_column(String(50), comment="最低名次.")
    zgf: Mapped[int | None] = mapped_column(Integer, comment="最高分.")
    zdf: Mapped[int | None] = mapped_column(Integer, comment="最低分.")
    pjf: Mapped[int | None] = mapped_column(Integer, comment="平均分.")


    __table_args__=(
        UniqueConstraint('nf','yxdm','zyzdm','zyzbh',name='unique_nf_yxdm_zyzdm_zyzbh'),
        {'schema': 'gaokao'}
    )


class LsZyInfoTable(GaokaoBase):
    __tablename__ = 'ls_zy_info'
    # 唯一索引
    nf: Mapped[str] = mapped_column(String(10), nullable=False, comment="年份.")
    yxmc: Mapped[str] = mapped_column(String(20), nullable=False, comment="院校名称.")
    zyzdm: Mapped[str] = mapped_column(String(20), nullable=False, comment="专业组代码.")
    zyzbh: Mapped[str] = mapped_column(String(20), nullable=False, comment="专业组编号.")
    zymc: Mapped[str] = mapped_column(String(50), nullable=False, comment="专业名称.")
    pjmc: Mapped[str] = mapped_column(String(50), nullable=False, comment="平均名次.")
    pjf: Mapped[int ] = mapped_column(Integer,nullable=False, comment="平均分.")
    lqrs: Mapped[int] = mapped_column(Integer, nullable=False,comment="录取人数.")
    # 排名信息
    zydm: Mapped[str|None] = mapped_column(String(20), nullable=True, comment="专业代码.")


    __table_args__=(
        UniqueConstraint('nf','yxmc','zyzdm','zyzbh','zymc','pjmc','pjf','lqrs','zydm','zymc',name='unique_nf_yxmc_zyzdm_zyzbh_zymc_pjmc_pjf_lqrs_zydm_zymc'),
        {'schema': 'gaokao'}
    )

