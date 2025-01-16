import time
import traceback
from datetime import datetime
from typing import Optional, List

import pandas as pd
from gspread import Worksheet, WorksheetNotFound
from gspread.utils import ValueInputOption

from app.settings import logger, GSPREAD_CLIENT, TABLE_ID_OF_OZON_STATISTICS
from gspread.exceptions import APIError


class CustomWorksheet:
    def __init__(self):
        self.worksheet: Optional[Worksheet] = None
        self.df: Optional[pd.DataFrame] = None

    def set_worksheet(self, worksheet: Worksheet) -> None:
        self.worksheet = worksheet

    def set_all_records(self) -> None:
        if self.worksheet is None:
            logger.info("INFO: worksheet is not set")
        else:
            try:
                result: List[dict] = self.worksheet.get_all_records(
                    numericise_ignore=["all"]
                )
                self.df = pd.DataFrame(result)
            except APIError as e:
                logger.error(f"Api Error: {e}")
                time.sleep(40)
                self.set_all_records()
            except Exception as e:
                logger.error(f"{e}\n{traceback.format_exc()}")
                time.sleep(10)
                self.set_all_records()

    def get_last_date(self) -> Optional[datetime]:
        result: Optional[datetime] = None
        if self.df is None:
            logger.info("INFO: df is not set")
        else:
            date_str = self.df.columns[-1]
            result = datetime.strptime(date_str, '%d.%m.%y')
        return result

    def add_base_columns(self) -> None:
        values = [
            "Заказано на сумму",
            "Заказано товаров, шт",
            "Всего добавлено в корзину",
            "Отменено товаров",
            "Доставлено товаров",
            "Возвращено товаров",
            "Всего сессий",
            "В корзину из поиска или категории",
            "В корзину из карточки товара",
            "Всего показов",
            "Показы в поиске и в категории",
            "Показы на карточке товара",
            "Позиция в поиске и категории",
            "Сессии с показом в поиске или в каталоге",
            "Продвижение в поиске - Расход",
            "Трафареты - Цена товара, ₽",
            "Трафареты - Показы",
            "Трафареты - Клики",
            "Трафареты - CTR (%)",
            "Трафареты - Ср. цена клика, ₽",
            "Трафареты - Расход",
            "ДРР",
            "Конверсия из корзины",
        ]
        self.df = pd.DataFrame(
            {
                "Тип данных": values,
            }
        )
        self.update_worksheet()

    def update_worksheet(self) -> None:
        if self.worksheet is None or self.df is None:
            logger.info("INFO: worksheet or df is not set")
        else:
            try:
                self.worksheet.update(
                    values=[self.df.columns.values.tolist()] + self.df.values.tolist(),
                    value_input_option=ValueInputOption.user_entered,
                )
            except APIError as e:
                logger.error(f"Api Error: {e}")
                time.sleep(40)
                self.update_worksheet()
            except Exception as e:
                logger.error(f"Error: {e}\n{traceback.format_exc()}")
                time.sleep(20)
                self.update_worksheet()


class CustomGoogleTable:
    def __init__(self):
        self.sh = None

    def open_by_key(self):
        try:
            self.sh = GSPREAD_CLIENT.open_by_key(TABLE_ID_OF_OZON_STATISTICS)
        except APIError as e:
            logger.error(f"Api Error: {e}")
            time.sleep(40)
            self.open_by_key()
        except Exception as e:
            logger.error(f"{e}\n{traceback.format_exc()}")
            time.sleep(10)
            self.open_by_key()

    def get_worksheets(self):
        return self.sh.worksheets()

    def get_worksheet_by_title(self, title: str):
        try:
            return self.sh.worksheet(title=title)
        except WorksheetNotFound:
            return None
        except APIError as e:
            logger.error(f"Api Error: {e}")
            time.sleep(40)
            return self.get_worksheet_by_title(title)
        except Exception as e:
            logger.error(f"{e}\n{traceback.format_exc()}")
            time.sleep(10)
            return self.get_worksheet_by_title(title)

    def add_worksheet(self, title: str, rows: int = 100, cols: int = 100):
        try:
            return self.sh.add_worksheet(title=title, rows=rows, cols=cols)
        except APIError as e:
            logger.error(f"Api Error: {e}")
            time.sleep(40)
            return self.add_worksheet(title, rows=100, cols=100)
        except Exception as e:
            logger.error(f"{e}\n{traceback.format_exc()}")
            time.sleep(10)
            return self.add_worksheet(title, rows=1, cols=1)


if __name__ == '__main__':
    sh = CustomGoogleTable()
    worksheet = CustomWorksheet()
    worksheet.set_worksheet(sh.get_worksheet_by_title("test"))
    worksheet.add_base_columns()
    worksheet.update_worksheet()

