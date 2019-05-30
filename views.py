from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import Img, Grade, Subject, User, Question, Paper, Paper_detail, Knowledge1, Knowledge2, School
import random
import json
import os,pypandoc
import codecs


def index(request):
    return HttpResponse("Hello, world. You're at the test_library index.")


@csrf_exempt
def login(request):
    res_data = {'isOK': False, 'errmsg': '未知错误', 'data': 'null'}
    if request.method == 'POST':
        # data=request.POST
        username = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        # print(data)
        # username=data.get('username')
        # pwd=data.get('password')
        print(username, pwd)

        if username and pwd:
            user = User.objects.filter(
                user_name=username,
            )
            if user.exists():
                user = user.first()
                print('查到', user)
                user_obj = User.objects.filter(user_name=user, password=pwd).first()
                if user_obj:
                    print("okk")
                    res_data['isOK'] = True
                    res_data['errmsg'] = '登陆成功'
                    res_data['data'] = username
                else:
                    print("密码错误")
                    res_data['errmsg'] = '密码错误'
            else:
                print("用户名不存在")
                res_data['errmsg'] = '用户名不存在'
        else:
            print("账号或密码为空")
            res_data['errmsg'] = '账号或密码为空'
    return JsonResponse(res_data)


@csrf_exempt
def register(request):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        pwd = request.POST.get('pwd')
        re_pwd = request.POST.get('re_pwd')
        if name and email and role and pwd and re_pwd:
            if pwd == re_pwd:
                user_obj = User.objects.filter(user_name=name).first()
                if user_obj:
                    res_data['errmsg'] = '用户已存在'
                else:
                    User.objects.create(user_name=name, email=email, role=role, password=pwd).save()
                    res_data['isOK'] = True
                    res_data['errmsg'] = '注册成功'
            else:
                res_data['errmsg'] = '两次密码不一致'
        else:
            res_data['errmsg'] = '不能有空！'
    return JsonResponse(res_data)


# 将数据库中所拿到的多条试题的信息全部转换成json的格式放进一个list中 返回一个list
# a 为数据库查找结果arrayset
def paperlist_tojson(a):
    PaperList = []
    for i in a:
        PaperData_each = {'id': 'null', 'name': 'null', 'points': 'null', 'subject': 'null', 'grade': 'null',
                          'school': 'null'}
        PaperData_each['id'] = i.id
        PaperData_each['name'] = i.name
        PaperData_each['points'] = i.points
        PaperData_each['subject'] = Subject.objects.get(id=i.subject_id).subject
        PaperData_each['grade'] = Grade.objects.get(id=i.grade_id).grade
        PaperData_each['school'] = School.objects.get(id=i.school_id).school
        PaperList.append(PaperData_each)
    return PaperList


# 将数据库中所拿到的多条问题的信息全部转换成json的格式放进一个list中 返回一个list
# a 为数据库查找结果arrayset
def questionlist_tojsonlist(a):
    QuestionList = []
    for i in a:
        QuestionData_each = {'id': 'null', 'text': 'null', 'types': 'null',  'difficult': 'null', 'answer': 'null',
                              'grade': 'null', 'knowledge1': 'null','number':'null',
                             'knowledge2': 'null', 'school': 'null', 'school_info': 'null', 'subject': 'null'}
        QuestionData_each['id'] = i.id
        QuestionData_each['text'] = i.text
        QuestionData_each['types'] = i.types
        if i.difficult==1:
            QuestionData_each['difficult'] = "简单"
        if i.difficult==2:
            QuestionData_each['difficult'] = "一般"
        if i.difficult == 3:
            QuestionData_each['difficult'] = "困难"
        QuestionData_each['answer'] = i.answer
        QuestionData_each['number']=len(Paper_detail.objects.filter(question_id=i.id))
        QuestionData_each['grade'] = Grade.objects.get(id=i.grade_id).grade
        QuestionData_each['knowledge1'] = Knowledge1.objects.get(id=i.knowledge1_id).knowledge1
        QuestionData_each['knowledge2'] = Knowledge2.objects.get(id=i.knowledge2_id).knowledge2
        QuestionData_each['school'] = School.objects.get(id=i.school_id).school
        QuestionData_each['school_info'] = School.objects.get(id=i.school_id).school_info
        QuestionData_each['subject'] = Subject.objects.get(id=i.subject_id).subject
        QuestionList.append(QuestionData_each)
    return QuestionList


# 获得所有试卷信息-首页
@csrf_exempt
def paper(request):
    if request.method == 'POST':
        PaperList = []
        PaperInfo = Paper.objects.all()
        PaperList = paperlist_tojson(PaperInfo)
    return JsonResponse(PaperList, safe=False)


# 获得所有试题信息-试题库页面-已测试
@csrf_exempt
def question(request):
    if request.method == 'POST':
        QuestionInfo = Question.objects.all()
        print(QuestionInfo)
        print(QuestionInfo.first())
        QuestionList = questionlist_tojsonlist(QuestionInfo)
        print(QuestionList)
    return JsonResponse(QuestionList, safe=False)


@csrf_exempt
def add_school(request):
    res_data = {'isOK': False, 'errmsg': '未知错误', 'school': 'null'}
    if request.method == 'POST':
        school = request.POST.get('school')
        school_info = request.POST.get('school_info')  # 新增学校需提交新增学校信息
        print(school, school_info)
        if school and school_info:
            school_obj = School.objects.filter(school=school)
            if school_obj.exists():
                pass
            else:
                print("新增学校", school, school_info)
                School.objects.create(school=school, school_info=school_info).save()
                res_data['isOK'] = True
        else:
            res_data['errmsg'] = '存在空值'
        schoollist = []
        SchoolData = School.objects.all()
        for i in SchoolData:
            schoollist.append(i.school)
        res_data['school'] = schoollist
    return JsonResponse(res_data)


