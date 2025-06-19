# import json

from rest_framework import status

# Create your views here.
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Lesson, Unit, Word
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

# 提交错误
'''
@csrf_exempt
def set_error_words(self):
    if (self.method == 'POST'):
        try:
            data = json.loads(self.body)
            ids = [ item['id'] for item in data.get('id', [])]

            #批量更新
            updated = Word.objects.filter(word_id_in = ids).update(is_wrong = 2)

            for word in Word.objects.filter(word_id__in=ids):
                word.wrong_num = (word.wrong_num or 0) + 1
                word.save()
            return Response({
                "e": "9999",
                "m": "操作成功",
                "title": f"",
                "data": updated
            })
        except Exception as e:
            return Response({
                "e": "0000",
                "m": "操作失败"
            }, status=400)

'''

class SetErrorWordsView(APIView):
    def post(self, request):
        try:
            error_words = request.data.get('errorWords', {})
            ids = list(error_words.keys())
            lesson_id = request.data.get('lesson_id')
            # 先将本lesson下的所有单词is_wrong设置为1
            Word.objects.filter(lesson_id = lesson_id).update(is_wrong = 1)
            # 批量更新is_wrong字段
            updated = Word.objects.filter(id__in = ids).update(is_wrong = 2)

            # 错误次数+1
            for word in Word.objects.filter(id__in = ids):
                word.wrong_num = (word.wrong_num or 0) + 1
                word.error_text = error_words.get(str(word.id), "")
                word.save()

            return Response({
                "e": "9999",
                "m": "操作成功",
                "updated": updated
            })
        except Exception as e:
            return Response({
                "e": "4001",
                "m": f"操作失败: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

