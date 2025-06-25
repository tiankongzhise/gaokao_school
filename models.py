from sqlalchemy import String, Text, Integer, JSON, ForeignKey, MetaData, DateTime, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime

from tk_db_utils import DbOrmBaseMixedIn

class DatabaseBase(DbOrmBaseMixedIn):
    """SQLAlchemy 2.0 风格的基类，支持多数据库配置"""
    
    # 可以通过子类重写来指定不同的数据库schema
    __abstract__ = True
    
    @classmethod
    def set_schema(cls, schema_name: str):
        """设置数据库schema"""
        cls.metadata.schema = schema_name
    
    @classmethod
    def set_table_prefix(cls, prefix: str):
        """设置表名前缀"""
        cls.__table_prefix__ = prefix


# 默认基类
Base = DatabaseBase


# 可以为不同数据库创建不同的基类
class GaokaoDatabase(DatabaseBase):
    """高考数据库专用基类"""
    __abstract__ = True
    
    # 可以在这里设置特定的metadata配置
    metadata = MetaData(schema="gaokao")
    
    # 添加通用的审计字段
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    version: Mapped[int] = mapped_column(Integer, default=1, comment='版本号，用于乐观锁')


class School(GaokaoDatabase):
    """学校基本信息表"""
    __tablename__ = 'schools'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    school_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment='学校ID')
    data_code: Mapped[Optional[str]] = mapped_column(String(50), comment='数据代码')
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment='学校名称')
    type: Mapped[Optional[str]] = mapped_column(String(50), comment='类型')
    school_type: Mapped[Optional[str]] = mapped_column(String(50), comment='学校类型')
    school_nature: Mapped[Optional[str]] = mapped_column(String(50), comment='学校性质')
    level: Mapped[Optional[str]] = mapped_column(String(50), comment='层次')
    code_enroll: Mapped[Optional[str]] = mapped_column(String(50), comment='招生代码')
    zs_code: Mapped[Optional[str]] = mapped_column(String(50), comment='招生代码2')
    belong: Mapped[Optional[str]] = mapped_column(String(100), comment='隶属')
    
    # 标识字段
    f985: Mapped[Optional[str]] = mapped_column(String(10), comment='是否985')
    f211: Mapped[Optional[str]] = mapped_column(String(10), comment='是否211')
    department: Mapped[Optional[str]] = mapped_column(String(10), comment='部门')
    admissions: Mapped[Optional[str]] = mapped_column(String(10), comment='招生')
    central: Mapped[Optional[str]] = mapped_column(String(10), comment='中央')
    dual_class: Mapped[Optional[str]] = mapped_column(String(50), comment='双一流')
    is_seal: Mapped[Optional[str]] = mapped_column(String(10), comment='是否封印')
    applied_grade: Mapped[Optional[str]] = mapped_column(String(10), comment='应用等级')
    vocational: Mapped[Optional[str]] = mapped_column(String(10), comment='职业')
    
    # 数量统计
    num_subject: Mapped[Optional[str]] = mapped_column(String(10), comment='学科数量')
    num_master: Mapped[Optional[str]] = mapped_column(String(10), comment='硕士点数量')
    num_doctor: Mapped[Optional[str]] = mapped_column(String(10), comment='博士点数量')
    num_academician: Mapped[Optional[str]] = mapped_column(String(10), comment='院士数量')
    num_library: Mapped[Optional[str]] = mapped_column(String(50), comment='图书馆藏书量')
    num_lab: Mapped[Optional[str]] = mapped_column(String(10), comment='实验室数量')
    num_master2: Mapped[Optional[str]] = mapped_column(String(10), comment='硕士点数量2')
    num_doctor2: Mapped[Optional[str]] = mapped_column(String(10), comment='博士点数量2')
    
    # 地理位置
    province_id: Mapped[Optional[str]] = mapped_column(String(10), comment='省份ID')
    city_id: Mapped[Optional[str]] = mapped_column(String(10), comment='城市ID')
    county_id: Mapped[Optional[str]] = mapped_column(String(10), comment='县区ID')
    province_name: Mapped[Optional[str]] = mapped_column(String(50), comment='省份名称')
    city_name: Mapped[Optional[str]] = mapped_column(String(50), comment='城市名称')
    town_name: Mapped[Optional[str]] = mapped_column(String(50), comment='区县名称')
    
    # 其他信息
    is_ads: Mapped[Optional[str]] = mapped_column(String(10), comment='是否广告')
    is_recruitment: Mapped[Optional[str]] = mapped_column(String(10), comment='是否招生')
    create_date: Mapped[Optional[str]] = mapped_column(String(10), comment='创建日期')
    area: Mapped[Optional[int]] = mapped_column(Integer, comment='面积')
    old_name: Mapped[Optional[str]] = mapped_column(String(200), comment='旧名称')
    is_fenxiao: Mapped[Optional[str]] = mapped_column(String(10), comment='是否分校')
    status: Mapped[Optional[str]] = mapped_column(String(10), comment='状态')
    ad_level: Mapped[Optional[str]] = mapped_column(String(10), comment='广告等级')
    short: Mapped[Optional[str]] = mapped_column(String(200), comment='简称')
    e_pc: Mapped[Optional[str]] = mapped_column(String(10), comment='PC端')
    e_app: Mapped[Optional[str]] = mapped_column(String(10), comment='APP端')
    single: Mapped[Optional[str]] = mapped_column(String(200), comment='单独')
    colleges_level: Mapped[Optional[str]] = mapped_column(String(50), comment='学院等级')
    doublehigh: Mapped[Optional[str]] = mapped_column(String(10), comment='双高')
    
    # 排名信息
    ruanke_rank: Mapped[Optional[str]] = mapped_column(String(10), comment='软科排名')
    wsl_rank: Mapped[Optional[str]] = mapped_column(String(10), comment='WSL排名')
    qs_rank: Mapped[Optional[str]] = mapped_column(String(10), comment='QS排名')
    xyh_rank: Mapped[Optional[str]] = mapped_column(String(10), comment='校友会排名')
    eol_rank: Mapped[Optional[str]] = mapped_column(String(10), comment='EOL排名')
    us_rank: Mapped[Optional[str]] = mapped_column(String(10), comment='US排名')
    qs_world: Mapped[Optional[str]] = mapped_column(String(10), comment='QS世界排名')
    
    # 其他字段
    school_batch: Mapped[Optional[str]] = mapped_column(String(200), comment='学校批次')
    is_logo: Mapped[Optional[str]] = mapped_column(String(10), comment='是否有logo')
    ai_status: Mapped[Optional[str]] = mapped_column(String(10), comment='AI状态')
    is_ads2: Mapped[Optional[str]] = mapped_column(String(10), comment='是否广告2')
    coop_money: Mapped[Optional[str]] = mapped_column(String(20), comment='合作金额')
    bdold_name: Mapped[Optional[str]] = mapped_column(String(200), comment='百度旧名称')
    college_employment: Mapped[Optional[str]] = mapped_column(String(10), comment='学院就业')
    xyq_id: Mapped[Optional[str]] = mapped_column(String(10), comment='校友圈ID')
    senior_status: Mapped[Optional[str]] = mapped_column(String(10), comment='高级状态')
    senior_show: Mapped[Optional[str]] = mapped_column(String(10), comment='高级显示')
    is_upgrade: Mapped[Optional[str]] = mapped_column(String(10), comment='是否升级')
    view_total_show: Mapped[Optional[str]] = mapped_column(String(10), comment='总浏览显示')
    gb_show: Mapped[Optional[str]] = mapped_column(String(10), comment='国标显示')
    gbh_num: Mapped[Optional[str]] = mapped_column(String(10), comment='国标号码')
    motto: Mapped[Optional[str]] = mapped_column(Text, comment='校训')
    upgrading_rate: Mapped[Optional[str]] = mapped_column(String(10), comment='升学率')
    recommend_master_rate: Mapped[Optional[str]] = mapped_column(String(10), comment='推荐硕士率')
    recommend_master_level: Mapped[Optional[int]] = mapped_column(Integer, comment='推荐硕士等级')
    is_show_xcxcode: Mapped[Optional[int]] = mapped_column(Integer, comment='是否显示小程序码')
    
    # 名称字段
    level_name: Mapped[Optional[str]] = mapped_column(String(50), comment='层次名称')
    type_name: Mapped[Optional[str]] = mapped_column(String(50), comment='类型名称')
    school_type_name: Mapped[Optional[str]] = mapped_column(String(50), comment='学校类型名称')
    school_nature_name: Mapped[Optional[str]] = mapped_column(String(50), comment='学校性质名称')
    dual_class_name: Mapped[Optional[str]] = mapped_column(String(50), comment='双一流名称')
    
    # JSON字段
    xueke_rank: Mapped[Optional[dict]] = mapped_column(JSON, comment='学科排名')
    province_single: Mapped[Optional[dict]] = mapped_column(JSON, comment='省份单独')
    single_year: Mapped[Optional[int]] = mapped_column(Integer, comment='单独年份')
    remark: Mapped[Optional[list]] = mapped_column(JSON, comment='备注')
    
    # 联系信息
    email: Mapped[Optional[str]] = mapped_column(String(100), comment='邮箱')
    school_email: Mapped[Optional[str]] = mapped_column(String(100), comment='学校邮箱')
    address: Mapped[Optional[str]] = mapped_column(Text, comment='地址')
    postcode: Mapped[Optional[str]] = mapped_column(String(20), comment='邮编')
    site: Mapped[Optional[str]] = mapped_column(String(200), comment='网站')
    school_site: Mapped[Optional[str]] = mapped_column(String(200), comment='学校网站')
    phone: Mapped[Optional[str]] = mapped_column(String(100), comment='电话')
    school_phone: Mapped[Optional[str]] = mapped_column(String(100), comment='学校电话')
    miniprogram: Mapped[Optional[str]] = mapped_column(String(200), comment='小程序')
    content: Mapped[Optional[str]] = mapped_column(Text, comment='内容介绍')
    
    # 其他链接和信息
    weiwangzhan: Mapped[Optional[str]] = mapped_column(String(200), comment='微网站')
    yjszs: Mapped[Optional[str]] = mapped_column(String(200), comment='研究生招生')
    xiaoyuan: Mapped[Optional[str]] = mapped_column(String(200), comment='校园')
    urllinks: Mapped[Optional[dict]] = mapped_column(JSON, comment='URL链接')
    video: Mapped[Optional[dict]] = mapped_column(JSON, comment='视频')
    video_pc: Mapped[Optional[dict]] = mapped_column(JSON, comment='PC视频')
    is_video: Mapped[Optional[int]] = mapped_column(Integer, comment='是否有视频')
    
    # 特色和排名
    dualclass: Mapped[Optional[list]] = mapped_column(JSON, comment='双一流')
    school_special_num: Mapped[Optional[int]] = mapped_column(Integer, comment='学校特色数量')
    province_score_year: Mapped[Optional[str]] = mapped_column(String(10), comment='省份分数年份')
    rank: Mapped[Optional[dict]] = mapped_column(JSON, comment='排名信息')
    
    # 分校信息
    fenxiao: Mapped[Optional[list]] = mapped_column(JSON, comment='分校')
    gbh_url: Mapped[Optional[str]] = mapped_column(String(200), comment='国标URL')
    
    # 艺考相关
    is_yikao: Mapped[Optional[int]] = mapped_column(Integer, comment='是否艺考')
    yk_feature: Mapped[Optional[list]] = mapped_column(JSON, comment='艺考特色')
    yk_type: Mapped[Optional[list]] = mapped_column(JSON, comment='艺考类型')
    
    # 国际化
    is_international_undergraduate: Mapped[Optional[int]] = mapped_column(Integer, comment='是否国际本科')
    is_evaluation: Mapped[Optional[int]] = mapped_column(Integer, comment='是否评估')
    is_special_project: Mapped[Optional[int]] = mapped_column(Integer, comment='是否特殊项目')
    single_province: Mapped[Optional[dict]] = mapped_column(JSON, comment='单独省份')
    
    # MD5校验
    md5: Mapped[Optional[str]] = mapped_column(String(50), comment='MD5校验值')
    
    # 关联关系 - SQLAlchemy 2.0 风格
    master_degrees: Mapped[List["MasterDegree"]] = relationship(back_populates="school", cascade="all, delete-orphan")
    doctor_degrees: Mapped[List["DoctorDegree"]] = relationship(back_populates="school", cascade="all, delete-orphan")
    subjects: Mapped[List["Subject"]] = relationship(back_populates="school", cascade="all, delete-orphan")
    specialties: Mapped[List["Specialty"]] = relationship(back_populates="school", cascade="all, delete-orphan")
    
    # 索引
    __table_args__ = (
        Index('idx_school_name', 'name'),
        Index('idx_school_province_city', 'province_name', 'city_name'),
        Index('idx_school_type', 'type_name'),
        Index('idx_school_985_211', 'f985', 'f211'),
    )


