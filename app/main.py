import time
import traceback

from app.enums import ProductFields, AnalyticalDataFields, PvpFields, TrfFields, ValueName
from app.services.google_sheets import CustomGoogleTable, CustomWorksheet
from app.services.ozon_seller import OzonSeller
from app.services.ozon_performance import OzonPerformance
from app.services.utils import get_date_of_ozon_format
from app.settings import logger
import datetime
import pytz


def replace_key_dict(enum_class, product_dict):
    for field in enum_class:
        if field.value[ValueName.api_name] in product_dict:
            product_dict[field.value[ValueName.main_name]] = product_dict.pop(field.value[ValueName.api_name])
    return product_dict


def get_analytical_data(ozon_seller: OzonSeller, date: datetime.datetime) -> dict:
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

    result = {}

    try:
        date_from = get_date_of_ozon_format(date)
        date_to = get_date_of_ozon_format(date)
        logger.info("Analytical data: api call")
        analytical_data = None
        while analytical_data is None:
            analytical_data = ozon_seller.analytical_data(date_from=date_from, date_to=date_to)
        logger.info("Analytical data:  data parsing")
        data = analytical_data["result"]["data"]
        totals = analytical_data["result"]["totals"]

        for product in data:
            sku = product["dimensions"][0]["id"]
            metrics = product["metrics"]
            result.update({
                sku: _get_metrics(metrics)
            })
        result.update({
            "total": _get_metrics(totals)
        })
    except Exception as e:
        logger.error(f"Метод обработки аналитических данных произошла с ошибкой: {e}\n{traceback.format_exc()}")
        result = None
    return result


def get_total_pvp(pvp: dict):
    total = {
        PvpFields.money_spent.value[ValueName.main_name]: 0
    }

    for sku, data in pvp.items():
        for field in PvpFields:
            total[field.value[ValueName.main_name]] += data[field.value[ValueName.main_name]]
    pvp.update({
        "total": total
    })
    return pvp


def get_total_trf(trf: dict):
    total = {
        TrfFields.views.value[ValueName.main_name]: 0,
        TrfFields.clicks.value[ValueName.main_name]: 0,
        TrfFields.ctr.value[ValueName.main_name]: 0,
        TrfFields.money_spent.value[ValueName.main_name]: 0,
        TrfFields.price.value[ValueName.main_name]: 0,
        TrfFields.avg_bid.value[ValueName.main_name]: 0,
    }

    for sku, data in trf.items():
        for field in TrfFields:
            total[field.value[ValueName.main_name]] += data[field.value[ValueName.main_name]]

    length = len(trf)
    if length == 0:
        values = (0, 0, 0)
    else:
        values = (
            round(total[TrfFields.ctr.value[ValueName.main_name]] / len(trf), 2),
            round(total[TrfFields.avg_bid.value[ValueName.main_name]] / len(trf), 2),
            round(total[TrfFields.price.value[ValueName.main_name]] / len(trf), 2),
        )

    total[TrfFields.ctr.value[ValueName.main_name]] = values[0]
    total[TrfFields.avg_bid.value[ValueName.main_name]] = values[1]
    total[TrfFields.price.value[ValueName.main_name]] = values[2]

    trf.update({
        "total": total
    })

    return trf


def get_pvp(ozon_performance: OzonPerformance, date_from: datetime.datetime, date_to: datetime.datetime):
    ozon_performance.set_access_token()
    result = {}
    try:
        logger.info("PVP: api - generate_orders_statistics call")
        order_generation_result = ozon_performance.generate_orders_statistics(date_from=date_from, date_to=date_to)
        if order_generation_result["status_code"] == 200:
            uuid = order_generation_result["data"]["UUID"]
            logger.info("PVP: uuid: {0}".format(uuid))
        else:
            logger.error(f"Ошибка при генерации статистики заказов: {order_generation_result["data"]}")
            time.sleep(10)
            return get_pvp(ozon_performance, date_from, date_to)

    except Exception as e:
        logger.error(f"Ошибка при генерации статистики заказов: {e}\n{traceback.format_exc()}")
        time.sleep(10)
        return get_pvp(ozon_performance, date_from, date_to)

    count = 0
    status = False
    time.sleep(10)
    while not status:
        count += 1
        ozon_performance.set_access_token()
        logger.info("PVP: api - check_report_status call №{0}".format(count))
        report_status = ozon_performance.check_report_status(uuid)
        status_code = report_status["status_code"]
        if status_code == 200:
            state = report_status["data"]["state"]
            if state == "OK":
                status = True
            elif state == "ERROR":
                logger.error(f"Ошибка при генерации статистики заказов и проверки статуса отчета заказов")
                time.sleep(10)
                return get_pvp(ozon_performance, date_from, date_to)
            else:
                time.sleep(10)
        else:
            logger.error(f"Ошибка при получении статуса отчета заказов: {status_code}")
            time.sleep(10)
            return get_pvp(ozon_performance, date_from, date_to)
    logger.info("PVP: api - get_report_orders_statistics call")
    ozon_performance.set_access_token()
    report = ozon_performance.get_report_orders_statistics(uuid)
    report_status = report["status_code"]

    logger.info("PVP: data parsing")
    if report_status == 200:
        data = report["data"]
        for product in data:
            sku = product.pop("sku")
            product = replace_key_dict(PvpFields, product)
            result.update({
                sku: product
            })
    else:
        logger.error(f"Ошибка с получении статистики продвижения в поиске после генерации и проверки статуса")
        time.sleep(10)
        return get_pvp(ozon_performance, date_from, date_to)
    return result


