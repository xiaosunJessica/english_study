# *_* coding: utf-8 *_* 
# @Time: 2025/6/7 17:39
# @Author: JessicaSun
# @File: urls
# @Project: backend
from django.urls import path
from .views import CorpusFullListView, CorpusFullItemView, SetErrorWordsView

urlpatterns = [
    path('ApicorpusFly/fullList', CorpusFullListView.as_view()),
    path('ApicorpusFly/fullItem', CorpusFullItemView.as_view()),
    path('ApicorpusFly/setErrorWord', SetErrorWordsView.as_view())
]