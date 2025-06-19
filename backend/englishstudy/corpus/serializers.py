# *_* coding: utf-8 *_*
# @Time: 2025/6/7 17:41
# @Author: JessicaSun
# @File: serializers
# @Project: backend
from rest_framework import serializers
from .models import Unit, Lesson,  Word

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            'id', 'text', 'note', 'voice', 'url', 'local_url', 'error_num', 'lesson_id', 'is_wrong', 'wrong_num'
        ]

class LessonSerializer(serializers.ModelSerializer):
    # 1️⃣ 声明一个只读方法字段
    more = serializers.SerializerMethodField()
    class Meta:
        model = Lesson
        fields = ['id','name', 'is_checked', 'extra', 'url', 'word_count', 'unit_id', 'more']

    def get_more(self, obj):
        if obj.status == 1:
            if obj.word_count:
                accuracy = 1 - (obj.error_count / obj.word_count)
                # 限定在 0~1 之间，避免 error_num > word_count 时出现负值
                accuracy = max(0, min(accuracy, 1))
                return f"正确率{accuracy:.2%}"
            else:
                return "正确率0.00%"
        else:
            return "未练习"

class LessonDetailSerializer(serializers.ModelSerializer):
    list = serializers.SerializerMethodField()
    class Meta:
        model = Lesson
        fields = ['name', 'url', 'word_count', 'error_count', 'extra', 'list', 'status']

    def get_list(self, obj):
        return WordSerializer(obj.words.all(), many=True).data

class UnitSerializer(serializers.ModelSerializer):
    list = LessonSerializer(source='lessons', many=True, read_only=True)
    class Meta:
        model = Unit
        fields = ['id','title', 'style', 'is_selected', 'intro', 'list']