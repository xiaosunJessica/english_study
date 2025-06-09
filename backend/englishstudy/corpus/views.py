from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class ChapterFullListView(APIView):
    def get(self, request):
        books = Book.objects.prefetch_related('units').all()
        serializer = BookSerializer(books, many=True)
        return Response({
            "e": "9999",
            "m": "操作成功",
            "title": "全本语料库列表",
            "data": serializer.data
        })