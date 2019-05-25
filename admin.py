# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Grade,Subject,User,Question,Paper,Paper_detail,Knowledge1,Knowledge2,School
# Register your models here.

def decode(info):
    return info.decode('utf-8')

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    search_fields = ['school']
    list_display = ['school','school_info']
    list_display_links = ['school','school_info']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    search_fields = ['grade']
    list_display = ['grade']
    list_display_links = ['grade']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['subject']
    list_display = ['subject']
    list_display_links = ['subject']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['user_name','email','role']
    list_display = ['user_name','email','role','password']
    list_display_links = ['user_name','email','role','password']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['text','types','subject','grade','school','difficult','user']
    list_display = ['text','types','option1','option2','option3','option4','subject','grade','knowledge1','knowledge2','school','difficult','answer','photo','formula','user']
    list_display_links = ['text','types','option1','option2','option3','option4','subject','grade','knowledge1','knowledge2','school','difficult','answer','photo','formula','user']

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    search_fields = ['name','subject','school','grade','user']
    list_display = ['name','subject','grade','school','points','user']
    list_display_links = ['name','subject','school','grade','points','user']

@admin.register(Paper_detail)
class PaperdateilAdmin(admin.ModelAdmin):
    search_fields = ['paper','question','point']
    list_display = ['paper','question','point']
    list_display_links = ['paper','question','point']

@admin.register(Knowledge1)
class Knowledge1Admin(admin.ModelAdmin):
    list_display = ['knowledge1','subject']
    list_display_links = ['knowledge1','subject']

@admin.register(Knowledge2)
class Knowledge1Admin(admin.ModelAdmin):
    list_display = ['knowledge2', 'knowledge1']
    list_display_links = ['knowledge2', 'knowledge1']