import datetime
import time
from pprint import pprint
import pytz
import json
from services.ozon_performance import OzonPerformance
from services.ozon_seller import OzonSeller
from main import get_pvp, get_campaigns_list, get_trf, get_total_pvp, get_total_trf, get_products
from services.utils import get_date_of_ozon_format
from enums import AnalyticalDataFields, ValueName, PvpFields, TrfFields, ProductFields


def _get_metrics(metrics_list):
    return {
        AnalyticalDataFields.revenue.value[ValueName.main_name]: metrics_list[0],
        AnalyticalDataFields.ordered_units.value[ValueName.main_name]: metrics_list[1],
        AnalyticalDataFields.hits_tocart.value[ValueName.main_name]: metrics_list[2],
        AnalyticalDataFields.cancellations.value[ValueName.main_name]: metrics_list[3],
        AnalyticalDataFields.delivered_units.value[ValueName.main_name]: metrics_list[4],
        AnalyticalDataFields.returns.value[ValueName.main_name]: metrics_list[5],
        AnalyticalDataFields.session_view.value[ValueName.main_name]: metrics_list[6],
        AnalyticalDataFields.hits_tocart_search.value[ValueName.main_name]: metrics_list[7],
        AnalyticalDataFields.hits_tocart_pdp.value[ValueName.main_name]: metrics_list[8],
        AnalyticalDataFields.hits_view.value[ValueName.main_name]: metrics_list[9],
        AnalyticalDataFields.hits_view_search.value[ValueName.main_name]: metrics_list[10],
        AnalyticalDataFields.hits_view_pdp.value[ValueName.main_name]: metrics_list[11],
        AnalyticalDataFields.position_category.value[ValueName.main_name]: round(metrics_list[12], 3),
        AnalyticalDataFields.session_view_search.value[ValueName.main_name]: metrics_list[13],
    }


if __name__ == '__main__':
    # date_from = datetime.datetime(
    #     year=2024, month=12, day=1, hour=0, minute=0, second=0, tzinfo=pytz.timezone('Europe/Moscow')
    # )
    # date_to = datetime.datetime(
    #     year=2024, month=12, day=6, hour=0, minute=0, second=0, tzinfo=pytz.timezone('Europe/Moscow')
    # )
    # ozon_date_from = get_date_of_ozon_format(date_from)
    # ozon_date_to = get_date_of_ozon_format(date_to)
    #
    # result = {}
    ozon_seller = OzonSeller()

    # analytical_data = ozon_seller.analytical_data(ozon_date_from, ozon_date_to)
    # data = analytical_data["result"]["data"]
    # totals = analytical_data["result"]["totals"]
    # pprint(data)
    products = get_products(ozon_seller)
    pprint(products)
    print(len(products))
    # # with open('analytical_data_data.json', 'w') as f:
    # #     json.dump(data, f, indent=4)
    #
    # with open('analytical_data_total.json', 'w') as f:
    #     json.dump(totals, f, indent=4)

    # for product in data:
    #     sku = product["dimensions"][0]["id"]
    #     ozon_date = product["dimensions"][1]["id"]
    #     date = datetime.datetime.strptime(ozon_date, "%Y-%m-%d")
    #     metrics = product["metrics"]

    # ozon_performance = OzonPerformance()
    # #
    # ozon_performance.set_access_token()
    # campaigns = get_campaigns_list(ozon_performance)
    # # print(ozon_performance.generate_campaign_statistics(
    # #     campaigns[10:], date_from=ozon_date_from, date_to=ozon_date_to
    # # ))
    #
    # uuid = "eec08d65-4475-41b3-aebf-61845642530a"
    # while True:
    #     print(ozon_performance.check_report_status(uuid))
    #     time.sleep(1)


    # trf = ozon_performance.get_report(uuid)["data"]
    #
    # print(trf)
    # for sku, sku_data in trf.items():
    #     result.update({
    #         sku: sku_data["report"]["rows"]
    #     })
    # #
    # with open('trf4.json', 'w') as f:
    #     json.dump(result, f, indent=4)


    # pprint(get_products(ozon_seller))

    # def str_datetime_to_date(str_datetime):
    #     try:
    #         return datetime.datetime.strptime(str_datetime, "%Y-%m-%dT%H:%M:%S").date()
    #     except Exception as e:
    #         return None
    #
    # date = datetime.date(2023, 12, 3)
    # new_month = (date.month + 6) // 12
    # print(new_month)
    # print(date.month)
    # print((date.month + 6) % 12)
    # new_year = date.year + ((date.month + 6) % 12)
    # new_date = datetime.datetime(new_year, new_month, date.day)
    # print(new_date.isoformat())

    # print(20 // 9 + 1)
