from dotenv import load_dotenv
import os

load_dotenv()  # загружаем переменные из .env файла

TEST_URL = os.getenv('TEST_URL')
TEST_PHONE = os.getenv('TEST_PHONE')
TEST_PASSWORD = os.getenv('TEST_PASSWORD')
CRM_URL = "https://preprodmy.autogpbl.ru/bitrix/admin/#authorize"
CRM_LOGIN = "OsipovAVl"
CRM_PASSWORD = "Spduf5gy!"