class MasterDegree(GaokaoDatabase):
    """硕士学位授权点表"""
    __tablename__ = 'master_degrees'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    school_id: Mapped[str] = mapped_column(String(50), ForeignKey('gaokao.schools.school_id'), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment='学位名称')
    num: Mapped[Optional[str]] = mapped_column(String(10), comment='数量')
    
    school: Mapped["School"] = relationship(back_populates="master_degrees")


class DoctorDegree(GaokaoDatabase):
    """博士学位授权点表"""
    __tablename__ = 'doctor_degrees'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    school_id: Mapped[str] = mapped_column(String(50), ForeignKey('gaokao.schools.school_id'), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment='学位名称')
    num: Mapped[Optional[str]] = mapped_column(String(10), comment='数量')
    
    school: Mapped["School"] = relationship(back_populates="doctor_degrees")


class Subject(GaokaoDatabase):
    """学科表"""
    __tablename__ = 'subjects'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    school_id: Mapped[str] = mapped_column(String(50), ForeignKey('gaokao.schools.school_id'), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment='学科名称')
    
    school: Mapped["School"] = relationship(back_populates="subjects")


class Specialty(GaokaoDatabase):
    """专业表"""
    __tablename__ = 'specialties'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    specialty_id: Mapped[Optional[str]] = mapped_column(String(50), comment='专业ID')
    school_id: Mapped[str] = mapped_column(String(50), ForeignKey('gaokao.schools.school_id'), nullable=False)
    special_id: Mapped[Optional[str]] = mapped_column(String(50), comment='特殊ID')
    nation_feature: Mapped[Optional[str]] = mapped_column(String(10), comment='国家特色')
    province_feature: Mapped[Optional[str]] = mapped_column(String(10), comment='省级特色')
    is_important: Mapped[Optional[str]] = mapped_column(String(10), comment='是否重要')
    limit_year: Mapped[Optional[str]] = mapped_column(String(20), comment='学制年限')
    year: Mapped[Optional[str]] = mapped_column(String(10), comment='年份')
    level3_weight: Mapped[Optional[str]] = mapped_column(String(10), comment='三级权重')
    nation_first_class: Mapped[Optional[str]] = mapped_column(String(10), comment='国家一流')
    xueke_rank: Mapped[Optional[str]] = mapped_column(String(10), comment='学科排名')
    xueke_rank_score: Mapped[Optional[str]] = mapped_column(String(10), comment='学科排名分数')
    ruanke_rank: Mapped[Optional[str]] = mapped_column(String(10), comment='软科排名')
    ruanke_level: Mapped[Optional[str]] = mapped_column(String(10), comment='软科等级')
    is_video: Mapped[Optional[int]] = mapped_column(Integer, comment='是否有视频')
    special_name: Mapped[Optional[str]] = mapped_column(String(200), comment='专业名称')
    level_name: Mapped[Optional[str]] = mapped_column(String(50), comment='层次名称')
    
    school: Mapped["School"] = relationship(back_populates="specialties")
    
    # 索引
    __table_args__ = (
        Index('idx_specialty_name', 'special_name'),
        Index('idx_specialty_school', 'school_id'),
        Index('idx_specialty_features', 'nation_feature', 'province_feature'),
    )


