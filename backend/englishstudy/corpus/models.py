from django.db import models

# Create your models here.
from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=100)  # 如 "Chapter 3 雅思听力特别名词语料库"
    style = models.CharField(max_length=10, default="2")
    is_selected = models.CharField(max_length=10, default="2")

    def __str__(self):
        return self.name

class Unit(models.Model):
    book = models.ForeignKey(Book, related_name='units', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # 如 "Test Paper 1"
    is_checked = models.CharField(max_length=10, default="2")
    extra = models.CharField(max_length=100, blank=True)
    url = models.URLField()
    word_count = models.CharField(max_length=50)  # 如 "共112个单词"

    def __str__(self):
        return self.name

class Lesson(models.Model):
    test = models.ForeignKey(Unit, related_name='lessons', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True)
    count = models.IntegerField(default=0)
    unit_id = models.IntegerField(null=True, blank=True)
    product_type = models.IntegerField(null=True, blank=True)
    url = models.TextField(blank=True)
    check_url = models.TextField(blank=True)
    lesson_id = models.IntegerField(null=True, blank=True)
    is_selected = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

class Word(models.Model):
    test_detail = models.ForeignKey(Lesson, related_name='words', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True)
    voice = models.CharField(max_length=100, blank=True)
    url = models.TextField(blank=True)
    local_url = models.CharField(max_length=255, blank=True)
    word_id = models.CharField(max_length=50, blank=True)
    error_num = models.CharField(max_length=20, blank=True)
    lesson_id = models.IntegerField(null=True, blank=True)