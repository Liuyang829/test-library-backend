# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.

def decode(info):
    return info.decode('utf-8')


class User(models.Model):
    user_name = models.CharField('用户名', max_length=16)
    email = models.EmailField('email', max_length=32)
    role = models.CharField('身份', max_length=8)
    password=models.CharField('密码',max_length=30,default='1234')

    def __str__(self):
        return self.user_name


class Subject(models.Model):
    subject = models.CharField('科目', max_length=200)

    def __str__(self):
        return self.subject


class Grade(models.Model):
    grade = models.CharField('年级', max_length=100)

    def __str__(self):
        return self.grade


class Knowledge1(models.Model):
    knowledge1 = models.CharField('一级知识点', max_length=50)
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.knowledge1


class Knowledge2(models.Model):
    knowledge2 = models.CharField('二级知识点', max_length=50)
    knowledge1 = models.ForeignKey(Knowledge1, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.knowledge2


class School(models.Model):
    TYPES_CHOICES = (
        ('小学', '小学'),
        ('初中', '初中'),
        ('高中', '高中'),
        ('大学', '大学'),
    )
    school = models.CharField('学校', max_length=50)
    school_info = models.CharField('学校性质', max_length=50,choices=TYPES_CHOICES)

    def __str__(self):
        return self.school


class Question(models.Model):
    TYPES_CHOICES = (
        ('选择题', '选择题'),
        ('判断题', '判断题'),
        ('填空题', '填空题'),
        ('解答题', '解答题'),
    )
    DIFF_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    text = models.CharField('题目内容', max_length=300)
    types = models.CharField('题目类型', max_length=30, choices=TYPES_CHOICES)
    option1 = models.CharField('A', max_length=50, null=True, blank=True,default='null')
    option2 = models.CharField('B', max_length=50, null=True, blank=True,default='null')
    option3 = models.CharField('C', max_length=50, null=True, blank=True,default='null')
    option4 = models.CharField('D', max_length=50, null=True, blank=True,default='null')
    subject = models.ForeignKey('Subject', null=True, blank=True, on_delete=models.SET_NULL)
    grade = models.ForeignKey('Grade', null=True, blank=True, on_delete=models.SET_NULL)
    # 外键有问题
    knowledge1 = models.ForeignKey(Knowledge1, null=True, blank=True, on_delete=models.SET_NULL)
    knowledge2 = models.ForeignKey(Knowledge2, null=True, blank=True, on_delete=models.SET_NULL)
    school = models.ForeignKey(School, null=True, blank=True, on_delete=models.SET_NULL)
    difficult = models.IntegerField('难度系数', default=0, choices=DIFF_CHOICES)
    answer = models.CharField('答案', max_length=300)
    photo = models.CharField('图片', max_length=50, null=True, blank=True)
    formula = models.CharField('公式', max_length=50, null=True, blank=True)
    user= models.CharField('录人员', default=0,max_length=50)

    def __str__(self):
        return self.text


class Paper(models.Model):
    name = models.CharField('试卷名称', max_length=50)
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL)
    grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.SET_NULL)
    school = models.ForeignKey(School, null=True, blank=True, on_delete=models.SET_NULL)
    points = models.IntegerField('总分')
    user = models.CharField('录人员',max_length=30,default=0)

    def __str__(self):
        return self.name


class Paper_detail(models.Model):
    paper = models.ForeignKey(Paper, null=True, blank=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.SET_NULL)
    point=models.IntegerField('分数',default=0)
