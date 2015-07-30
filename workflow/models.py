# -.- coding:utf-8 -.-
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Menu(MPTTModel):
    name = models.CharField(max_length=50, unique=True,verbose_name="�˵���")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    url = models.CharField(max_length=200, verbose_name="·��")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="ͼ��")
    class Meta:
        verbose_name = "�˵���"
        verbose_name_plural = "�˵���"
    def __str__(self):
        return self.name

class Department(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="��������")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    desc = models.TextField(max_length=1000, blank=True, null=True, verbose_name="��������")
    class Meta:
        verbose_name = "���ű�"
        verbose_name_plural = "���ű�"
    def __str__(self):
        return self.name

class UserRole(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="��ɫ����")
    permission = models.ManyToManyField(Menu)
    desc = models.TextField(max_length=1000, blank=True, null=True, verbose_name="��ɫ����")
    class Meta:
        verbose_name = "��ɫ��"
        verbose_name_plural = "��ɫ��"
    def __str__(self):
        return self.name

class UserExt(MPTTModel):
    user = models.OneToOneField(User)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    department = models.ManyToManyField(Department)
    role = models.ForeignKey(UserRole)
    real_name = models.CharField(max_length=20, unique=True, verbose_name="��������")
    phone = models.CharField(max_length=11, verbose_name="�ֻ�����")
    telephone = models.CharField(max_length=11, verbose_name="�ֻ���")
    def __str__(self):
        return self.real_name

		
class FlowOpera(models.Model):
    """���̲�����:1. �ύ  2. ���  3. ͬ��  4. ��ͬ��  5. �ر�"""
    name = models.CharField(max_length=10, verbose_name="��������")

    class Meta:
        verbose_name = "00_���̲������ͱ�"
        verbose_name_plural = "00_���̲������ͱ�"

    def __str__(self):
        return self.name

class FlowName(models.Model):
    """�������Ʊ�"""
    is_static_flow = (
        ("1", "�̶�����"),
        ("2", "�ǹ̶�����")
    )

    remind_type = (
        ("1", "����"),
        ("2", "����"),
        ("3", "�������"),
    )

    name = models.CharField(max_length=20, verbose_name="��������")
    type = models.CharField(max_length=20, choices=is_static_flow, default=1, verbose_name="��������")
    remind = models.CharField(max_length=20, choices=remind_type, default=1, verbose_name="���ѷ�ʽ")
    diagrams = models.FileField(upload_to=settings.STATICFILES_DIRS[0]+"/files", null=True, blank=True, verbose_name="����ͼ")
    desc = models.TextField(max_length=2000, null=True, blank=True, verbose_name="��������")

    class Meta:
        verbose_name = "01_��������"
        verbose_name_plural = "01_��������"

    def __str__(self):
        return self.name

class FlowStatus(models.Model):
    """����״̬��"""
    flowname = models.ForeignKey(FlowName)
    name = models.CharField(max_length=20, verbose_name="��������")
    desc = models.TextField(max_length=2000, null=True, blank=True, verbose_name="��������")

    class Meta:
        verbose_name = "02_����״̬��"
        verbose_name_plural = "02_����״̬��"

    def __str__(self):
        return self.name

class FlowTrans(models.Model):
    """������ת��: ���Ƶ�ǰ�������һ��������."""
    approve_type = (
        ("1", "��ͨ"),
        ("2", "ֱ���쵼����"),
        ("3", "�����쵼����"),
    )
    flowname = models.ForeignKey(FlowName, verbose_name="��������")
    flowstep = models.ForeignKey(FlowStatus, verbose_name="��������", related_name="cur_status")
    condition = models.CharField(max_length=20, choices=approve_type, default=1, verbose_name="��������")
    transtion = models.ForeignKey(FlowStatus, verbose_name="��һ������", related_name="dest_status")

    class Meta:
        verbose_name = "03_������ת��"
        verbose_name_plural = "03_������ת��"

    def __str__(self):
        return self.get_condition_display()

class FlowPerms(models.Model):
    """����Ȩ�ޱ�: ����ÿ������Ĳ���Ȩ�޺��û����ӻ�Ȩ��."""
    flowname = models.ForeignKey(FlowName, verbose_name="��������")
    flowstep = models.ForeignKey(FlowStatus, verbose_name="��������")
    flowopera = models.ManyToManyField(FlowOpera, verbose_name="����Ȩ��")
    user = models.ManyToManyField(User, verbose_name="�û�")                          # ���д��������.

    class Meta:
        verbose_name = "04_���̲���Ȩ�ޱ�"
        verbose_name_plural = "04_���̲���Ȩ�ޱ�"

class FlowRecord(models.Model):
    """������ˮ��"""
    flowname = models.ForeignKey(FlowName, verbose_name="��������")
    flowstep = models.ForeignKey(FlowStatus, verbose_name="��������")
    action = models.ForeignKey(FlowOpera, verbose_name="��������")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="����ʱ��")

    # һ�����ڱ���ҵ��id��Ϣ.
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "05_���̲�����ˮ��"
        verbose_name_plural = "05_���̲�����ˮ��"		