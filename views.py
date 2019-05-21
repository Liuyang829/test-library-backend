from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from .models import Grade, Subject, User, Question, Paper, Paper_detail, Knowledge1, Knowledge2, School
import random
import json


def index(request):
    return HttpResponse("Hello, world. You're at the test_library index.")

@csrf_exempt
def login(request):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
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
        PaperData_each = {'id': 'null', 'name': 'null', 'subject': 'null', 'grade': 'null', 'school': 'null'}
        PaperData_each['id'] = i.id
        PaperData_each['name'] = i.name
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
        QuestionData_each = {'id': 'null', 'text': 'null', 'types': 'null', 'option1': 'null', 'option2': 'null',
                             'option3': 'null', 'option4': 'null', 'difficult': 'null', 'answer': 'null',
                             'photo': 'null', 'formula': 'null', 'grade': 'null', 'knowledge1': 'null',
                             'knowledge2': 'null', 'school': 'null', 'school_info': 'null', 'subject': 'null'}
        QuestionData_each['id'] = i.id
        QuestionData_each['text'] = i.text
        QuestionData_each['types'] = i.types
        QuestionData_each['option1'] = i.option1
        QuestionData_each['option2'] = i.option2
        QuestionData_each['option3'] = i.option3
        QuestionData_each['option4'] = i.option4
        QuestionData_each['difficult'] = i.difficult
        QuestionData_each['answer'] = i.answer
        QuestionData_each['photo'] = i.photo
        QuestionData_each['formula'] = i.formula
        QuestionData_each['grade'] = Grade.objects.get(id=i.grade_id).grade
        QuestionData_each['knowledge1'] = Knowledge1.objects.get(id=i.knowledge1_id).knowledge1
        QuestionData_each['knowledge2'] = Knowledge2.objects.get(id=i.knowledge2_id).knowledge2
        QuestionData_each['school'] = School.objects.get(id=i.school_id).school
        QuestionData_each['school_info'] = School.objects.get(id=i.school_id).school_info
        QuestionData_each['subject'] = Subject.objects.get(id=i.school_id).subject
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
def add_subject(request):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method=='POST':
        subject = request.POST.get('subject')
        knowledge1 = request.POST.get('konwledge1')
        knowledge2 = request.POST.get('knowledge2')
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
            res_data['isOK']=True
        else:
            res_data['errmsg']='存在空值'
    return JsonResponse(res_data)



# 录入试题存入数据库 - 未测试
@csrf_exempt
def enter_questions(request):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        text = request.POST.get('text')
        types = request.POST.get('types')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        difficult = request.POST.get('difficult')
        answer = request.POST.get('answer')
        photo = request.POST.get('photo')
        formula = request.POST.get('formula')
        user = request.POST.get('user')
        grade = request.POST.get('grade')
        knowledge1 = request.POST.get('konwledge1')
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
                print("新增二级知识点", knowledge2, knowledge1)
                Knowledge2.objects.create(knowledge2=knowledge2, knowledge1_id=knowledge1_id).save()
            knowledge2_id = Knowledge1.objects.get(knowledge2=knowledge2).id

            if text == '选择题':
                if option1 and option2 and option3 and option4:
                    Question.objects.create(text=text, types=types, option1=option1, option2=option2, option3=option3,
                                            option4=option4, difficult=difficult, answer=answer, photo=photo,
                                            formula=formula, user=user, grade_id=grade_id, knowledge1_id=knowledge1_id,
                                            knowledge2_id=knowledge2_id, school_id=school_id,
                                            subject_id=subject_id).save()
                    res_data['isOK'] = True
                else:
                    print("选择题选项不可为空")
                    res_data['errmsg'] = '选择题选项不可为空'
            else:
                Question.objects.create(text=text, types=types, difficult=difficult, answer=answer, photo=photo,
                                        formula=formula, user=user, grade_id=grade_id, knowledge1_id=knowledge1_id,
                                        knowledge2_id=knowledge2_id, school_id=school_id, subject_id=subject_id).save()
                res_data['isOK'] = True
        else:
            print("不可为空值")
            res_data['errmsg'] = '存在空值'
    return JsonResponse(res_data)


