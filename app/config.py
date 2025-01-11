import os

import environ


@environ.config(prefix="")
class AppConfig:

    @environ.config()
    class Python:
        debug = environ.bool_var(
            default=True,
            help="Debug mode",
        )

    @environ.config()
    class Google:
        google_sheets_table_id = environ.var(
            default="1Zl_EcJOWvV_K6ZT37htTArIIZTqwMsXb4kva10IFPlk",
            help="Google Sheets table id",
        )
        service_account_type = environ.var(
            default="service_account",
        )
        service_account_project_id = environ.var(
            default="ozon-statistics-440308"
        )
        service_account_private_key_id = environ.var(
            default="040b88f27b6264fc26f010d5f4861da209f310ad"
        )
        service_account_private_key = environ.var(
            default="-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC2yuUkdtJZeeOf\n0A9HnXE/QNpQ0mJQxJcVXt3dqedAyctKWGWjd1o/dTn2Oit24NrolVifEB8QpAxF\nBOCE+UjhPMcPUz8PhWtBbSieoISwSYCeD1q9CcdGxO4FGA9SMnOq1GYQ3wiRRFHG\nojrPJjaeKQYEdwW1qlg2fxMIbRvRsVLMrPrFCsXdsbQx+G0i73gVdvmHakOJzBwI\nfApS3zDCn8KA+1mJEvad9pHyyvDOFhZkAVNQj8aY4WH49MML/C9bqKXVYNb0NLjp\n30xdWcDyRr+stgOxMoBQrizJ+MtcLO70vyCYDN5SolFlDumfi/H8qZ4iEVmrN/y8\nAnbcHkixAgMBAAECggEAJCEXSG1J51CNuqU7l+qZGyj83bOvpgotWJZ/INR3tlkM\nWt38/OHWzysi8TWPKLiJ3CXEte/QTBA4sp2jqPTCwG4sZC2OjclPqUdjm3LbtyJY\nDyW2yB16K1U6PHyEbrk1HoNLxzLmNRw9U5b2K8KAUiOGonRKBx2rwN2+C9DRClF8\n/a98NUlGNCSEHP4pxpXJrvZ3QvNy8yMfY06h2QJBeL8lRaNMktUTIEPqfLR8idB0\niCJISIpunN4obX2hinKBShC9Q5k/Yhbp9wfo4MNkDQZCEbOpfVCWGndJqEVA6Klx\nglYoZ5W8Mki7yBHauxMcN5wQ0Y63Ug1AzhH3d6NaKQKBgQD/P9IKSVsA8LhSxrfi\nDCUF7iFNoF4RK06KPk3RU0IfBpnOInMst726SLR+B2USg3Ckv8OkxdoeLSXolLkw\n89uDCHbPH56oLQTPrliIJVB+UvBKCCf2O4hRnQWteT7FSdfrzo4jDUlE80onAMCo\nbgr0IyL7ZrIuWTWpfdjyf2GeDQKBgQC3VIVyXr55HdBlm8jacUO5420RAv0FTsmR\nTpUWA+Pj7wT0x1f1hKtakE8i26MwJ2Oi3AuiNpWKPJ8yh0LuiLx9ZXcKzvdL0Cnf\nVRUcfKXiu+ivIleAv16PmUbYjdNiz6eWry9nk1uzEF9ybAU7/LrcnSd89l+dxb/n\nkU9DfPbQNQKBgQD5591YjuuXpxeAi+kbW3KgNL7MhteyjakO9uMvsAmL4OWTie0j\n+h27FlYJEmplzuTpmIsPd1sPsnpsFbifchIYX6AbOEUZOUJ9p6AsZAREOiXjBctC\nbJUR+t/FMXFArgTGbeyB6w8yf9S5DSaTgXIeB4zHgYuwj01Xzcwr2IWVvQKBgAFt\n8EhvAq8xE1HngA5r+ao2YsBSNKTY82tloHX2e81oLLK35zCr4yYmn+dWrRQQCo/X\nhWOzZ0EXreoX8eaoPEgCBYaZDIaTze/G2w5IzoZRDsRm0SXY2CTofgvsNyy7D8R2\nAzmchYeE5imfO/82vkJAG3G2/hHd29wzXtnY3JfNAoGBANPhhPDRxtDSRGI5BBQv\nxdg+tWKFgX1mz6p1FrQgxCsICEUqeDcM3ko9/+HupgX+3drKe1g48fcVKMf/ez/q\nTSEtLofjltaGcLKdN2OsBYx9HkNHrDByQ5iQCCdDZoIx9cHq0M4A+qqQr6lOqzxv\ngyFSDO7VcsY4929U8sz5u15S\n-----END PRIVATE KEY-----\n"
        )
        service_account_client_email = environ.var(
            default="acc-829@ozon-statistics-440308.iam.gserviceaccount.com"
        )
        service_account_client_id = environ.var(
            default="106220609935467546343"
        )
        service_account_auth_uri = environ.var(
            default="https://accounts.google.com/o/oauth2/auth"
        )
        service_account_token_uri = environ.var(
            default="https://oauth2.googleapis.com/token"
        )
        service_account_auth_provider_x509_cert_url = environ.var(
            default="https://www.googleapis.com/oauth2/v1/certs"
        )
        service_account_client_x509_cert_url = environ.var(
            default="https://www.googleapis.com/robot/v1/metadata/x509/acc-829%40ozon-statistics-440308.iam.gserviceaccount.com"
        )
        service_account_universe_domain = environ.var(
            default="googleapis.com"
        )

    @environ.config()
    class Ozon:
        ozon_seller_client_id = environ.var(
            default="2304748", help="Ozon seller client id"
        )
        ozon_seller_api_key = environ.var(
            default="2172881f-517c-4a8e-abf4-f2f1a15a515c",
            help="Ozon seller api key",
        )
        ozon_performance_client_id = environ.var(
            default="43494887-1730058110799@advertising.performance.ozon.ru",
            help="Ozon performance client id"
        )
        ozon_performance_client_secret = environ.var(
            default="n5ffMDl_9pPCTd_IBi5TePBdwsW_WjR-hWvNzBzQKcRLc5tCVxBCwTCNakXa6QQbBfdpTbr6Rx3lFnF8LA",
            help="Ozon performance client secret"
        )

    python = environ.group(Python)
    google = environ.group(Google)
    ozon = environ.group(Ozon)


def get_config() -> AppConfig:
    return AppConfig.from_environ(os.environ)