def get_campaigns_list(ozon_performance: OzonPerformance):
    campaigns_list = []
    ozon_performance.set_access_token()
    campaigns_info = ozon_performance.get_campaigns()
    data = campaigns_info["data"]
    status_code = campaigns_info["status_code"]
    if status_code == 200:
        campaigns = [{"id": elem["id"], "title": elem["title"]} for elem in data["list"]]
        for campaign in campaigns:
            campaigns_list.append(campaign["id"])
    else:
        logger.error(f"Ошибка при получении информации о кампаниях: {data}")
    return campaigns_list


def get_trf(ozon_performance: OzonPerformance, date_from: datetime.datetime, date_to: datetime.datetime):
    logger.info("TRF: api - get_campaigns call")
    campaigns = get_campaigns_list(ozon_performance)
    result = {}
    logger.info("TRF: Length of campaigns list = {0}".format(len(campaigns)))
    for i in range(len(campaigns) // 9 + 1):
        logger.info("TRF: api - generate_campaign_statistics call")
        generation_campaign_statistics = ozon_performance.generate_campaign_statistics(
            campaign_ids=campaigns[i * 9:(i + 1) * 9],
            date_from=get_date_of_ozon_format(date_from),
            date_to=get_date_of_ozon_format(date_to)
        )
        data = generation_campaign_statistics["data"]
        status_code = generation_campaign_statistics["status_code"]
        if status_code == 200:
            uuid = data["UUID"]
            logger.info("TRF: uuid: {0}".format(uuid))
        else:
            logger.error(f"Ошибка при генерации статистики кампании: {data}")
            time.sleep(10)
            return get_trf(ozon_performance, date_from, date_to)

        count = 0
        status = False
        time.sleep(60)
        while not status:
            count += 1
            ozon_performance.set_access_token()
            logger.info("TRF: api - check_report_status call №{0}".format(count))
            report_status = ozon_performance.check_report_status(uuid)
            status_code = report_status["status_code"]
            if status_code == 200:
                state = report_status["data"]["state"]
                if state == "OK":
                    status = True
                elif state == "ERROR":
                    logger.error(f"Ошибка при генерации статистики заказов и проверки статуса отчета заказов")
                    time.sleep(10)
                    return get_trf(ozon_performance, date_from, date_to)
                else:
                    time.sleep(60)
            else:
                logger.error(f"Ошибка при получении статуса отчета заказов: {status_code}")
                time.sleep(10)
                return get_trf(ozon_performance, date_from, date_to)

        logger.info("TRF: api - get_report_campaign_statistics call")
        ozon_performance.set_access_token()
        report = ozon_performance.get_report_campaign_statistics(uuid)

        logger.info("TRF: data parsing")
        data = report["data"]
        status_code = report["status_code"]
        if status_code == 200:
            for sku, sku_data in data.items():
                sku_data = replace_key_dict(TrfFields, sku_data)
                if result.get(sku) is None:
                    result[sku] = sku_data
                else:
                    result[sku]["views"] += sku_data["views"]
                    result[sku]["clicks"] += sku_data["clicks"]
                    result[sku]["ctr"] += sku_data["ctr"]
                    result[sku]["money_spent"] += sku_data["money_spent"]
                    result[sku]["avg_bid"] += sku_data["avg_bid"]
                    result[sku]["price"] += sku_data["price"]

    return result


def get_products(ozon_seller: OzonSeller):
    products_dict = {}
    try:
        products = ozon_seller.products()["result"]["items"]
        for product in products:
            offer_id = product["offer_id"]
            product_id = product["product_id"]
            product_info = ozon_seller.product_info(product_id, offer_id)
            sku = product_info["result"]["sku"]
            is_archived = product_info["result"]["is_archived"]
            if sku not in products_dict:
                products_dict[sku] = {
                    "offer_id": offer_id,
                    # "product_info": product_info["result"],
                    # "offer_id": offer_id,
                    "product_id": product_id,
                    "is_archived": is_archived,
                }
    except Exception as e:
        logger.error(f"Ошибка при получении списка товаров из OzonSeller: {e}\n{traceback.format_exc()}")
        return get_products(ozon_seller)

    return products_dict


def count_drr(general_data: dict):
    for sku, values in general_data.items():
        pvp_money_spent = values.get(PvpFields.money_spent.value[ValueName.main_name], 0)
        trf_money_spent = values.get(TrfFields.money_spent.value[ValueName.main_name], 0)
        revenue = values.get(AnalyticalDataFields.revenue.value[ValueName.main_name], 0)
        if revenue == 0:
            drr = 0
        else:
            drr = (pvp_money_spent + trf_money_spent) / revenue * 100
        drr = round(drr, 3)
        general_data[sku].update({ProductFields.drr.value[ValueName.main_name]: drr})
    try:
        total_pvp_money_spent = general_data["total"].get(PvpFields.money_spent.value[ValueName.main_name], 0)
        total_trf_money_spent = general_data["total"].get(TrfFields.money_spent.value[ValueName.main_name], 0)
        total_revenue = general_data["total"].get(AnalyticalDataFields.revenue.value[ValueName.main_name], 0)
        if total_revenue == 0:
            total_drr = 0
        else:
            total_drr = (total_pvp_money_spent + total_trf_money_spent) / total_revenue * 100
        general_data["total"].update({ProductFields.drr.value[ValueName.main_name]: round(total_drr, 3)})
    except KeyError:
        logger.error("No total value")
    return general_data


def count_conversion(general_data: dict):
    for sku, values in general_data.items():
        ordered_units = values.get(AnalyticalDataFields.ordered_units.value[ValueName.main_name], 0)
        hits_tocart = values.get(AnalyticalDataFields.hits_tocart.value[ValueName.main_name], 0)
        if hits_tocart == 0:
            conversion = 0
        else:
            conversion = ordered_units / hits_tocart * 100
        conversion = round(conversion, 3)
        general_data[sku].update({ProductFields.conversion.value[ValueName.main_name]: conversion})
    try:
        total_ordered_units = general_data["total"].get(AnalyticalDataFields.ordered_units.value[ValueName.main_name], 0)
        total_hits_tocart = general_data["total"].get(AnalyticalDataFields.hits_tocart.value[ValueName.main_name], 0)
        if total_hits_tocart == 0:
            total_conversion = 0
        else:
            total_conversion = total_ordered_units / total_hits_tocart * 100
        general_data["total"].update({ProductFields.conversion.value[ValueName.main_name]: round(total_conversion, 3)})
    except KeyError:
        logger.error("No total value")
    return general_data


def main(date: datetime.datetime):
    table = CustomGoogleTable()
    table.open_by_key()
    ozon_seller = OzonSeller()
    ozon_performance = OzonPerformance()
    general_data = {}
    str_date = date.strftime("%d.%m.%y")

    logger.info("Starting checking")
    logger.info("Calculation start: Analytical data")
    analytical_data = get_analytical_data(ozon_seller, date)
    general_data.update(analytical_data)
    logger.info("Calculation end: Analytical data")

    logger.info("Calculation start: PVP")
    pvp = get_pvp(ozon_performance, date_from=date, date_to=date)
    pvp = get_total_pvp(pvp)

    for sku, data in pvp.items():
        if general_data.get(sku):
            general_data[sku].update(data)
        else:
            general_data.update({sku: data})
    logger.info("Calculation end: PVP")

    logger.info("Calculation start: TRF")
    trf = get_trf(ozon_performance, date_from=date, date_to=date)
    # trf = get_example_trf(date_from=date, date_to=date)
    trf = get_total_trf(trf)
    for sku, data in trf.items():
        if general_data.get(sku):
            general_data[sku].update(data)
        else:
            general_data.update({sku: data})
    logger.info("Calculation end: TRF")

    logger.info("Calculation start: Products")
    products = get_products(ozon_seller)
    logger.info("Calculation end: Products")

    logger.info("Calculation start: DRR")
    general_data = count_drr(general_data)
    logger.info("Calculation end: DRR")

    logger.info("Calculation start: Conversion")
    general_data = count_conversion(general_data)
    logger.info("Calculation end: Conversion")

    logger.info("Making sheets start")
    for sku, values in products.items():
        offer_id = values["offer_id"]
        sku_data = general_data.get(str(sku), {})
        logger.info(f"Making sheets for offer_id: {offer_id}")
        worksheet = CustomWorksheet()
        worksheet_of_table = table.get_worksheet_by_title(offer_id)
        if worksheet_of_table is None:
            worksheet_of_table = table.add_worksheet(offer_id)
            worksheet.set_worksheet(worksheet_of_table)
            worksheet.add_base_columns()
        else:
            worksheet.set_worksheet(worksheet_of_table)
        worksheet.set_all_records()
        worksheet.df[f"Дата: {str_date}"] = [
            sku_data.get(AnalyticalDataFields.revenue.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.ordered_units.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.hits_tocart.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.cancellations.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.delivered_units.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.returns.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.session_view.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.hits_tocart_search.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.hits_tocart_pdp.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.hits_view.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.hits_view_search.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.hits_view_pdp.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.position_category.value[ValueName.main_name], 0),
            sku_data.get(AnalyticalDataFields.session_view_search.value[ValueName.main_name], 0),
            sku_data.get(PvpFields.money_spent.value[ValueName.main_name], 0),
            sku_data.get(TrfFields.price.value[ValueName.main_name], 0),
            sku_data.get(TrfFields.views.value[ValueName.main_name], 0),
            sku_data.get(TrfFields.clicks.value[ValueName.main_name], 0),
            sku_data.get(TrfFields.ctr.value[ValueName.main_name], 0),
            sku_data.get(TrfFields.avg_bid.value[ValueName.main_name], 0),
            sku_data.get(TrfFields.money_spent.value[ValueName.main_name], 0),
            sku_data.get(ProductFields.drr.value[ValueName.main_name], 0),
            sku_data.get(ProductFields.conversion.value[ValueName.main_name], 0),
        ]
        worksheet.update_worksheet()

    logger.info("Making 'All' sheet")
    total_all_worksheet = CustomWorksheet()
    total_all_worksheet.set_worksheet(table.get_worksheet_by_title("All"))
    total_all_worksheet.set_all_records()
    total_all_worksheet.df[f"Дата: {str_date}"] = [
        general_data["total"].get(AnalyticalDataFields.revenue.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.ordered_units.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.hits_tocart.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.cancellations.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.delivered_units.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.returns.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.session_view.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.hits_tocart_search.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.hits_tocart_pdp.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.hits_view.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.hits_view_search.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.hits_view_pdp.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.position_category.value[ValueName.main_name], 0),
        general_data["total"].get(AnalyticalDataFields.session_view_search.value[ValueName.main_name], 0),
        general_data["total"].get(PvpFields.money_spent.value[ValueName.main_name], 0),
        general_data["total"].get(TrfFields.price.value[ValueName.main_name], 0),
        general_data["total"].get(TrfFields.views.value[ValueName.main_name], 0),
        general_data["total"].get(TrfFields.clicks.value[ValueName.main_name], 0),
        general_data["total"].get(TrfFields.ctr.value[ValueName.main_name], 0),
        general_data["total"].get(TrfFields.avg_bid.value[ValueName.main_name], 0),
        general_data["total"].get(TrfFields.money_spent.value[ValueName.main_name], 0),
        general_data["total"].get(ProductFields.drr.value[ValueName.main_name], 0),
        general_data["total"].get(ProductFields.conversion.value[ValueName.main_name], 0),
    ]
    total_all_worksheet.update_worksheet()

    logger.info("Making 'Short All' sheet")
    short_all_worksheet = CustomWorksheet()
    short_all_worksheet.set_worksheet(table.get_worksheet_by_title("Short All"))
    short_all_worksheet.set_all_records()
    short_all_worksheet.df[f"Дата: {str_date}"] = [
        general_data["total"].get(AnalyticalDataFields.revenue.value[ValueName.main_name], 0),
        general_data["total"].get(PvpFields.money_spent.value[ValueName.main_name], 0),
        general_data["total"].get(TrfFields.money_spent.value[ValueName.main_name], 0),
        general_data["total"].get(ProductFields.drr.value[ValueName.main_name], 0),
        general_data["total"].get(ProductFields.conversion.value[ValueName.main_name], 0),
    ]
    short_all_worksheet.update_worksheet()


if __name__ == '__main__':

    start_date = datetime.datetime(
        year=2025, month=1, day=16, hour=0, minute=0, second=0, tzinfo=pytz.timezone('Europe/Moscow')
    )
    one_day = datetime.timedelta(days=1)
    for i in range(1):
        logger.info(f"Start algorithm for date: {start_date}")
        main(start_date)
        new_date = start_date + one_day
        start_date = new_date