@csrf_exempt
def add_subject(request):
    res_data = {'isOK': False, 'errmsg': '未知错误', 'subjectall': 'null', 'subject_know1': 'null'}
    if request.method == 'POST':
        subject = request.POST.get('subject')
        knowledge1 = request.POST.get('knowledge1')
        knowledge2 = request.POST.get('knowledge2')
        print(subject, knowledge1, knowledge2)
        if subject and knowledge1 and knowledge2:
            subject_obj = Subject.objects.filter(subject=subject)
            if subject_obj.exists():
                pass
            else:
                print("新增科目", subject)
                Subject.objects.create(subject=subject).save()
            subject_id = Subject.objects.get(subject=subject).id

            knowledge1_obj = Knowledge1.objects.filter(knowledge1=knowledge1)
            if knowledge1_obj.exists():
                pass
            else:
                print("新增一级知识点", knowledge1, subject)
                Knowledge1.objects.create(knowledge1=knowledge1, subject_id=subject_id).save()
            knowledge1_id = Knowledge1.objects.get(knowledge1=knowledge1).id
            print("新增二级知识点", knowledge2, knowledge1)
            Knowledge2.objects.create(knowledge2=knowledge2, knowledge1_id=knowledge1_id).save()
            res_data['isOK'] = True
            subjectall, subjectall1 = cascader()
            res_data['subjectall'] = subjectall
            res_data['subject_know1'] = subjectall1
        else:
            res_data['errmsg'] = '存在空值'
    return JsonResponse(res_data)


# 录入试题存入数据库 - 已测试
@csrf_exempt
def enter_questions(request):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        text = request.POST.get('text')
        types = request.POST.get('types')
        difficult = request.POST.get('difficult')
        answer = request.POST.get('answer')
        user = request.POST.get('user')
        grade = request.POST.get('grade')
        subject = request.POST.get('subject')
        knowledge1 = request.POST.get('knowledge1')
        knowledge2 = request.POST.get('knowledge2')
        school = request.POST.get('school')
        school_info = request.POST.get('school_info')  # 新增学校需提交新增学校信息
        if text and types and difficult and answer and user and grade and knowledge1 and knowledge2 and school and subject:
            grade_id = Grade.objects.get(grade=grade).id
            # 判断表中是否已经有当前的school
            school_obj = School.objects.filter(school=school)
            if school_obj.exists():
                pass
            else:
                print("新增学校", school, school_info)
                School.objects.create(school=school, school_info=school_info).save()
            school_id = School.objects.get(school=school).id

            # 判断表中是否已经有当前的subject
            subject_obj = Subject.objects.filter(subject=subject)
            if subject_obj.exists():
                pass
            else:
                print("新增科目", subject)
                Subject.objects.create(subject=subject).save()
            subject_id = Subject.objects.get(subject=subject).id

            # 判断表中是否已经有当前的knowledge1
            knowledge1_obj = Knowledge1.objects.filter(knowledge1=knowledge1)
            if knowledge1_obj.exists():
                pass
            else:
                print("新增一级知识点", knowledge1, subject)
                Knowledge1.objects.create(knowledge1=knowledge1, subject_id=subject_id).save()
            knowledge1_id = Knowledge1.objects.get(knowledge1=knowledge1).id

            # 判断表中是否已经有当前的knowledge2
            knowledge2_obj = Knowledge2.objects.filter(knowledge2=knowledge2)
            if knowledge2_obj.exists():
                pass
            else:
                print("新增二级知识点", knowledge2, knowledge1)
                Knowledge2.objects.create(knowledge2=knowledge2, knowledge1_id=knowledge1_id).save()
            knowledge2_id = Knowledge2.objects.get(knowledge2=knowledge2).id
            print(subject_id, knowledge1_id, knowledge2_id)
            Question.objects.create(text=text, types=types, difficult=difficult, answer=answer, user=user, grade_id=grade_id, knowledge1_id=knowledge1_id,
                                        knowledge2_id=knowledge2_id, school_id=school_id, subject_id=subject_id).save()
            res_data['isOK'] = True
        else:
            print("不可为空值")
            res_data['errmsg'] = '存在空值'
    return JsonResponse(res_data)


# 为前端级联选择器构造学科-一级知识点-二级知识点的数据格式 还有两级知识点的级联选择器
@csrf_exempt
def cascader():
    cascaderlist = []
    cascaderlist2 = []
    subjectlist = Subject.objects.all()
    for subject in subjectlist:
        subject_json = {'value': 'null', 'label': 'null', 'children': 'null'}
        subject_json2 = {'value': 'null', 'label': 'null', 'children': 'null'}
        subject_children = []
        subject_children2 = []
        subject_json['value'] = subject.subject
        subject_json['label'] = subject.subject
        subject_json2['value'] = subject.subject
        subject_json2['label'] = subject.subject
        subject_id = Subject.objects.get(subject=subject).id
        knowledge1list = Knowledge1.objects.filter(subject_id=subject_id)
        for knowledge1 in knowledge1list:
            knowledge1_json = {'value': 'null', 'label': 'null', 'children': 'null'}
            knowledge1_json2 = {'value': 'null', 'label': 'null'}
            knowledge1_children = []
            knowledge1_json['value'] = knowledge1.knowledge1
            knowledge1_json['label'] = knowledge1.knowledge1
            knowledge1_json2['value'] = knowledge1.knowledge1
            knowledge1_json2['label'] = knowledge1.knowledge1
            knowledge1_id = Knowledge1.objects.get(knowledge1=knowledge1).id
            knowledge2list = Knowledge2.objects.filter(knowledge1_id=knowledge1_id)
            for knowledge2 in knowledge2list:
                knowledge2_json = {'value': 'null', 'label': 'null'}
                knowledge2_json['value'] = knowledge2.knowledge2
                knowledge2_json['label'] = knowledge2.knowledge2
                knowledge1_children.append(knowledge2_json)
            knowledge1_json['children'] = knowledge1_children
            subject_children.append(knowledge1_json)
            subject_children2.append(knowledge1_json2)
        subject_json['children'] = subject_children
        subject_json2['children'] = subject_children2
        cascaderlist2.append(subject_json2)
        cascaderlist.append(subject_json)
    return cascaderlist, cascaderlist2


