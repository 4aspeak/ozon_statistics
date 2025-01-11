import traceback
from typing import Optional, Dict, Any
import requests
from app.settings import logger, OZON_SELLER_API_KEY, OZON_SELLER_CLIENT_ID


# metrics
# revenue — заказано на сумму,
# ordered_units — заказано товаров.
# unknown_metric — неизвестная метрика.
# hits_view_search — показы в поиске и в категории.
# hits_view_pdp — показы на карточке товара.
# hits_view — всего показов.
# hits_tocart_search — в корзину из поиска или категории.
# hits_tocart_pdp — в корзину из карточки товара.
# hits_tocart — всего добавлено в корзину.
# session_view_search — сессии с показом в поиске или в каталоге.
# Считаются уникальные посетители с просмотром в поиске или каталоге.
# session_view_pdp — сессии с показом на карточке товара.
# Считаются уникальные посетители, которые просмотрели карточку товара.
# session_view — всего сессий. Считаются уникальные посетители.
# conv_tocart_search — конверсия в корзину из поиска или категории.
# conv_tocart_pdp — конверсия в корзину из карточки товара.
# conv_tocart — общая конверсия в корзину.
# returns — возвращено товаров.
# cancellations — отменено товаров.
# delivered_units — доставлено товаров.
# position_category — позиция в поиске и категории.


class OzonSeller:
    def __init__(self, client_id: int = OZON_SELLER_CLIENT_ID, api_key: str = OZON_SELLER_API_KEY):
        self.host = "https://api-seller.ozon.ru"
        self.client_id = client_id
        self.api_key = api_key

    def products(self):
        result = []
        url = f"{self.host}/v2/product/list"
        headers = {
            "Content-Type": "application/json",
            "Client-Id": self.client_id,
            "Api-Key": self.api_key
        }
        try:
            response = requests.post(url, headers=headers)
            result = response.json()
        except Exception as e:
            logger.error(f"Ошибка при запросе данных из OzonSeller: {e}\n{traceback.format_exc()}")
        return result

    def product_info(self, product_id: int, offer_id: str):
        result = None
        url = f"{self.host}/v2/product/info"
        body = {
            "product_id": product_id,
            "offer_id": offer_id
        }
        headers = {
            "Content-Type": "application/json",
            "Client-Id": self.client_id,
            "Api-Key": self.api_key
        }
        try:
            response = requests.post(url, json=body, headers=headers)
            result = response.json()
        except Exception as e:
            logger.error(f"Ошибка при запросе данных из OzonSeller: {e}\n{traceback.format_exc()}")
        return result

    def analytical_data(self, date_from: str = None, date_to: str = None):
        result: Optional[Dict[str, Any]] = None
        url = f"{self.host}/v1/analytics/data"
        body = {
            "date_from": date_from,
            "date_to": date_to,
            "metrics": [
                "revenue",
                "ordered_units",
                "hits_tocart",
                "cancellations",
                "delivered_units",
                "returns",
                "session_view",
                "hits_tocart_search",
                "hits_tocart_pdp",
                "hits_view",
                "hits_view_search",
                "hits_view_pdp",
                "position_category",
                "session_view_search"
            ],
            "dimension": [
                "sku",
                "day"
            ],
            "sort": [
                {
                    "order": "DESC"
                }
            ],
            "limit": 1000,
            "offset": 0
        }
        headers = {
            "Content-Type": "application/json",
            "Client-Id": self.client_id,
            "Api-Key": self.api_key
        }
        try:
            response = requests.post(url, json=body, headers=headers)
            result = response.json()
        except Exception as e:
            logger.error(f"Ошибка при запросе данных из OzonSeller: {e}\n{traceback.format_exc()}")
        return result



