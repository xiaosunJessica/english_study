import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'englishstudy.settings')  # 替换为你的项目名
django.setup()

from corpus.models import Book, Unit, TestDetail, Word

# 1. 抓取 fullList
full_list_url = "https://v.xueweigui.com/ApicorpusFly/fullList"
resp = requests.get(full_list_url)
resp.encoding = 'utf-8'
data = resp.json()["data"]

for chapter_itm in data:
    if not chapter_itm.get("name"):
        continue
    # 写入 corpus
    chapter, _ = Book.objects.get_or_create(
        name=chapter_itm["name"],
        defaults={
            "style": chapter_itm.get("style", "2"),
            "is_selected": int(chapter_itm.get("is_selected", "0") or 0)
        }
    )
    for paper in chapter_itm.get("list", []):
        # 写入 Test
        test, _ = Unit.objects.get_or_create(
            chapter=chapter,
            name=paper["name"],
            defaults={
                "is_checked": int(paper.get("is_checked", "0") or 0),
                "extra": paper.get("extra", ""),
                "url": paper.get("url", ""),
                "word_count": paper.get("word_count", "")
            }
        )
        # 2. 抓取 test 的 url，写入 TestDetail 和 Word
        test_url = paper.get("url")
        if not test_url:
            continue
        try:
            test_resp = requests.get(test_url)
            test_resp.encoding = 'utf-8'
            test_data = test_resp.json()
            for detail in test_data.get("data", []):
                # 写入 TestDetail
                test_detail, _ = TestDetail.objects.get_or_create(
                    test=test,
                    text=detail.get("text", ""),
                    defaults={
                        "count": int(detail.get("count", 0) or 0),
                        "unit_id": int(detail.get("unit_id", 0) or 0),
                        "product_type": int(detail.get("product_type", 0) or 0),
                        "url": detail.get("url", ""),
                        "check_url": detail.get("check_url", ""),
                        "lesson_id": int(detail.get("lesson_id", 0) or 0),
                        "is_selected": int(detail.get("is_selected", 0) or 0)
                    }
                )
                for word in detail.get("list", []):
                    # 写入 Word
                    Word.objects.get_or_create(
                        test_detail=test_detail,
                        text=word.get("text", ""),
                        defaults={
                            "note": word.get("note", ""),
                            "voice": word.get("voice", ""),
                            "url": word.get("url", ""),
                            "local_url": word.get("local_url", ""),
                            "word_id": word.get("word_id", ""),
                            "error_num": word.get("error_num", ""),
                            "lesson_id": int(word.get("lesson_id", 0) or 0)
                        }
                    )
        except Exception as e:
            print(f"抓取 {test_url} 失败: {e}")

print("所有 testdetail 和 words 数据已写入数据库。")