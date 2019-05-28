from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'login/',views.login,name='login'),
    path(r'register/',views.register,name='register'),
    path(r'paper/',views.paper,name='paper'),
    path(r'question/',views.question,name='question'),
    path(r'enter_question/',views.enter_questions,name='enter_question'),
    path(r'add_school/',views.add_school,name='add_school'),
    path(r'add_subject/',views.add_subject,name='add_subject'),
    path(r'get_enterquestionpage/',views.get_enterquestionpage,name='get_enterquestionpage'),
    path(r'postpaperinfo/',views.postpaperinfo,name='postpaperinfo'),
    path(r'getmanualpaperquestion/',views.getmanualpaperquestion,name='getmanualpaperquestion'),
    path(r'loadpaper/',views.loadpaper,name='loadpaper'),
    path(r'getautopaper/',views.getautopaper,name='getautopaper'),
    path(r'paper_detail/<int:paper_id>',views.paper_detail,name='paper_detail'),
    path(r'question_detail/<int:question_id>',views.question_detail,name='question_detail'),
    # 未测试
    path(r'alter_question/<int:question_id>',views.alter_question,name='alter_question'),
    path(r'delete_question/<int:question_id>',views.delete_question,name='delete_question'),
    path(r'alter_point/<int:question_id>',views.alter_point,name='alter_point'),
    path(r'alter_paper/<int:paper_id>',views.alter_paper,name='alter_paper'),
    path(r'delete_paper/<int:paper_id>',views.delete_paper,name='delete_paper'),
    path(r'delete_paperdetail/',views.delete_paperdetail,name='delete_paperdetail'),
    path(r'cascader/',views.cascader,name='cascader'),
    path(r'uploadImg/',views.uploadImg,name='uploagImg'),
    path(r'add_question/<int:question_id>',views.add_question,name="add_question")
]