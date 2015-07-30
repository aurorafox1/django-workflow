# -.- coding:utf-8 -.-
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Menu(MPTTModel):
    name = models.CharField(max_length=50, unique=True,verbose_name="菜单名")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    url = models.CharField(max_length=200, verbose_name="路径")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="图标")
    class Meta:
        verbose_name = "菜单表"
        verbose_name_plural = "菜单表"
    def __str__(self):
        return self.name

class Department(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="部门名称")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    desc = models.TextField(max_length=1000, blank=True, null=True, verbose_name="部门描述")
    class Meta:
        verbose_name = "部门表"
        verbose_name_plural = "部门表"
    def __str__(self):
        return self.name

class UserRole(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="角色名称")
    permission = models.ManyToManyField(Menu)
    desc = models.TextField(max_length=1000, blank=True, null=True, verbose_name="角色描述")
    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = "角色表"
    def __str__(self):
        return self.name

class UserExt(MPTTModel):
    user = models.OneToOneField(User)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    department = models.ManyToManyField(Department)
    role = models.ForeignKey(UserRole)
    real_name = models.CharField(max_length=20, unique=True, verbose_name="中文姓名")
    phone = models.CharField(max_length=11, verbose_name="手机号码")
    telephone = models.CharField(max_length=11, verbose_name="分机号")
    def __str__(self):
        return self.real_name

		
class FlowOpera(models.Model):
    """流程操作表:1. 提交  2. 打回  3. 同意  4. 不同意  5. 关闭"""
    name = models.CharField(max_length=10, verbose_name="操作类型")

    class Meta:
        verbose_name = "00_流程操作类型表"
        verbose_name_plural = "00_流程操作类型表"

    def __str__(self):
        return self.name

class FlowName(models.Model):
    """流程名称表"""
    is_static_flow = (
        ("1", "固定流程"),
        ("2", "非固定流程")
    )

    remind_type = (
        ("1", "邮箱"),
        ("2", "短信"),
        ("3", "语音外呼"),
    )

    name = models.CharField(max_length=20, verbose_name="流程名称")
    type = models.CharField(max_length=20, choices=is_static_flow, default=1, verbose_name="流程类型")
    remind = models.CharField(max_length=20, choices=remind_type, default=1, verbose_name="提醒方式")
    diagrams = models.FileField(upload_to=settings.STATICFILES_DIRS[0]+"/files", null=True, blank=True, verbose_name="流程图")
    desc = models.TextField(max_length=2000, null=True, blank=True, verbose_name="流程描述")

    class Meta:
        verbose_name = "01_流程名称"
        verbose_name_plural = "01_流程名称"

    def __str__(self):
        return self.name

class FlowStatus(models.Model):
    """流程状态表"""
    flowname = models.ForeignKey(FlowName)
    name = models.CharField(max_length=20, verbose_name="步骤名称")
    desc = models.TextField(max_length=2000, null=True, blank=True, verbose_name="步骤描述")

    class Meta:
        verbose_name = "02_流程状态表"
        verbose_name_plural = "02_流程状态表"

    def __str__(self):
        return self.name

class FlowTrans(models.Model):
    """流程流转表: 定制当前步骤的下一步是哪里."""
    approve_type = (
        ("1", "普通"),
        ("2", "直属领导审批"),
        ("3", "部门领导审批"),
    )
    flowname = models.ForeignKey(FlowName, verbose_name="流程名称")
    flowstep = models.ForeignKey(FlowStatus, verbose_name="步骤名字", related_name="cur_status")
    condition = models.CharField(max_length=20, choices=approve_type, default=1, verbose_name="步骤类型")
    transtion = models.ForeignKey(FlowStatus, verbose_name="下一步名字", related_name="dest_status")

    class Meta:
        verbose_name = "03_流程流转表"
        verbose_name_plural = "03_流程流转表"

    def __str__(self):
        return self.get_condition_display()

class FlowPerms(models.Model):
    """流程权限表: 定制每个步骤的操作权限和用户可视化权限."""
    flowname = models.ForeignKey(FlowName, verbose_name="流程名称")
    flowstep = models.ForeignKey(FlowStatus, verbose_name="步骤名称")
    flowopera = models.ManyToManyField(FlowOpera, verbose_name="操作权限")
    user = models.ManyToManyField(User, verbose_name="用户")                          # 这行代码待讨论.

    class Meta:
        verbose_name = "04_流程步骤权限表"
        verbose_name_plural = "04_流程步骤权限表"

class FlowRecord(models.Model):
    """流程流水表"""
    flowname = models.ForeignKey(FlowName, verbose_name="流程名称")
    flowstep = models.ForeignKey(FlowStatus, verbose_name="步骤名称")
    action = models.ForeignKey(FlowOpera, verbose_name="操作类型")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="操作时间")

    # 一般用于保存业务id信息.
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "05_流程步骤流水表"
        verbose_name_plural = "05_流程步骤流水表"		