from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Lesson, Unit
from .serializers import UnitSerializer, LessonSerializer

class CorpusFullListView(APIView):
    def get(self, request):
        units = Unit.objects.prefetch_related('lessons').all()
        serializer = UnitSerializer(units, many=True)
        return Response({
            "e": "9999",
            "m": "操作成功",
            "title": "全本语料库列表",
            "data": serializer.data
        })

class CorpusFullItemView(APIView):
    def get(self, request):
        # 获取参数
        name = request.GET.get('name')
        book_id = request.GET.get('book_id')
        unit_id = request.GET.get('unit_id')
        lesson_id = request.GET.get('lesson_id')

        # 找到对应的unit
        try:
            unit = Lesson.objects.get(name = name, unit_id = unit_id, lesson_id=lesson_id)
        except Unit.DoesNotExist:
            return Response({"e": "4004", "m": "未找到对应试卷"}, status=404)
        # 找到该 Unit 下所有 Lesson

        lessons = unit.lessons.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response({
            "e": "9999",
            "m": "操作成功",
            "title": f"{unit.book.name} {unit.name}",
            "data": serializer.data
        })
