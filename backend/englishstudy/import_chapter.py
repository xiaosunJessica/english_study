import os
import django
import requests
from urllib.parse import urlparse, parse_qs

# Django 环境设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'englishstudy.settings')
django.setup()

from corpus.models import Unit, Lesson, Word

urls = [
    'https://v.xueweigui.com/ApicorpusFly/fullItem?anchor=all&name=Test%20Paper%201&book_id=10006&unit_id=4&lesson_id=10026',
    'https://v.xueweigui.com/ApicorpusFly/fullItem?anchor=all&name=Test%20Paper%201&book_id=10006&unit_id=4&lesson_id=10027',
    'https://v.xueweigui.com/ApicorpusFly/fullItem?anchor=all&name=Test%20Paper%201&book_id=10006&unit_id=4&lesson_id=10028',
    'https://v.xueweigui.com/ApicorpusFly/fullItem?anchor=all&name=Test%20Paper%201&book_id=10006&unit_id=4&lesson_id=10029'
]

session = requests.Session()

for url in urls:
    try:
        # 解析 unit_id 与 lesson_id
        qs = parse_qs(urlparse(url).query)
        unit_id  = int(qs.get('unit_id',   [0])[0])

        if not unit_id:
            print(f'URL 缺少必要参数：{url}')
            continue

        # 请求数据
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
        data_node = resp.json().get('data')
        if not data_node:
            print(f'API 无有效数据：{url}')
            continue
        lesson_data = data_node[0]

        # 确保 Unit 存在
        unit, _ = Unit.objects.get_or_create(
            id=unit_id,
            defaults={'title': f'Unit {unit_id}'}
        )

        # ★ 关键：用 lesson_id 作为主键写入 Lesson
        lesson, _ = Lesson.objects.get_or_create(
            unit=unit,  # 这里传的是 Unit 对象
            url=url,  # 查找条件之一
            defaults={  # 新建时赋的默认字段
                'name': lesson_data.get('text', 'No title'),
                'word_count': int(lesson_data.get('word_count', 0)),
            }
        )

        # 写入 Word：同一个 (lesson, text) 只留一条
        for w in lesson_data.get('list', []):
            Word.objects.update_or_create(
                lesson=lesson,
                text=w.get('text', ''),
                defaults={
                    'note':      w.get('note', ''),
                    'voice':     w.get('voice', ''),
                    'url':       w.get('url', ''),
                    'local_url': w.get('local_url', ''),
                    'error_num': w.get('error_num', ''),
                }
            )
        print(f'✅ 完成：lesson ')

    except Exception as e:
        print(f'❌ 处理 {url} 时出错：{e}')

print('全部写入完成')
