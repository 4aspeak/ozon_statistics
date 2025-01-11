import logging
import os
from pathlib import Path

from app.config import get_config
from app.services.service_account import initialize_gspread

config = get_config()


BASE_DIR = Path(__file__).resolve().parent


SERVICE_ACCOUNT_CREDENTIALS = {
    "type": config.google.service_account_type,
    "project_id": config.google.service_account_project_id,
    "private_key_id": config.google.service_account_private_key_id,
    "private_key": config.google.service_account_private_key,
    "client_email": config.google.service_account_client_email,
    "client_id": config.google.service_account_client_id,
    "auth_uri": config.google.service_account_auth_uri,
    "token_uri": config.google.service_account_token_uri,
    "auth_provider_x509_cert_url": config.google.service_account_auth_provider_x509_cert_url,
    "client_x509_cert_url": config.google.service_account_client_x509_cert_url,
    "universe_domain": config.google.service_account_universe_domain
}

TABLE_ID_OF_OZON_STATISTICS = config.google.google_sheets_table_id
GSPREAD_CLIENT = initialize_gspread(SERVICE_ACCOUNT_CREDENTIALS)

OZON_SELLER_CLIENT_ID = config.ozon.ozon_seller_client_id
OZON_SELLER_API_KEY = config.ozon.ozon_seller_api_key

OZON_PERFORMANCE_CLIENT_ID = config.ozon.ozon_performance_client_id
OZON_PERFORMANCE_CLIENT_SECRET = config.ozon.ozon_performance_client_secret


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, "app.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