# 进入录入试题页面-获得所有的下拉列表信息-已测试
@csrf_exempt
def get_enterquestionpage(request):
    if request.method == 'POST':
        res_data = {'isOK': False, 'grade': 'null', 'school': 'null', 'subject': 'null', 'subjectall': 'null',
                    'subject_know1': 'null'}
        gradelist = []
        schoollist = []
        subjectlist = []
        GradeData = Grade.objects.all()
        SchoolData = School.objects.all()
        SubjectData = Subject.objects.all()
        for i in GradeData:
            gradelist.append(i.grade)
        for i in SchoolData:
            schoollist.append(i.school)
        for i in SubjectData:
            subjectlist.append(i.subject)
        res_data['isOK'] = True
        res_data['grade'] = gradelist
        res_data['school'] = schoollist
        res_data['subject'] = subjectlist
        subjectall, subject_know1 = cascader()
        res_data['subjectall'] = subjectall
        res_data['subject_know1'] = subject_know1
    return JsonResponse(res_data)


# 手动 自动组卷用 -已测试
# 输入试卷名称 学校等信息 存入试卷表中，也就是试卷的title
# 前端数据格式为 {'name':'xxx','points':'xxx','user':'xxx','school':'xxx','grade':'xxx','subject':'xxx'}
@csrf_exempt
def postpaperinfo(request):
    res_data = {'isOK': False, 'errmsg': '未知错误', 'paper_id': 'null','knowledge1':'null'}
    if request.method == 'POST':
        name = request.POST.get('name')
        points = request.POST.get('points')
        user = request.POST.get('user')
        # 三个外键
        school = request.POST.get('school')
        grade = request.POST.get('grade')
        subject = request.POST.get('subject')
        if name and points and school and grade and subject:
            print(name,points,school,grade,subject)
            school_id = School.objects.get(school=school).id
            grade_id = Grade.objects.get(grade=grade).id
            subject_id = Subject.objects.get(subject=subject).id
            a=Paper.objects.filter(name=name)
            if len(a)!=0 :
                res_data['errmsg']="已有当前试卷，可进入试卷详情页进行修改"
            else:
                Paper.objects.create(name=name, points=points, grade_id=grade_id, school_id=school_id, user=user,
                                 subject_id=subject_id).save()
                paper_id = Paper.objects.get(name=name).id
                res_data['paper_id'] = paper_id
                k12=[]
                knowledge1list = Knowledge1.objects.filter(subject_id=subject_id)
                for knowledge1 in knowledge1list:
                    knowledge1_json = {'value': 'null', 'label': 'null', 'children': 'null'}
                    knowledge1_children = []
                    knowledge1_json['value'] = knowledge1.knowledge1
                    knowledge1_json['label'] = knowledge1.knowledge1
                    knowledge1_id = Knowledge1.objects.get(knowledge1=knowledge1).id
                    knowledge2list = Knowledge2.objects.filter(knowledge1_id=knowledge1_id)
                    for knowledge2 in knowledge2list:
                        knowledge2_json = {'value': 'null', 'label': 'null'}
                        knowledge2_json['value'] = knowledge2.knowledge2
                        knowledge2_json['label'] = knowledge2.knowledge2
                        knowledge1_children.append(knowledge2_json)
                    knowledge1_json['children'] = knowledge1_children
                    k12.append(knowledge1_json)
                res_data['knowledge1']=k12
                res_data['isOK'] = True
        else:
            res_data['errmsg'] = '存在空值'
    return JsonResponse(res_data)


# 手动组卷用，根据试题的筛选条件 返回试卷等信息 -已测试
# 前端所传递数据格式为{'grade':'xxx','subject':'xxx','knowledge1':'xxx','knowledge2':'xxx','difficult':'xxx','types':'xxx'}
@csrf_exempt
def getmanualpaperquestion(request):
    res_data = {'isOK': False, 'errmsg': '未知错误', 'questionlist': 'null'}
    if request.method == 'POST':
        grade = request.POST.get('grade')
        subject = request.POST.get('subject')
        # knowledge1 = request.POST.get('knowledge1')
        knowledge2 = request.POST.get('knowledge2')
        difficult = request.POST.get('difficult')
        types = request.POST.get('types')
        search_dict = dict()
        if grade and subject and difficult and types and knowledge2!="undefined":
            search_dict['types'] = types
            search_dict['difficult'] = difficult
            grade_id = Grade.objects.get(grade=grade).id
            subject_id = Subject.objects.get(subject=subject).id
            # knowledge1_id = Knowledge1.objects.get(knowledge1=knowledge1).id
            search_dict['grade_id'] = grade_id
            search_dict['subject_id'] = subject_id
            # search_dict['knowledge1_id'] = knowledge1_id
            knowledge2_id = Knowledge2.objects.get(knowledge2=knowledge2).id
            search_dict['knowledge2_id'] = knowledge2_id
            question_order_info = Question.objects.filter(**search_dict)
            question_info = questionlist_tojsonlist(question_order_info)
            # 应该是只打印出了题目
            print(question_info)
            res_data['questionlist'] = question_info
            if len(question_info)!=0:
                res_data['isOK'] = True
            else:
                res_data['errmsg']="题库中无符合标准的试题"
        else:
            res_data['errmsg'] = '存在空值'
    return JsonResponse(res_data)


