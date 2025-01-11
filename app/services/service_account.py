import gspread


def initialize_gspread(service_account_credentials: dict) -> gspread.client.Client:
    scopes = [
        'https://spreadsheets.google.com/feeds'
    ]
    return gspread.service_account_from_dict(service_account_credentials, scopes=scopes)
