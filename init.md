# [架构](https://www.notion.so/English-study-web-208e5524c9d680f29f76e726ee2172db)
# 一、 后端Django + MySQL 框架搭建
## 1. 创建Django项目
```
# 新建虚拟环境并激活
python3 -m venv venv
source venv/bin/activate

# 安装 Django、MySQL 驱动、DRF
pip install django djangorestframework mysqlclient djangorestframework-simplejwt corsheaders

# 创建项目和应用
django-admin startproject englishstudy
cd englishstudy
python manage.py startapp users
python manage.py startapp corpus
python manage.py startapp dictation

```

## 2. 配置 MySQL 数据库
在 englishstudy/settings.py 中修改数据库配置：

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'english_study_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```


## 3. 注册 App 和中间件
在 INSTALLED_APPS 添加：
```
INSTALLED_APPS = [
    # ... 其他
    'rest_framework',
    'corsheaders',
    'users',
    'corpus',
    'dictation',
]
```

在 MIDDLEWARE 顶部添加：
```
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ... 其他
]
```

允许前端跨域（开发阶段）：
```
CORS_ALLOW_ALL_ORIGINS = True
```

## 4. 配置 JWT 认证
在 settings.py 添加：
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

## 5. 迁移数据库

```
python manage.py makemigrations
python manage.py migrate
```

# 二、前端 Vue3 框架搭建
## 1. 创建 Vue3 项目

```
# 在 english-study 目录下
npm init vue@latest frontend
cd frontend
npm install
```
