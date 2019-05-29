"test-library-backend" 
========

将该项目放置django环境文件夹下，修改以下配置文件

为支持跨域访问需
```
pip install django-cors-headers
```
settings.py文件中修改
--------
在INSTALLED_APPS添加
```
'test_library.apps.TestLibraryConfig'
```
在MIDDLEWARE中注释
```
＃ 'django.middleware.csrf.CsrfViewMiddleware'
```
在MIDDLEWARE中添加
```
'django.contrib.sessions.middleware.SessionMiddleware'，
```
修改数据库配置及系统设置
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER':'',
        'PASSWORD':'',
        'HOST':'',
        'PORT':'3306'
    }
}

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
```

在urls.py文件中修改
--------
```
path('test_library/', include('test_library.urls')),
```
在django项目文件夹下命令行中运行以生成数据库
```
python manage.py makemigrations
python manage.py migrate
```

配置上传图片操作：
-----
首先需安装图片处理的库
```
pip install Pillow
```
在django环境下的settings中配置添加
```
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/') # media即为图片上传的根路径
MEDIA_URL = '/media/'
```
在django环境下urls中配置
```
from testdjango(django环境文件夹名) import settings
```
在urlpatterns[]外最后加上代码
```
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
在django环境同级文件夹目录下新建文件夹 media 在里面新建文件夹 img 用来保存图片，上传的图片即保存至该目录下

配置下载试卷docx操作
-----
首先需安装pypandoc，进行转化<br>
下载传送门：https://github.com/jgm/pandoc/releases/tag/1.19.2.1
windows下直接下载.msi文件即可
```
pip install pypandoc
```
在django环境settings.py下配置，添加如下代码
```
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'test_library/static')  # 这个是和服务器软件链接的时候收集静态文件
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",  # 在系统文件路径查找
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",  # 在Apps的路径下查找
)  # 这是查找的方法
```
在本app文件夹下建立文件夹static，在路径下建立app名的文件夹，即可通过服务器访问该路径文件
例如：
http://127.0.0.1:8000/static/test_library/1.doc
