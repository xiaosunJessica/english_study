# *_* coding: utf-8 *_* 
# @Time: 2025/6/7 17:41
# @Author: JessicaSun
# @File: serializers
# @Project: backend
from rest_framework import serializers
from .models import Book, Unit, Lesson,  Word

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            'id', 'text', 'note', 'voice', 'url', 'local_url',
            'word_id', 'error_num', 'lesson_id'
        ]

class LessonSerializer(serializers.ModelSerializer):
    words = WordSerializer(many=True, read_only=True)
    class Meta:
        model = Lesson
        fields = [
            'id', 'text', 'count', 'unit_id', 'product_type', 'url',
            'check_url', 'unit_id', 'is_selected', 'words'
        ]

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id','name', 'is_checked', 'extra', 'url', 'word_count', 'book_id']

class BookSerializer(serializers.ModelSerializer):
    list = UnitSerializer(source='units', many=True, read_only=True)
    class Meta:
        model = Book
        fields = ['id','name', 'style', 'is_selected', 'list']