# 自动通用
# 组卷根据选择的题目存到试卷内容表中 -已测试
# 前端所传递数据格式为
# {
#     'paper':'某某某期末试卷',
#     question_info:[
#         {
#             id:'xxxxx',
#             point:'2'
#         },
#         {
#             id:'xxxxx',
#             point:'3'
#         },
#     ]
# }
@csrf_exempt
def loadpaper(request):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        print(request.body)
        print(request.body.decode())

        a = request.body.decode()
        b = json.loads(a)
        paper = b['paper']
        question_info_list = b['question_info']
        # print(type(question_info_list))
        # print(paper, question_info_list)
        if paper and question_info_list:
            paper_id = paper
            if paper_id:
                print(paper_id)
                for i in question_info_list:
                    if i['id'] and i['point']:
                        question_id = i['id']
                        point = i['point']
                        a=Paper_detail.objects.filter(paper_id=paper_id)
                        questionid=[]
                        for i in a:
                            questionid.append(i.question_id)
                        print(questionid)
                        if question_id in questionid:
                            res_data['errmsg'] = '题库中有重复题目'
                        else:
                            Paper_detail.objects.create(paper_id=paper_id, question_id=question_id, point=point).save()
                            res_data['isOK'] = True
                    else:
                        res_data['errmsg'] = '有分数未输入'
            else:
                res_data['errmsg'] = '该试卷名为空'
    return JsonResponse(res_data)


