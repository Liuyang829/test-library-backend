"# test-library-backend" 
将该项目放置django环境文件夹下，修改以下配置文件

为支持跨域访问
pip install django-cors-headers


在settings.py文件中修改

在INSTALLED_APPS添加'test_library.apps.TestLibraryConfig'

在MIDDLEWARE中
注释＃ 'django.middleware.csrf.CsrfViewMiddleware'
添加'django.contrib.sessions.middleware.SessionMiddleware'，

在DATABASES = {
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

在urls.py文件中修改
path('test_library/', include('test_library.urls')),

在django项目文件夹下命令行中运行

python manage.py makemigrations

python manage.py migrate

生成数据库

配置上传图片操作：

首先需 pip install Pillow

在django环境下的settings中配置
添加

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/') # media即为图片上传的根路径
MEDIA_URL = '/media/'

在django环境下urls中配置

from testdjango(django环境文件夹名) import settings
在最后 加上代码
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

在django环境同级文件夹目录下新建文件夹 media 在里面新建文件夹 img 用来保存图片，上传的图片即保存至该目录下