from typing import Any, Self

import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from your_app.models import News  # 請替換為你實際的 app 名稱

from crawler.base import BaseCrawler


class UDNNBANewsCrawler(BaseCrawler):

    def fetch_raw_data(self: Self) -> str:
        """負責發送請求並回傳原始 HTML 文字"""
        response = requests.get(self.base_url, headers=self.headers)
        response.encoding = 'utf-8'
        response.raise_for_status()  # 若狀態碼非 200 會拋出例外
        return response.text

    def parse_data(self: Self, raw_data: str) -> list[dict[str, Any]]:
        """負責解析 HTML 並轉換為字典清單"""
        soup = BeautifulSoup(raw_data, 'html.parser')
        news_items = soup.select('#news_list_body dt')

        parsed_results = []
        for item in news_items:
            try:
                title_tag = item.select_one('h3')
                link_tag = item.select_one('a')

                if title_tag and link_tag:
                    parsed_results.append(
                        {
                            'title': title_tag.text.strip(),
                            'link': 'https://tw-nba.udn.com' + link_tag['href'],
                            # 備註：首頁列表通常沒內文與精確時間，
                            # 建議在進階實作中再對 link 發起請求抓取詳細資訊
                        },
                    )
            except Exception as e:
                self.logger.warning(f'解析單筆新聞失敗: {e}')

        return parsed_results

    def save_data(self: Self, items: list[dict[str, Any]]) -> int:
        """負責將資料寫入資料庫，並回傳成功新增的筆數"""
        new_count = 0
        for item in items:
            # 使用 update_or_create 避免重複抓取
            obj, created = News.objects.update_or_create(
                source_url=item['link'],
                defaults={
                    'title': item['title'],
                    'published_at': timezone.now(),  # 若 parse 未抓到時間，先以當下代替
                },
            )
            if created:
                new_count += 1
                # TODO: 這裡可以實作 WebSocket 發送新新聞通知

        return new_count