# 根据所给科目 年级 难度系数 选择题数量 填空题数量 判断题数量 解答题数量 返回题目列表
@csrf_exempt
def getautopaper(request):
    res_data = {'isOK': False, 'errmsg': '未知错误', 'questionlist': 'null','questionidlist':'null',
                'choice_q_e': 'null', 'choice_q_n': 'null','choice_q_d': 'null',
                'filling_q_e': 'null', 'filling_q_n': 'null','filling_q_d': 'null',
                'solve_q_e': 'null', 'solve_q_n': 'null', 'solve_q_d': 'null',
                'tf_q_e': 'null','tf_q_n': 'null', 'tf_q_d': 'null'}
    QuestionList = []
    if request.method == 'POST':
        grade = request.POST.get('grade')
        subject = request.POST.get('subject')
        easy1=request.POST.get('easy')
        normal1=request.POST.get('normal')
        difficult1=request.POST.get('difficult')
        choice_question_num = request.POST.get('choice_qusetion_num')
        tf_question_num = request.POST.get('tf_qusetion_num')
        filling_question_num = request.POST.get('filling_qusetion_num')
        solve_question_num = request.POST.get('solve_qusetion_num')
        print(choice_question_num,type(choice_question_num))
        easy1=int(easy1)
        normal1=int(normal1)
        difficult1=int(difficult1)
        easy=easy1/(easy1+normal1+difficult1)
        normal=normal1/(easy1+normal1+difficult1)
        difficult=difficult1/(easy1+normal1+difficult1)
        print(easy,normal,difficult)
        print(choice_question_num,tf_question_num,filling_question_num,solve_question_num)
        if grade and subject and easy and normal and difficult:
            grade_id = Grade.objects.get(grade=grade).id
            subject_id = Subject.objects.get(subject=subject).id
            if choice_question_num!="undefined":
                choice_question_num = int(choice_question_num)
                choice_question_order_info_easy = Question.objects.filter(types="选择题",difficult=1,subject_id=subject_id,grade_id=grade_id)
                choice_question_order_info_normal = Question.objects.filter(types="选择题", difficult=2,
                                                                          subject_id=subject_id, grade_id=grade_id)
                choice_question_order_info_difficult = Question.objects.filter(types="选择题", difficult=3,
                                                                          subject_id=subject_id, grade_id=grade_id)
                # 利用questionlist_tojsonlist函数将查找到的所有内容转换成json后存进一个list
                choice_question_list_easy = questionlist_tojsonlist(choice_question_order_info_easy)
                choice_question_list_normal = questionlist_tojsonlist(choice_question_order_info_normal)
                choice_question_list_difficult = questionlist_tojsonlist(choice_question_order_info_difficult)
                choice_question_num_easy = int(choice_question_num * easy)
                choice_question_num_normal = int(choice_question_num * normal)
                choice_question_num_difficult = int(choice_question_num * difficult)
                print(len(choice_question_list_easy))
                if len(choice_question_list_easy) >= choice_question_num*easy:
                    choice_question_list_easy = random.sample(choice_question_list_easy, choice_question_num_easy)
                    res_data['choice_q_e'] = '选择题ok'
                    for i in choice_question_list_easy:
                        QuestionList.append(i)
                else:
                    res_data['choice_q_e'] = '题库中没有那么多符合要求的简单选择题'
                if len(choice_question_list_normal) >= choice_question_num*normal:
                    choice_question_list_normal = random.sample(choice_question_list_normal, choice_question_num_normal)
                    res_data['choice_q_n'] = '选择题ok'
                    for i in choice_question_list_normal:
                        QuestionList.append(i)
                else:
                    res_data['choice_q_n'] = '题库中没有那么多符合要求的难度正常选择题'
                if len(choice_question_list_difficult) >= choice_question_num*difficult:
                    choice_question_list_difficult = random.sample(choice_question_list_difficult, choice_question_num_difficult)
                    res_data['choice_q_d'] = '选择题ok'
                    for i in choice_question_list_difficult:
                        QuestionList.append(i)
                else:
                    res_data['choice_q_d'] = '题库中没有那么多符合要求的困难选择题'
            else:
                res_data['choice_q'] = '选择题信息有空值，无选择题'

            if tf_question_num!="undefined":
                tf_question_num = int(tf_question_num)
                tf_question_order_info_easy = Question.objects.filter(types="判断题",difficult=1,subject_id=subject_id,grade_id=grade_id)
                tf_question_order_info_normal = Question.objects.filter(types="判断题", difficult=2,
                                                                          subject_id=subject_id, grade_id=grade_id)
                tf_question_order_info_difficult = Question.objects.filter(types="判断题", difficult=3,
                                                                          subject_id=subject_id, grade_id=grade_id)
                # 利用questionlist_tojsonlist函数将查找到的所有内容转换成json后存进一个list
                tf_question_list_easy = questionlist_tojsonlist(tf_question_order_info_easy)
                tf_question_list_normal = questionlist_tojsonlist(tf_question_order_info_normal)
                tf_question_list_difficult = questionlist_tojsonlist(tf_question_order_info_difficult)
                tf_question_num_easy = int(tf_question_num * easy)
                tf_question_num_normal = int(tf_question_num * normal)
                tf_question_num_difficult = int(tf_question_num * difficult)
                if len(tf_question_list_easy) >= tf_question_num*easy:
                    tf_question_list_easy = random.sample(tf_question_list_easy, tf_question_num_easy)
                    res_data['tf_q_e'] = '判断题ok'
                    for i in tf_question_list_easy:
                        QuestionList.append(i)
                else:
                    res_data['tf_q_e'] = '题库中没有那么多符合要求的简单判断题'
                if len(tf_question_list_normal) >= tf_question_num*normal:
                    tf_question_list_normal = random.sample(tf_question_list_normal, tf_question_num_normal)
                    res_data['tf_q_n'] = '判断题ok'
                    for i in tf_question_list_normal:
                        QuestionList.append(i)
                else:
                    res_data['tf_q_n'] = '题库中没有那么多符合要求的难度正常判断题'
                if len(tf_question_list_difficult) >= tf_question_num*difficult:
                    tf_question_list_difficult = random.sample(tf_question_list_difficult, tf_question_num_difficult)
                    res_data['tf_q_d'] = '判断题ok'
                    for i in tf_question_list_difficult:
                        QuestionList.append(i)
                else:
                    res_data['tf_q_d'] = '题库中没有那么多符合要求的困难判断题'
            else:
                res_data['tf_q'] = '判断题信息有空值，无判断题'

            if solve_question_num!="undefined":
                solve_question_num = int(solve_question_num)
                solve_question_order_info_easy = Question.objects.filter(types="解答题",difficult=1,subject_id=subject_id,grade_id=grade_id)
                solve_question_order_info_normal = Question.objects.filter(types="解答题", difficult=2,
                                                                          subject_id=subject_id, grade_id=grade_id)
                solve_question_order_info_difficult = Question.objects.filter(types="解答题", difficult=3,
                                                                          subject_id=subject_id, grade_id=grade_id)
                # 利用questionlist_tojsonlist函数将查找到的所有内容转换成json后存进一个list
                solve_question_list_easy = questionlist_tojsonlist(solve_question_order_info_easy)
                solve_question_list_normal = questionlist_tojsonlist(solve_question_order_info_normal)
                solve_question_list_difficult = questionlist_tojsonlist(solve_question_order_info_difficult)
                solve_question_num_easy = int(solve_question_num * easy)
                solve_question_num_normal = int(solve_question_num * normal)
                solve_question_num_difficult = int(solve_question_num * difficult)
                if len(solve_question_list_easy) >= solve_question_num*easy:
                    solve_question_list_easy = random.sample(solve_question_list_easy, solve_question_num_easy)
                    res_data['solve_q_e'] = '解答题ok'
                    for i in solve_question_list_easy:
                        QuestionList.append(i)
                else:
                    res_data['solve_q_e'] = '题库中没有那么多符合要求的简单解答题'
                if len(solve_question_list_normal) >= solve_question_num*normal:
                    solve_question_list_normal = random.sample(solve_question_list_normal, solve_question_num_normal)
                    res_data['solve_q_n'] = '解答题ok'
                    for i in solve_question_list_normal:
                        QuestionList.append(i)
                else:
                    res_data['solve_q_n'] = '题库中没有那么多符合要求的难度正常解答题'
                if len(solve_question_list_difficult) >= solve_question_num*difficult:
                    solve_question_list_difficult = random.sample(solve_question_list_difficult, solve_question_num_difficult)
                    res_data['solve_q_d'] = '解答题ok'
                    for i in solve_question_list_difficult:
                        QuestionList.append(i)
                else:
                    res_data['solve_q_d'] = '题库中没有那么多符合要求的困难解答题'
            else:
                res_data['solve_q'] = '解答题信息有空值，无解答题'

            if filling_question_num!="undefined":
                filling_question_num = int(filling_question_num)
                filling_question_order_info_easy = Question.objects.filter(types="填空题",difficult=1,subject_id=subject_id,grade_id=grade_id)
                filling_question_order_info_normal = Question.objects.filter(types="填空题", difficult=2,
                                                                          subject_id=subject_id, grade_id=grade_id)
                filling_question_order_info_difficult = Question.objects.filter(types="填空题", difficult=3,
                                                                          subject_id=subject_id, grade_id=grade_id)
                # 利用questionlist_tojsonlist函数将查找到的所有内容转换成json后存进一个list
                filling_question_list_easy = questionlist_tojsonlist(filling_question_order_info_easy)
                filling_question_list_normal = questionlist_tojsonlist(filling_question_order_info_normal)
                filling_question_list_difficult = questionlist_tojsonlist(filling_question_order_info_difficult)
                filling_question_num_easy = int(filling_question_num * easy)
                filling_question_num_normal = int(filling_question_num * normal)
                filling_question_num_difficult = int(filling_question_num * difficult)
                if len(filling_question_list_easy) >= filling_question_num*easy:
                    filling_question_list_easy = random.sample(filling_question_list_easy, filling_question_num_easy)
                    res_data['filling_q_e'] = '填空题ok'
                    for i in filling_question_list_easy:
                        QuestionList.append(i)
                else:
                    res_data['filling_q_e'] = '题库中没有那么多符合要求的简单填空题'
                if len(filling_question_list_normal) >= filling_question_num*normal:
                    filling_question_list_normal = random.sample(filling_question_list_normal, filling_question_num_normal)
                    res_data['filling_q_n'] = '填空题ok'
                    for i in filling_question_list_normal:
                        QuestionList.append(i)
                else:
                    res_data['filling_q_n'] = '题库中没有那么多符合要求的难度正常填空题'
                if len(filling_question_list_difficult) >= filling_question_num*difficult:
                    filling_question_list_difficult = random.sample(filling_question_list_difficult, filling_question_num_difficult)
                    res_data['filling_q_d'] = '填空题ok'
                    for i in filling_question_list_difficult:
                        QuestionList.append(i)
                else:
                    res_data['filling_q_d'] = '题库中没有那么多符合要求的困难填空题'
            else:
                res_data['filling_q'] = '填空题信息有空值，无填空题'
            res_data['questionlist']=QuestionList
            questionidlist=[]
            for i in QuestionList:
                each={'id':'null','types':'null'}
                each['id']=i['id']
                each['types']=i['types']
                questionidlist.append(each)
            print(questionidlist)
            res_data['questionidlist']=questionidlist
            if len(QuestionList)!=0:
                res_data['isOK']=True
        else:
            res_data['errmsg'] = '年级与科目存在空值'
        print(res_data)
    return JsonResponse(res_data)


