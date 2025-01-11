from aenum import Enum, extend_enum


class ValueName(Enum):
    api_name = "api_name"
    main_name = "main_name"
    ru_name = "ru_name"


class AnalyticalDataFields(Enum):
    revenue = {
        ValueName.api_name: "revenue",
        ValueName.main_name: "revenue",
        ValueName.ru_name: "заказано на сумму"
    }
    ordered_units = {
        ValueName.api_name: "ordered_units",
        ValueName.main_name: "ordered_units",
        ValueName.ru_name: "заказано товаров"
    }
    hits_tocart = {
        ValueName.api_name: "hits_tocart",
        ValueName.main_name: "hits_tocart",
        ValueName.ru_name: "всего добавлено в корзину"
    }
    cancellations = {
        ValueName.api_name: "cancellations",
        ValueName.main_name: "cancellations",
        ValueName.ru_name: "отменено товаров"
    }
    delivered_units = {
        ValueName.api_name: "delivered_units",
        ValueName.main_name: "delivered_units",
        ValueName.ru_name: "доставлено товаров"
    }
    returns = {
        ValueName.api_name: "returns",
        ValueName.main_name: "returns",
        ValueName.ru_name: "возвращено товаров"
    }
    session_view = {
        ValueName.api_name: "session_view",
        ValueName.main_name: "session_view",
        ValueName.ru_name: "всего сессий"
    }
    hits_tocart_search = {
        ValueName.api_name: "hits_tocart_search",
        ValueName.main_name: "hits_tocart_search",
        ValueName.ru_name: "в корзину из поиска или категории"
    }
    hits_tocart_pdp = {
        ValueName.api_name: "hits_tocart_pdp",
        ValueName.main_name: "hits_tocart_pdp",
        ValueName.ru_name: "в корзину из карточки товара"
    }
    hits_view = {
        ValueName.api_name: "hits_view",
        ValueName.main_name: "hits_view",
        ValueName.ru_name: "всего показов"
    }
    hits_view_search = {
        ValueName.api_name: "hits_view_search",
        ValueName.main_name: "hits_view_search",
        ValueName.ru_name: "показы в поиске и в категории"
    }
    hits_view_pdp = {
        ValueName.api_name: "hits_view_pdp",
        ValueName.main_name: "hits_view_pdp",
        ValueName.ru_name: "показы на карточке товара"
    }
    position_category = {
        ValueName.api_name: "position_category",
        ValueName.main_name: "position_category",
        ValueName.ru_name: "позиция в поиске и категории"
    }
    session_view_search = {
        ValueName.api_name: "session_view_search",
        ValueName.main_name: "session_view_search",
        ValueName.ru_name: "сессии с показом в поиске или в каталоге"
    }


class PvpFields(Enum):
    money_spent = {
        ValueName.api_name: "money_spent",
        ValueName.main_name: "pvp_money_spent",
        ValueName.ru_name: "расход, ₽"
    }


class TrfFields(Enum):
    views = {
        ValueName.api_name: "views",
        ValueName.main_name: "trf_views",
        ValueName.ru_name: "показы"
    }
    clicks = {
        ValueName.api_name: "clicks",
        ValueName.main_name: "trf_clicks",
        ValueName.ru_name: "клики"
    }
    ctr = {
        ValueName.api_name: "ctr",
        ValueName.main_name: "trf_ctr",
        ValueName.ru_name: "ctr (%)"
    }
    money_spent = {
        ValueName.api_name: "money_spent",
        ValueName.main_name: "trf_money_spent",
        ValueName.ru_name: "расход"
    }
    price = {
        ValueName.api_name: "price",
        ValueName.main_name: "trf_price",
        ValueName.ru_name: "цена товара, ₽"
    }
    avg_bid = {
        ValueName.api_name: "avg_bid",
        ValueName.main_name: "trf_avg_bid",
        ValueName.ru_name: "ср. цена клика, ₽"
    }


class ProductFields(Enum):
    drr = {
        ValueName.api_name: "drr",
        ValueName.main_name: "drr",
        ValueName.ru_name: "дрр"
    }
    conversion = {
        ValueName.api_name: "conversion",
        ValueName.main_name: "conversion",
        ValueName.ru_name: "конверсия"
    }


AnalyticalDataFields: Enum
PvpFields: Enum
TrfFields: Enum
ProductFields: Enum

for field in AnalyticalDataFields:
    extend_enum(ProductFields, field.value[ValueName.main_name], field.value)

for field in PvpFields:
    extend_enum(ProductFields, field.value[ValueName.main_name], field.value)

for field in TrfFields:
    extend_enum(ProductFields, field.value[ValueName.main_name], field.value)

