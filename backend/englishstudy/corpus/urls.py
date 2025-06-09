# *_* coding: utf-8 *_* 
# @Time: 2025/6/7 17:39
# @Author: JessicaSun
# @File: urls
# @Project: backend
from django.urls import path
from .views import ChapterFullListView

urlpatterns = [
    path('ApicorpusFly/fullList', ChapterFullListView.as_view()),
]