# 进入每一个试卷详情页 查看题目、试卷信息 -已测试
@csrf_exempt
def paper_detail(request, paper_id=0):
    res_data = {'isOK': False, 'errmsg': '未知错误', 'paperinfo': 'null', 'question_list': ''}
    if request.method == 'POST':
        print(paper_id)
        p = Paper.objects.filter(id=paper_id)
        if p:
            paperlist = paperlist_tojson(p)
            res_data['paperinfo'] = paperlist[0]
        else:
            res_data['errmsg'] = '当前试卷id为空'
        QuestionList = []
        Paper_detail_info = Paper_detail.objects.filter(paper_id=paper_id)
        if Paper_detail_info:
            for i in Paper_detail_info:
                print(i)
                question_id = i.question_id
                question_point = i.point
                # 这里是filter，用first
                print(Question.objects.filter(id=question_id))
                j = Question.objects.filter(id=question_id).first()
                # print(j.id,j.text)
                # 这里返回的试题list需要分数，不能用那个函数
                QuestionData_each = {'id': 'null', 'text': 'null', 'point': 'null', 'types': 'null','difficult': 'null',
                                     'answer': 'null', 'grade': 'null','number':'null',
                                     'knowledge1': 'null', 'knowledge2': 'null', 'school': 'null',
                                     'school_info': 'null', 'subject': 'null'}
                QuestionData_each['id'] = j.id
                QuestionData_each['number'] = len(Paper_detail.objects.filter(question_id=j.id))
                QuestionData_each['text'] = j.text
                QuestionData_each['point'] = i.point
                QuestionData_each['types'] = j.types
                if j.difficult == 1:
                    QuestionData_each['difficult'] = "简单"
                if j.difficult == 2:
                    QuestionData_each['difficult'] = "一般"
                if j.difficult == 3:
                    QuestionData_each['difficult'] = "困难"
                QuestionData_each['answer'] = j.answer
                QuestionData_each['grade'] = Grade.objects.get(id=j.grade_id).grade
                QuestionData_each['knowledge1'] = Knowledge1.objects.get(id=j.knowledge1_id).knowledge1
                QuestionData_each['knowledge2'] = Knowledge2.objects.get(id=j.knowledge2_id).knowledge2
                QuestionData_each['school'] = School.objects.get(id=j.school_id).school
                QuestionData_each['school_info'] = School.objects.get(id=j.school_id).school_info
                QuestionData_each['subject'] = Subject.objects.get(id=j.subject_id).subject
                QuestionList.append(QuestionData_each)
            res_data['question_list'] = QuestionList
            res_data['isOK'] = True
        else:
            res_data['isOK'] = True
            res_data['errmsg'] = '当前试卷没有试题'
    return JsonResponse(res_data)

# 在试卷详情页中添加问题
def paper_detail_addquestion(request,paper_id=0):
    res_data = {'isOK': False, 'errmsg': '未知错误', 'paperinfo': 'null','knowledge1':'null'}
    if request.method=='POST':
        p = Paper.objects.filter(id=paper_id)
        if p:
            paperlist = paperlist_tojson(p)
            res_data['paperinfo'] = paperlist[0]
            subject=paperlist[0]['subject']
            subject_id=Subject.objects.get(subject=subject).id
            k12 = []
            knowledge1list = Knowledge1.objects.filter(subject_id=subject_id)
            for knowledge1 in knowledge1list:
                knowledge1_json = {'value': 'null', 'label': 'null', 'children': 'null'}
                knowledge1_children = []
                knowledge1_json['value'] = knowledge1.knowledge1
                knowledge1_json['label'] = knowledge1.knowledge1
                knowledge1_id = Knowledge1.objects.get(knowledge1=knowledge1).id
                knowledge2list = Knowledge2.objects.filter(knowledge1_id=knowledge1_id)
                for knowledge2 in knowledge2list:
                    knowledge2_json = {'value': 'null', 'label': 'null'}
                    knowledge2_json['value'] = knowledge2.knowledge2
                    knowledge2_json['label'] = knowledge2.knowledge2
                    knowledge1_children.append(knowledge2_json)
                knowledge1_json['children'] = knowledge1_children
                k12.append(knowledge1_json)
            res_data['knowledge1'] = k12
            res_data['isOK']=True
        else:
            res_data['errmsg'] = '当前试卷id为空'
    return JsonResponse(res_data)

# 用到了
# 点击题库列表页面上修改按钮-进入问题详情页，看到具体信息- 已测试
@csrf_exempt
def question_detail(request, question_id):
    res_data = {'isOK': False, 'errmsg': '未知错误', 'question_info': 'null'}
    if request.method == 'POST':
        q = Question.objects.filter(id=question_id)
        if q:
            q_list = questionlist_tojsonlist(q)
            res_data['isOK'] = True
            res_data['question_info'] = q_list[0]
        else:
            res_data['errmsg'] = '该id为空'
    return JsonResponse(res_data)


