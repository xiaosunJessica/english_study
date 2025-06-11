# *_* coding: utf-8 *_* 
# @Time: 2025/6/7 17:41
# @Author: JessicaSun
# @File: serializers
# @Project: backend
from rest_framework import serializers
from .models import LessonTest, Unit, Lesson,  Word

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            'id', 'text', 'note', 'voice', 'url', 'local_url',
            'word_id', 'error_num', 'lesson_id', 'is_wrong', 'wrong_num'
        ]

class LessonTestSerializer(serializers.ModelSerializer):
    words = WordSerializer(many=True, read_only=True)
    class Meta:
        model = Lesson
        fields = [
            'id', 'text', 'count', 'unit_id', 'product_type', 'url',
            'check_url', 'unit_id', 'is_selected', 'words'
        ]

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id','name', 'is_checked', 'extra', 'url', 'word_count', 'unit_id']

class LessonDetailSerializer(serializers.ModelSerializer):
    list = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['name', 'url', 'word_count', 'error_count', 'extra', 'list']

    def get_list(self, obj):
        return WordSerializer(obj.words.all(), many=True).data

class UnitSerializer(serializers.ModelSerializer):
    list = LessonSerializer(source='lessons', many=True, read_only=True)
    class Meta:
        model = Unit
        fields = ['id','title', 'style', 'is_selected', 'intro', 'list']