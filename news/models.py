from typing import Self

from django.db import models

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='新聞標題')
    source_url = models.URLField(unique=True, verbose_name='原始連結')
    content = models.TextField(blank=True, verbose_name='新聞內容')
    image_url = models.URLField(max_length=500, blank=True, verbose_name='縮圖連結')
    published_at = models.DateTimeField(db_index=True, verbose_name='發布時間')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='抓取時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最後更新時間')

    class Meta:
        ordering = ('-published_at',)  # 預設按發布時間倒序排列
        verbose_name = '新聞'

    def __str__(self: Self) -> str:
        return self.title