# 为前端级联选择器构造学科-一级知识点-二级知识点的数据格式
@csrf_exempt
def cascader():
    cascaderlist = []
    subjectlist = Subject.objects.all()
    for subject in subjectlist:
        subject_json = {'value': 'null', 'label': 'null', 'children': 'null'}
        subject_children = []
        print(subject)
        subject_json['value'] = subject.subject
        subject_json['label'] = subject.subject
        subject_id = Subject.objects.get(subject=subject).id
        knowledge1list = Knowledge1.objects.filter(subject_id=subject_id)
        print(knowledge1list)
        for knowledge1 in knowledge1list:
            knowledge1_json = {'value': 'null', 'label': 'null', 'children': 'null'}
            knowledge1_children = []
            knowledge1_json['value'] = knowledge1.knowledge1
            knowledge1_json['label'] = knowledge1.knowledge1
            knowledge1_id = Knowledge1.objects.get(knowledge1=knowledge1).id
            knowledge2list = Knowledge2.objects.filter(knowledge1_id=knowledge1_id)
            print(knowledge2list)
            for knowledge2 in knowledge2list:
                knowledge2_json = {'value': 'null', 'label': 'null'}
                knowledge2_json['value'] = knowledge2.knowledge2
                knowledge2_json['label'] = knowledge2.knowledge2
                knowledge1_children.append(knowledge2_json)
            knowledge1_json['children'] = knowledge1_children
            subject_children.append(knowledge1_json)
        print(subject_children)
        subject_json['children'] = subject_children
        cascaderlist.append(subject_json)
        print(cascaderlist)
    return cascaderlist


# 进入录入试题页面-获得所有的下拉列表信息-已测试
@csrf_exempt
def get_enterquestionpage(request):
    if request.method == 'POST':
        res_data = {'isOK': False, 'grade': 'null', 'school': 'null', 'subjectall': 'null'}
        gradelist = []
        schoollist = []

        GradeData = Grade.objects.all()
        SchoolData = School.objects.all()

        for i in GradeData:
            gradelist.append(i.grade)
        for i in SchoolData:
            schoollist.append(i.school)
        res_data['isOK'] = True
        res_data['grade'] = gradelist
        res_data['school'] = schoollist
        res_data['subjectall'] = cascader()
    return JsonResponse(res_data)


# 手动 自动组卷用 -已测试
# 输入试卷名称 学校等信息 存入试卷表中，也就是试卷的title
# 前端数据格式为 {'name':'xxx','points':'xxx','user':'xxx','school':'xxx','grade':'xxx','subject':'xxx'}
@csrf_exempt
def postpaperinfo(request):
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
            Paper.objects.create(name=name, points=points, grade_id=grade_id, school_id=school_id, user=user,
                                 subject_id=subject_id).save()
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
        knowledge1 = request.POST.get('knowledge1')
        knowledge2 = request.POST.get('knowledge2')
        difficult = request.POST.get('difficult')
        types = request.POST.get('types')
        search_dict = dict()
        search_dict['types'] = types
        search_dict['difficult'] = difficult
        if grade and subject and difficult and types and knowledge1:
            grade_id = Grade.objects.get(grade=grade).id
            subject_id = Subject.objects.get(subject=subject).id
            knowledge1_id = Knowledge1.objects.get(knowledge1=knowledge1).id
            search_dict['grade_id'] = grade_id
            search_dict['subject_id'] = subject_id
            search_dict['knowledge1_id'] = knowledge1_id
            if knowledge2:
                knowledge2_id = Knowledge2.objects.get(knowledge2=knowledge2).id
                search_dict['knowledge2_id'] = knowledge2_id
            question_order_info = Question.objects.filter(**search_dict)
            question_info = questionlist_tojsonlist(question_order_info)
            # 应该是只打印出了题目
            print(question_info)
            res_data['isOK'] = True
            res_data['questionlist'] = question_info
        else:
            res_data['errmsg'] = '存在空值'
    return JsonResponse(res_data)

# 手动、自动通用
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
# 还要做查重-未做
@csrf_exempt
def loadpaper(request):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        print(request.body)
        print(request.body.decode())

        a = request.body.decode()
        b = json.loads(a)
        # print(a['paper'])
        # print(a['question_info'])
        # receive_data = json.loads(request.body.decode())
        # print(receive_data)
        paper = b['paper']
        question_info_list = b['question_info']
        # print(type(question_info_list))
        # print(paper, question_info_list)
        if paper and question_info_list:
            paper_id = Paper.objects.get(name=paper).id
            if paper_id:
                print(paper_id)
                for i in question_info_list:
                    if i['id'] and i['point']:

                        question_id = i['id']
                        point = i['point']
                        Paper_detail.objects.create(paper_id=paper_id, question_id=question_id, point=point).save()
                        res_data['isOK'] = True
                    else:
                        res_data['errmsg'] = '有分数未输入'
            else:
                res_data['errmsg'] = '该试卷名为空'
    return JsonResponse(res_data)