# 没用到
# 修改问题 进入每一个问题的详情页 -点击问题详情页确认修改的提交按钮 -未测试
@csrf_exempt
def alter_question(request, question_id=0):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        # q=Question.objects.filter(id=question_id).first().id
        text = request.POST.get('text')
        types = request.POST.get('types')
        difficult = request.POST.get('difficult')
        answer = request.POST.get('answer')
        user = request.POST.get('user')
        grade = request.POST.get('grade')
        knowledge1 = request.POST.get('knowledge1')
        knowledge2 = request.POST.get('knowledge2')
        school = request.POST.get('school')
        school_info = request.POST.get('school_info')  # 新增学校需提交新增学校信息
        subject = request.POST.get('subject')
        if text and types and difficult and answer and user and grade and knowledge1 and knowledge2 and school and subject:
            grade_id = Grade.objects.get(grade=grade).id
            # 判断表中是否已经有当前的school
            school_obj = Subject.objects.filter(school=school)
            if school_obj.exists():
                pass
            else:
                print("新增学校", school, school_info)
                School.objects.create(school=school, school_info=school_info).save()
            school_id = Subject.objects.get(school=school).id

            # 判断表中是否已经有当前的subject
            subject_obj = Subject.objects.filter(subject=subject)
            if subject_obj.exists():
                pass
            else:
                print("新增科目", subject)
                Subject.objects.create(subject=subject).save()
            subject_id = Subject.objects.get(subject=subject).id

            # 判断表中是否已经有当前的knowledge1
            knowledge1_obj = Knowledge1.objects.filter(knowledge1=knowledge1)
            if knowledge1_obj.exists():
                pass
            else:
                print("新增一级知识点", knowledge1, subject)
                Knowledge1.objects.create(knowledge1=knowledge1, subject_id=subject_id).save()
            knowledge1_id = Knowledge1.objects.get(knowledge1=knowledge1).id

            # 判断表中是否已经有当前的knowledge2
            knowledge2_obj = Knowledge2.objects.filter(knowledge2=knowledge2)
            if knowledge2_obj.exists():
                pass
            else:
                print("新增一级知识点", knowledge2, knowledge1)
                Knowledge2.objects.create(knowledge2=knowledge2, knowledge1_id=knowledge1_id).save()
            knowledge2_id = Knowledge2.objects.get(knowledge2=knowledge2).id
            Question.objects.filter(id=question_id).update(text=text, types=types, difficult=difficult,
                                                           answer=answer, user=user, grade_id=grade_id,
                                                           knowledge1_id=knowledge1_id,
                                                           knowledge2_id=knowledge2_id, school_id=school_id,
                                                           subject_id=subject_id)
            res_data['isOK'] = True
        else:
            print("不可为空值")
            res_data['errmsg'] = '存在空值'
    return JsonResponse(res_data)


# 删除问题 -已测试
@csrf_exempt
def delete_question(request, question_id=0):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        question_obj = Question.objects.filter(id=question_id)
        if question_obj.exists():
            question_obj.delete()
            res_data['isOK'] = True
        else:
            res_data['errmsg'] = '所选题目为空'
    return JsonResponse(res_data)

# 没用到
# 传来的formdata格式为 name points user school grade subject
# 试卷题头的修改 -已测试
@csrf_exempt
def alter_paper(request, paper_id=0):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        name = request.POST.get('name')
        points = request.POST.get('points')
        user = request.POST.get('user')
        # 三个外键
        school = request.POST.get('school')
        grade = request.POST.get('grade')
        subject = request.POST.get('subject')
        if name and points and school and grade and subject:
            school_id = School.objects.get(school=school).id
            grade_id = Grade.objects.get(grade=grade).id
            subject_id = Subject.objects.get(subject=subject).id
            Paper.objects.filter(id=paper_id).update(name=name, points=points, grade_id=grade_id, school_id=school_id,
                                                     user=user, subject_id=subject_id)
            res_data['isOK'] = True
        else:
            res_data['errmsg'] = '存在空值'
    return JsonResponse(res_data)

# 没用到
# 传来的格式为formdata paper_id=x，point=x
# 再点击进入试卷详情页时，每一个试题可以修改分数，点击每个试题旁的修改按钮即可-已测试
@csrf_exempt
def alter_point(request, question_id):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        paper_id = request.POST.get('paper_id')
        point = request.POST.get('point')
        if paper_id and point:
            pd = Paper_detail.objects.filter(paper=paper_id, question=question_id)
            if pd:
                pd.update(point=point)
                res_data['isOK'] = True
        else:
            res_data['errmsg'] = '存在空值'
    return JsonResponse(res_data)

# 用到
# 试卷内题目的删除 单选 -已测试
@csrf_exempt
def delete_paperdetail(request,question_id=0):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        paper_id = request.POST.get('paper_id')
        pd = Paper_detail.objects.filter(paper=paper_id)
        if pd:
            pdi = Paper_detail.objects.filter(paper=paper_id, question=question_id)
            if pdi:
                pdi.delete()
            else:
                res_data['errmsg'] = '某题不存在'
            res_data['isOK'] = True
        else:
            res_data['errmsg'] = '该试卷为空'
    return JsonResponse(res_data)


# 没用到 - 直接删除试卷 -已测试
@csrf_exempt
def delete_paper(request, paper_id=0):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        paper_obj = Paper.objects.filter(id=paper_id)
        if paper_obj.exists():
            Paper_detail.objects.filter(paper=paper_id).delete()
            paper_obj.delete()
            res_data['isOK'] = True
        else:
            res_data['errmsg'] = '所选试卷为空'
    return JsonResponse(res_data)