# 用于JSON数据转换的工具函数
def json_to_school_orm(json_data: dict) -> School:
    """将JSON数据转换为School ORM对象"""
    data = json_data.get('data', {})
    
    school = School(
        school_id=data.get('school_id'),
        data_code=data.get('data_code'),
        name=data.get('name'),
        type=data.get('type'),
        school_type=data.get('school_type'),
        school_nature=data.get('school_nature'),
        level=data.get('level'),
        code_enroll=data.get('code_enroll'),
        zs_code=data.get('zs_code'),
        belong=data.get('belong'),
        f985=data.get('f985'),
        f211=data.get('f211'),
        department=data.get('department'),
        admissions=data.get('admissions'),
        central=data.get('central'),
        dual_class=data.get('dual_class'),
        is_seal=data.get('is_seal'),
        applied_grade=data.get('applied_grade'),
        vocational=data.get('vocational'),
        num_subject=data.get('num_subject'),
        num_master=data.get('num_master'),
        num_doctor=data.get('num_doctor'),
        num_academician=data.get('num_academician'),
        num_library=data.get('num_library'),
        num_lab=data.get('num_lab'),
        num_master2=data.get('num_master2'),
        num_doctor2=data.get('num_doctor2'),
        province_id=data.get('province_id'),
        city_id=data.get('city_id'),
        county_id=data.get('county_id'),
        province_name=data.get('province_name'),
        city_name=data.get('city_name'),
        town_name=data.get('town_name'),
        is_ads=data.get('is_ads'),
        is_recruitment=data.get('is_recruitment'),
        create_date=data.get('create_date'),
        area=data.get('area'),
        old_name=data.get('old_name'),
        is_fenxiao=data.get('is_fenxiao'),
        status=data.get('status'),
        ad_level=data.get('ad_level'),
        short=data.get('short'),
        e_pc=data.get('e_pc'),
        e_app=data.get('e_app'),
        single=data.get('single'),
        colleges_level=data.get('colleges_level'),
        doublehigh=data.get('doublehigh'),
        ruanke_rank=data.get('ruanke_rank'),
        wsl_rank=data.get('wsl_rank'),
        qs_rank=data.get('qs_rank'),
        xyh_rank=data.get('xyh_rank'),
        eol_rank=data.get('eol_rank'),
        us_rank=data.get('us_rank'),
        qs_world=data.get('qs_world'),
        school_batch=data.get('school_batch'),
        is_logo=data.get('is_logo'),
        ai_status=data.get('ai_status'),
        is_ads2=data.get('is_ads2'),
        coop_money=data.get('coop_money'),
        bdold_name=data.get('bdold_name'),
        college_employment=data.get('college_employment'),
        xyq_id=data.get('xyq_id'),
        senior_status=data.get('senior_status'),
        senior_show=data.get('senior_show'),
        is_upgrade=data.get('is_upgrade'),
        view_total_show=data.get('view_total_show'),
        gb_show=data.get('gb_show'),
        gbh_num=data.get('gbh_num'),
        motto=data.get('motto'),
        upgrading_rate=data.get('upgrading_rate'),
        recommend_master_rate=data.get('recommend_master_rate'),
        recommend_master_level=data.get('recommend_master_level'),
        is_show_xcxcode=data.get('is_show_xcxcode'),
        level_name=data.get('level_name'),
        type_name=data.get('type_name'),
        school_type_name=data.get('school_type_name'),
        school_nature_name=data.get('school_nature_name'),
        dual_class_name=data.get('dual_class_name'),
        xueke_rank=data.get('xueke_rank'),
        province_single=data.get('province_single'),
        single_year=data.get('single_year'),
        remark=data.get('remark'),
        email=data.get('email'),
        school_email=data.get('school_email'),
        address=data.get('address'),
        postcode=data.get('postcode'),
        site=data.get('site'),
        school_site=data.get('school_site'),
        phone=data.get('phone'),
        school_phone=data.get('school_phone'),
        miniprogram=data.get('miniprogram'),
        content=data.get('content'),
        weiwangzhan=data.get('weiwangzhan'),
        yjszs=data.get('yjszs'),
        xiaoyuan=data.get('xiaoyuan'),
        urllinks=data.get('urllinks'),
        video=data.get('video'),
        video_pc=data.get('video_pc'),
        is_video=data.get('is_video'),
        dualclass=data.get('dualclass'),
        school_special_num=data.get('school_special_num'),
        province_score_year=data.get('province_score_year'),
        rank=data.get('rank'),
        fenxiao=data.get('fenxiao'),
        gbh_url=data.get('gbh_url'),
        is_yikao=data.get('is_yikao'),
        yk_feature=data.get('yk_feature'),
        yk_type=data.get('yk_type'),
        is_international_undergraduate=data.get('is_international_undergraduate'),
        is_evaluation=data.get('is_evaluation'),
        is_special_project=data.get('is_special_project'),
        single_province=data.get('single_province'),
        md5=json_data.get('md5')
    )
    
    return school


