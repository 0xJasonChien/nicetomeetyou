import logging
from abc import ABC, abstractmethod
from typing import Any, Self


class BaseCrawler(ABC):
    def __init__(self: Self, base_url: str) -> None:
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
        }
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self: Self) -> None:
        self.logger.info('開始爬蟲任務...')
        try:
            # 1. 取得原始網頁內容
            raw_data = self.fetch_raw_data()

            # 2. 解析內容轉為結構化資料
            parsed_items = self.parse_data(raw_data)

            # 3. 儲存至資料庫
            count = self.save_data(parsed_items)

            msg = f'任務完成, 共儲存 {count} 筆資料。'
            self.logger.info(msg)
        except Exception as e:
            msg = f'爬蟲執行失敗: {e!s}'
            self.logger.exception(msg)

    @abstractmethod
    def fetch_raw_data(self: Self) -> None:
        """定義如何發送請求"""

    @abstractmethod
    def parse_data(self: Self, raw_data: Any) -> list[dict[str, Any]]:
        """定義如何解析 HTML 或 JSON, 應回傳一個清單 (List of dicts)"""

    @abstractmethod
    def save_data(self: Self, items: list[dict[str, Any]]) -> int:
        """定義如何將資料寫入 Django Model, 然後回傳儲存的筆數"""
