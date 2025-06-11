from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Lesson, Unit
from .serializers import UnitSerializer, LessonDetailSerializer

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
        book_id = request.GET.get('book_id')
        unit_id = request.GET.get('unit_id')
        lesson_id = request.GET.get('lesson_id')

        if not all([unit_id, lesson_id]):
            return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

        # 找到对应的lesson
        try:
            lesson = Lesson.objects.get(
                id=lesson_id,
                unit__id=unit_id)
        except Lesson.DoesNotExist:
            return Response({"e": "4004", "m": "未找到对应试卷"}, status=404)
        # 找到该 lesson 下所有 words

        serializer = LessonDetailSerializer(lesson)
        return Response({
            "e": "9999",
            "m": "操作成功",
            "title": f"",
            "data": serializer.data
        })