def json_to_master_degrees(json_data: dict, school_id: str) -> List[MasterDegree]:
    """将JSON数据转换为MasterDegree ORM对象列表"""
    data = json_data.get('data', {})
    master_arr = data.get('master_arr', [])
    
    master_degrees = []
    for item in master_arr:
        master_degree = MasterDegree(
            school_id=school_id,
            name=item.get('name'),
            num=item.get('num')
        )
        master_degrees.append(master_degree)
    
    return master_degrees


def json_to_doctor_degrees(json_data: dict, school_id: str) -> List[DoctorDegree]:
    """将JSON数据转换为DoctorDegree ORM对象列表"""
    data = json_data.get('data', {})
    doctor_arr = data.get('doctor_arr', [])
    
    doctor_degrees = []
    for item in doctor_arr:
        doctor_degree = DoctorDegree(
            school_id=school_id,
            name=item.get('name'),
            num=item.get('num')
        )
        doctor_degrees.append(doctor_degree)
    
    return doctor_degrees


def json_to_subjects(json_data: dict, school_id: str) -> List[Subject]:
    """将JSON数据转换为Subject ORM对象列表"""
    data = json_data.get('data', {})
    subject_arr = data.get('subject_arr', [])
    
    subjects = []
    for item in subject_arr:
        if isinstance(item, dict) and 'name' in item:
            subject = Subject(
                school_id=school_id,
                name=item.get('name')
            )
            subjects.append(subject)
    
    return subjects