# 未测试 根据所给科目 年级 难度系数 选择题数量 填空题数量 判断题数量 解答题数量 返回题目列表
@csrf_exempt
def getautopaper(request):
    res_data = {'isOK': False, 'errmsg': '未知错误', 'questionlist': 'null', 'choice_q': 'null', 'filling_q': 'null',
                'solve_q': 'null', 'tf_q': 'null'}
    QuestionList = []
    if request.method == 'POST':
        grade = request.POST.get('grade')
        subject = request.POST.get('subject')
        choice_question_num = request.POST.get('choice_qusetion_num')
        choice_question_difficult = request.POST.get('choice_question_difficult')
        tf_question_num = request.POST.get('tf_qusetion_num')
        tf_question_difficult = request.POST.get('tf_question_difficult')
        filling_question_num = request.POST.get('filling_qusetion_num')
        filling_question_difficult = request.POST.get('filling_qusetion_difficult')
        solve_question_num = request.POST.get('solve_qusetion_num')
        solve_question_difficult = request.POST.get('solve_qusetion_difficult')
        search_dict_choice = dict()
        search_dict_tf = dict()
        search_dict_filling = dict()
        search_dict_solve = dict()
        if grade and subject:
            grade_id = Grade.objects.get(grade=grade).id
            subject_id = Subject.objects.get(subject=subject).id
            search_dict_choice['grade_id'] = grade_id
            search_dict_choice['subject_id'] = subject_id
            search_dict_tf['grade_id'] = grade_id
            search_dict_tf['subject_id'] = subject_id
            search_dict_filling['grade_id'] = grade_id
            search_dict_filling['subject_id'] = subject_id
            search_dict_solve['grade_id'] = grade_id
            search_dict_solve['subject_id'] = subject_id
            if choice_question_difficult and choice_question_num:
                search_dict_choice['difficult'] = choice_question_difficult
                choice_question_order_info = Question.objects.filter(**search_dict_choice)
                # 利用questionlist_tojsonlist函数将查找到的所有内容转换成json后存进一个list
                choice_question_list = questionlist_tojsonlist(choice_question_order_info)
                if len(choice_question_list) >= choice_question_num:
                    choice_question_list = random.sample(choice_question_list, choice_question_num)
                    res_data['choice_q'] = '选择题ok'
                else:
                    res_data['choice_q'] = '题库中没有那么多符合要求的选择题'
                QuestionList.append(choice_question_list)
            else:
                res_data['choice_q'] = '选择题信息有空值，无选择题'

            if tf_question_difficult and tf_question_num:
                search_dict_tf['difficult'] = tf_question_difficult
                tf_question_order_info = Question.objects.filter(**search_dict_tf)
                tf_question_list = questionlist_tojsonlist(tf_question_order_info)
                if len(tf_question_list) >= tf_question_num:
                    tf_question_list = random.sample(tf_question_list, tf_question_num)
                    res_data['tf_q'] = '判断题ok'
                else:
                    res_data['tf_q'] = '题库中没有那么多符合要求的判断题'
                QuestionList.append(tf_question_list)
            else:
                res_data['tf_q'] = '判断题信息有空值，无判断题'

            if filling_question_difficult and filling_question_num:
                search_dict_filling['difficult'] = filling_question_difficult
                filling_question_order_info = Question.objects.filter(**search_dict_filling)
                filling_question_list = questionlist_tojsonlist(filling_question_order_info)
                if len(filling_question_list) >= filling_question_num:
                    filling_question_list = random.sample(filling_question_list, filling_question_num)
                    res_data['filling_q'] = '判断题ok'
                else:
                    res_data['filling_q'] = '题库中没有那么多符合要求的判断题'
                QuestionList.append(filling_question_list)
            else:
                res_data['filling_q'] = '填空题信息有空值，无填空题'

            if solve_question_difficult and solve_question_num:
                search_dict_solve['difficult'] = solve_question_difficult
                solve_question_order_info = Question.objects.filter(**search_dict_solve)
                solve_question_list = questionlist_tojsonlist(solve_question_order_info)
                if len(solve_question_list) >= solve_question_num:
                    solve_question_list = random.sample(solve_question_list, solve_question_num)
                    res_data['solve_q'] = '判断题ok'
                else:
                    res_data['solve_q'] = '题库中没有那么多符合要求的判断题'
                QuestionList.append(solve_question_list)
            else:
                res_data['solve_q'] = '解答题信息有空值,无解答题'
            res_data['isOK'] = True
        else:
            res_data['errmsg'] = '年级与科目存在空值'
    return JsonResponse(res_data)


