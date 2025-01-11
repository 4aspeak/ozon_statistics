import datetime
import time
import traceback
from typing import List

import pytz
import requests
from app.settings import logger, OZON_PERFORMANCE_CLIENT_ID, OZON_PERFORMANCE_CLIENT_SECRET


class OzonPerformance:
    def __init__(
            self,
            client_id: str = OZON_PERFORMANCE_CLIENT_ID,
            client_secret: str = OZON_PERFORMANCE_CLIENT_SECRET
    ):
        self.host = "https://api-performance.ozon.ru"
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token: str or None = None

    def set_access_token(self):
        url = f"{self.host}/api/client/token"
        body = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        try:
            response = requests.post(url, json=body)
            result = response.json()
            access_token = result["access_token"]
            logger.info(f"Access token: {access_token}")
            self.access_token = access_token

        except Exception as e:
            logger.error(f"{e}\n{traceback.format_exc()}")
            self.set_access_token()

    def get_campaigns(self):
        result = {
            "data": {},
            "status_code": None
        }
        url = f"{self.host}/api/client/campaign"
        query_params = {
            "advObjectType": "SKU",
            # "state": "CAMPAIGN_STATE_RUNNING"
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers, params=query_params)
        result["data"] = response.json()
        result["status_code"] = response.status_code
        return result

    def get_campaign_products(self, campaign_id: int):
        result = {
            "data": {},
            "status_code": None
        }
        url = f"{self.host}/api/client/campaign/{campaign_id}/v2/products"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers)
        result["data"] = response.json()
        result["status_code"] = response.status_code
        return result

    def check_report_status(self, uuid_order: str):
        result = {
            "data": {},
            "status_code": None
        }
        states = ["NOT_STARTED", "IN_PROGRESS", "ERROR", "OK"]
        url = f"{self.host}/api/client/statistics/{uuid_order}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers)
        result["data"] = response.json()
        result["status_code"] = response.status_code
        return result

    def get_report(self, uuid_order: str):
        result = {
            "data": {},
            "status_code": None
        }
        url = f"{self.host}/api/client/statistics/report"
        query_params = {
            "UUID": uuid_order
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers, params=query_params)
        result["data"] = response.json()
        result["status_code"] = response.status_code
        return result

    def generate_campaign_statistics(self, campaign_ids: List[int], date_from: str, date_to: str):
        print(f"campaign_ids: {campaign_ids}")
        print(f"date_from: {date_from}")
        print(f"date_to: {date_to}")

        result = {
            "data": {},
            "status_code": None
        }
        url = f"{self.host}/api/client/statistics/json"
        body = {
            "campaigns": campaign_ids,
            "dateFrom": date_from,
            "dateTo": date_to,
            "groupBy": "DATE"
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.post(url, json=body, headers=headers)
        result["data"] = response.json()
        result["status_code"] = response.status_code
        print("result: {}".format(result))
        return result

    def get_report_campaign_statistics(self, uuid_order: str):
        result = {
            "data": {},
            "status_code": None
        }
        report = self.get_report(uuid_order)
        data = report["data"]
        status_code = report["status_code"]
        result["status_code"] = status_code
        if status_code == 200:
            for campaign, campaign_value in data.items():
                campaign_report = campaign_value["report"]
                rows = campaign_report["rows"]
                for row in rows:
                    views = int(row["views"])
                    clicks = int(row["clicks"])
                    ctr = float(row["ctr"].replace(",", "."))
                    money_spent = float(row["moneySpent"].replace(",", "."))
                    avg_bid = float(row["avgBid"].replace(",", "."))
                    sku = row["sku"]
                    price = float(row["price"].replace(",", "."))

                    if result["data"].get(sku) is None:
                        result["data"][sku] = {
                            "views": views,
                            "clicks": clicks,
                            "ctr": ctr,
                            "money_spent": money_spent,
                            "avg_bid": avg_bid,
                            "price": price,
                        }
                    else:
                        result["data"][sku]["views"] += views
                        result["data"][sku]["clicks"] += clicks
                        result["data"][sku]["ctr"] += ctr
                        result["data"][sku]["money_spent"] += money_spent
                        result["data"][sku]["avg_bid"] += avg_bid
                        result["data"][sku]["price"] += price
        return result

    def generate_orders_statistics(self, date_from: datetime.datetime, date_to: datetime.datetime):
        result = {
            "data": {},
            "status_code": None
        }
        url = f"{self.host}/api/client/statistic/products/generate/json"
        body = {
            "from": date_from.isoformat(),
            "to": date_to.isoformat(),
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.post(url, json=body, headers=headers)
        result["data"] = response.json()
        result["status_code"] = response.status_code
        return result

    def get_report_orders_statistics(self, uuid_order: str):
        result = {
            "data": [],
            "status_code": None
        }
        report = self.get_report(uuid_order)
        data = report["data"]
        status_code = report["status_code"]
        result["status_code"] = status_code
        if status_code == 200:
            rows = data["report"]["rows"]
            for row in rows:
                money_spent = float(row["moneySpent"].replace(",", "."))
                result["data"].append(
                    {
                        "sku": row["sku"],
                        "money_spent": money_spent,
                    }
                )
        return result


if __name__ == '__main__':
    date = datetime.datetime(
        year=2024, month=10, day=20, hour=0, minute=0, second=0, tzinfo=pytz.timezone('Europe/Moscow')
    )
    ozon_performance = OzonPerformance()
    ozon_performance.set_access_token()

    status = False
    uuid = ""
    while not status:
        order_generation_result = ozon_performance.generate_orders_statistics(date_from=date, date_to=date)
        if order_generation_result["status"] != 200:
            time.sleep(1)
        else:
            uuid = order_generation_result["data"]["UUID"]
            status = True

    status = False
    while not status:
        report_status = ozon_performance.check_report_status(uuid)
        status_name = report_status["state"]
        if status_name == "OK":
            status = True
        else:
            time.sleep(1)
    report = ozon_performance.get_report_orders_statistics(uuid)
