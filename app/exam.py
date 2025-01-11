import datetime
import json

import pytz

from enums import ValueName, TrfFields

trf_file = "trf3.json"


def replace_key_dict(product_dict):
    new_dict = {
        "trf_views": int(product_dict.pop("views")),
        "trf_clicks": int(product_dict.pop("clicks")),
        "trf_ctr": float(product_dict.pop("ctr").replace(",", ".")),
        "trf_money_spent": float(product_dict.pop("moneySpent").replace(",", ".")),
        "trf_price": float(product_dict.pop("price").replace(",", ".")),
        "trf_avg_bid": float(product_dict.pop("avgBid").replace(",", ".")),
    }
    return new_dict


def get_example_trf(date_from: datetime.datetime, date_to: datetime.datetime=None):
    one_day_date = date_from.strftime("%d.%m.%Y")
    with open(trf_file, "r") as f:
        trf = json.load(f)
    result = {}
    for campaign, data in trf.items():
        for day_data in data:
            sku = day_data["sku"]
            if day_data["date"] == one_day_date:
                result.update({
                    sku: replace_key_dict(day_data)
                })
    return result


if __name__ == '__main__':
    date = datetime.datetime(
        year=2024, month=10, day=11, hour=0, minute=0, second=0, tzinfo=pytz.timezone('Europe/Moscow')
    )
    trf = get_example_trf(date_from=date, date_to=date)