def json_to_specialties(json_data: dict, school_id: str) -> List[Specialty]:
    """将JSON数据转换为Specialty ORM对象列表"""
    data = json_data.get('data', {})
    special_arr = data.get('special', [])
    
    specialties = []
    for item in special_arr:
        specialty = Specialty(
            specialty_id=item.get('id'),
            school_id=school_id,
            special_id=item.get('special_id'),
            nation_feature=item.get('nation_feature'),
            province_feature=item.get('province_feature'),
            is_important=item.get('is_important'),
            limit_year=item.get('limit_year'),
            year=item.get('year'),
            level3_weight=item.get('level3_weight'),
            nation_first_class=item.get('nation_first_class'),
            xueke_rank=item.get('xueke_rank'),
            xueke_rank_score=item.get('xueke_rank_score'),
            ruanke_rank=item.get('ruanke_rank'),
            ruanke_level=item.get('ruanke_level'),
            is_video=item.get('is_video'),
            special_name=item.get('special_name'),
            level_name=item.get('level_name')
        )
        specialties.append(specialty)
    
    return specialties


def json_to_orm_objects(json_data: dict) -> tuple[School, List[MasterDegree], List[DoctorDegree], List[Subject], List[Specialty]]:
    """将完整的JSON数据转换为所有相关的ORM对象"""
    school = json_to_school_orm(json_data)
    school_id = json_data.get('data', {}).get('school_id')
    
    master_degrees = json_to_master_degrees(json_data, school_id)
    doctor_degrees = json_to_doctor_degrees(json_data, school_id)
    subjects = json_to_subjects(json_data, school_id)
    specialties = json_to_specialties(json_data, school_id)
    
    return school, master_degrees, doctor_degrees, subjects, specialties