# 进入每一个试卷详情页 查看题目、试卷信息 -已测试
@csrf_exempt
def paper_detail(request, paper_id=0):
    res_data = {'isOK': False, 'errmsg': '未知错误', 'paperinfo': 'null', 'question_list': 'null'}
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
                QuestionData_each = {'id': 'null', 'text': 'null', 'point': 'null', 'types': 'null', 'option1': 'null',
                                     'option2': 'null', 'option3': 'null', 'option4': 'null', 'difficult': 'null',
                                     'answer': 'null', 'photo': 'null', 'formula': 'null', 'grade': 'null',
                                     'knowledge1': 'null', 'knowledge2': 'null', 'school': 'null',
                                     'school_info': 'null', 'subject': 'null'}
                QuestionData_each['id'] = j.id
                QuestionData_each['text'] = j.text
                QuestionData_each['point'] = i.point
                QuestionData_each['types'] = j.types
                QuestionData_each['option1'] = j.option1
                QuestionData_each['option2'] = j.option2
                QuestionData_each['option3'] = j.option3
                QuestionData_each['option4'] = j.option4
                QuestionData_each['difficult'] = j.difficult
                QuestionData_each['answer'] = j.answer
                QuestionData_each['photo'] = j.photo
                QuestionData_each['formula'] = j.formula
                QuestionData_each['grade'] = Grade.objects.get(id=j.grade_id).grade
                QuestionData_each['knowledge1'] = Knowledge1.objects.get(id=j.knowledge1_id).knowledge1
                QuestionData_each['knowledge2'] = Knowledge2.objects.get(id=j.knowledge2_id).knowledge2
                QuestionData_each['school'] = School.objects.get(id=j.school_id).school
                QuestionData_each['school_info'] = School.objects.get(id=j.school_id).school_info
                QuestionData_each['subject'] = Subject.objects.get(id=j.school_id).subject
                QuestionList.append(QuestionData_each)
            res_data['question_list'] = QuestionList
            res_data['isOK'] = True
        else:
            res_data['errmsg'] = '无该试卷或当前试卷没有试题'
    return JsonResponse(res_data)


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


# 修改问题 进入每一个问题的详情页 -点击问题详情页确认修改的提交按钮 -未测试
@csrf_exempt
def alter_question(request, question_id=0):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        # q=Question.objects.filter(id=question_id).first().id
        text = request.POST.get('text')
        types = request.POST.get('types')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        difficult = request.POST.get('difficult')
        answer = request.POST.get('answer')
        photo = request.POST.get('photo')
        formula = request.POST.get('formula')
        user = request.POST.get('user')
        grade = request.POST.get('grade')
        knowledge1 = request.POST.get('konwledge1')
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
            knowledge2_id = Knowledge1.objects.get(knowledge2=knowledge2).id

            if text == '选择题':
                if option1 and option2 and option3 and option4:
                    Question.objects.filter(id=question_id).update(text=text, types=types, option1=option1,
                                                                   option2=option2, option3=option3,
                                                                   option4=option4, difficult=difficult, answer=answer,
                                                                   photo=photo, formula=formula, user=user,
                                                                   grade_id=grade_id,
                                                                   knowledge1_id=knowledge1_id,
                                                                   knowledge2_id=knowledge2_id, school_id=school_id,
                                                                   subject_id=subject_id)
                    res_data['isOK'] = True
                else:
                    print("选择题选项不可为空")
                    res_data['errmsg'] = '选择题选项不可为空'
            else:
                Question.objects.filter(id=question_id).update(text=text, types=types, difficult=difficult,
                                                               answer=answer, photo=photo,
                                                               formula=formula, user=user, grade_id=grade_id,
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


# 传来的格式为{’paper_id‘：’xx‘,questionlist:[1，2,3...]}
# 试卷内题目的删除 多选 -已测试
@csrf_exempt
def delete_paperdetail(request):
    res_data = {'isOK': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        a = request.body.decode()
        b = json.loads(a)
        paper_id = b['paper_id']
        questionlist = b['questionlist']
        pd = Paper_detail.objects.filter(paper=paper_id)
        if pd:
            for i in questionlist:
                pdi = Paper_detail.objects.filter(paper=paper_id, question=i)
                if pdi:
                    pdi.delete()
                else:
                    res_data['errmsg'] = '某题不存在'
            res_data['isOK'] = True
        else:
            res_data['errmsg'] = '该试卷为空'
    return JsonResponse(res_data)


# 直接删除试卷 -已测试
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


# 下载试卷 生成答案
@csrf_exempt
def downloadpaper(request):
    pass