#用到了 录入试题 文本编辑器
@csrf_exempt
def uploadImg(request):  # 图片上传函数
    res_data = {'isOK': False, 'errmsg': '未知错误', 'image': 'null'}
    if request.method == 'POST':
        img = Img(img_url=request.FILES.get('file'))
        img.save()
        res_data['image'] = str(img.img_url)
        res_data['isOK'] = True
        print(res_data)
    return JsonResponse(res_data)

# 用到了-手动组卷 试卷添加题目
@csrf_exempt
def add_question(request,question_id=0):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method=='POST':
        paper_id=request.POST.get('paperid')
        point = request.POST.get('point')
        if paper_id and point:
            a = Paper_detail.objects.filter(paper_id=paper_id)
            questionid = []
            for i in a:
                questionid.append(i.question_id)
            print(questionid)
            if question_id in questionid:
                res_data['errmsg'] = '题库中有重复题目'
            else:
                Paper_detail.objects.create(paper_id=paper_id, question_id=question_id, point=point).save()
                res_data['isOK'] = True
        else:
            res_data['errmsg'] = '有分数未输入'
    return JsonResponse(res_data)

# 下载试卷 生成答案
@csrf_exempt
def downloadpaper(request,paper_id=0):
    res_data = {'isOK': False, 'errmsg': '未知错误','url':'','url1':''}
    if request.method=='POST':
        paper_obj=Paper.objects.get(id=paper_id)
        if paper_obj:
            p_name=paper_obj.name
            p_points=paper_obj.points
            p_subject=Subject.objects.get(id=paper_obj.subject_id).subject
            p_school=School.objects.get(id=paper_obj.school_id).school
            p_grade=Grade.objects.get(id=paper_obj.grade_id).grade
            pd_obj=Paper_detail.objects.filter(paper_id=paper_id)
            if pd_obj.exists():
                question_id_list=[]
                for i in pd_obj:
                    question_id_list.append(i.question_id)
                print(question_id_list)
                choice_question_list = []
                filling_question_list=[]
                solve_question_list=[]
                tf_question_list=[]
                choice_point_list = []
                filling_point_list = []
                solve_point_list = []
                tf_point_list = []
                choice_answer_list = []
                filling_answer_list = []
                solve_answer_list = []
                tf_answer_list = []
                for i in question_id_list:
                    q=Question.objects.get(id=i)
                    point=Paper_detail.objects.get(paper_id=paper_id,question_id=i).point
                    if q.types=="选择题":
                        choice_question_list.append(q.text)
                        choice_point_list.append(point)
                        choice_answer_list.append(q.answer)
                    if q.types=="判断题":
                        tf_question_list.append(q.text)
                        tf_point_list.append(point)
                        tf_answer_list.append(q.answer)
                    if q.types=="解答题":
                        solve_question_list.append(q.text)
                        solve_point_list.append(point)
                        solve_answer_list.append(q.answer)
                    if q.types=="填空题":
                        filling_question_list.append(q.text)
                        filling_point_list.append(point)
                        filling_answer_list.append(q.answer)
                print(len(choice_question_list),len(filling_question_list),len(solve_question_list),len(tf_question_list))
                tag=["、选择题：","、判断题：","、填空题：","、解答题："]
                Questionall=[choice_question_list,tf_question_list,filling_question_list,solve_question_list]
                Pointall=[choice_point_list,tf_point_list,filling_point_list,solve_point_list]
                Answerall = [choice_answer_list, tf_answer_list, filling_answer_list, solve_answer_list]
                title="<h1>"+p_name+"</h1>"
                p_info="<p>年级："+p_grade+"&nbsp; &nbsp; &nbsp; 科目："+p_subject+"&nbsp; &nbsp; &nbsp; 学校："+p_school+"&nbsp; &nbsp; &nbsp; 总分："+str(p_points)+"</p><hr>"
                html=title+p_info
                html1="<h1>"+p_name+"答案"+"</h1>"+p_info
                tag1=1
                tag2=1
                tag2_dict={'1':'一','2':'二','3':'三','4':'四'}
                for i in range(len(Questionall)):
                    if len(Questionall[i])==0:
                        pass
                    else:
                        a="<h3>"+tag2_dict[str(tag2)]+tag[i]+"</h3>"
                        answer="<h3>"+tag2_dict[str(tag2)]+tag[i]+"</h3>"
                        for j in range(len(Questionall[i])):
                            length=len(Questionall[i][j])
                            b=Questionall[i][j][3:length]
                            d = Answerall[i][j][3:length]
                            c="<p>("+str(Pointall[i][j])+"分)"+str(tag1)+"."
                            a=a+c+b
                            answer=answer+c+d
                            tag1=tag1+1
                        tag2=tag2+1
                        html1=html1+answer
                        html=html+a
                path1 = os.getcwd()
                oldpath=path1
                path2 = path1 + "\\test_library\\static\\test_library"
                os.chdir(path2)
                GEN_HTML = p_name+".html"  # 命名生成的html
                GEN_DOCX= p_name+".docx"
                GEN_HTML1 = p_name + "_answer.html"  # 命名生成的html
                GEN_DOCX1= p_name + "_answer.docx"
                f = codecs.open(GEN_HTML,'w','utf-8')
                f.write(html)
                f.close()
                f1 = codecs.open(GEN_HTML1, 'w', 'utf-8')
                f1.write(html1)
                f1.close()
                pypandoc.convert_file(GEN_HTML, 'docx', format='html', encoding='GBK', outputfile=GEN_DOCX)
                pypandoc.convert_file(GEN_HTML1, 'docx', format='html', encoding='GBK', outputfile=GEN_DOCX1)
                res_data['isOK']=True
                res_data['url']="http://127.0.0.1:8000/static/test_library/"+GEN_DOCX
                res_data['url1']="http://127.0.0.1:8000/static/test_library/"+GEN_DOCX1
                os.chdir(oldpath)
            else:
                res_data['errmsg'] = '该试卷无试题'
        else:
            res_data['errmsg']='该试卷为空'
    return JsonResponse(res_data)

