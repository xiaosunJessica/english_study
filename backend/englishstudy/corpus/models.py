from django.db import models

# Create your models here.
from django.db import models

class Unit(models.Model):
    title = models.CharField(max_length=100)  # 如 "Chapter 3 "
    intro = models.CharField(max_length=100, default="") # 雅思听力特别名词语料库
    style = models.CharField(max_length=10, default="2")
    is_selected = models.CharField(max_length=10, default="2")

    def __str__(self):
        return self.name

class Lesson(models.Model):
    STATUS_CHOICES = (
        (1, '未练习'),
        (2, '已练习'),
    )
    unit = models.ForeignKey(Unit, related_name='lessons', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # 如 "Test Paper 1"
    is_checked = models.CharField(max_length=10, default="2")
    extra = models.CharField(max_length=100, blank=True)
    url = models.URLField()
    word_count = models.CharField(max_length=50)  # 如 "共112个单词"
    error_count = models.CharField(max_length=50) # 如 "错5个单词"
    more = models.CharField(max_length= 100) # 未练 / 正确率
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.name

class Word(models.Model):
    WRONG_CHOICES = (
        (1, '正确'),
        (2, '错误'),
    )
    lesson = models.ForeignKey(Lesson, related_name='words', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True)
    voice = models.CharField(max_length=100, blank=True)
    url = models.TextField(blank=True)
    local_url = models.CharField(max_length=255, blank=True)
    word_id = models.CharField(max_length=50, blank=True)
    error_num = models.CharField(max_length=20, blank=True)
    is_wrong = models.PositiveSmallIntegerField(choices=WRONG_CHOICES, null=True, blank=True)
    wrong_num = models.IntegerField(default=0) # 错误次数
    def __str__(self):
        return self.name


class LessonTest(models.Model):
    unit = models.ForeignKey(Unit, related_name='LessonTest', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True)
    count = models.IntegerField(default=0)
    product_type = models.IntegerField(null=True, blank=True)
    url = models.TextField(blank=True)
    check_url = models.TextField(blank=True)
    is_selected = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

