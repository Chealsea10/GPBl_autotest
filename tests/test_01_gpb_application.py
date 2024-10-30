import pytest
import testit
from pages.login_page import LoginPage
from pages.marketplace_page import MarketplacePage
from pages.application_page import ApplicationPage
from utils.file_handler import FileHandler
from utils.env import TEST_URL, TEST_PHONE, TEST_PASSWORD

@pytest.mark.order(1)
@pytest.mark.gpb
@testit.nameSpace("WEB Регресс ЛКК.Автотесты")
@testit.className("Создание заявки на лизинг")
@testit.workItemIds(5297)  # Сюда добавим ID тест-кейса после его создания в TestIT
@testit.displayName('Создание заявки на лизинг')
@testit.externalId('gpb_create_application')
def test_gpb_application(page, application_number):
    """
    Тест оформления заявки на сайте GPB 
    """
    login_page = LoginPage(page)
    marketplace_page = MarketplacePage(page)
    application_page = ApplicationPage(page)
    
    pdf_files = FileHandler.get_docs_files()
    with testit.step("Открытие страницы авторизации"):
        login_page.navigate_to(TEST_URL)
    with testit.step("Авторизация"):    
        login_page.login(TEST_PHONE, TEST_PASSWORD)
    with testit.step("Переход на страницу лизингмаркета"):
        marketplace_page.go_to_marketplace()
    with testit.step("Добавление авто в корзину"):    
        marketplace_page.add_to_application()
    with testit.step("Сохранение номер заявки"):
        number = application_page.get_application_number()
    print(f"Получен номер заявки: {number}")
    application_number.set(number)
    with testit.step("Выбор компании"):
        application_page.select_contractor()
    with testit.step("Загрузка документов"):    
        application_page.upload_documents(pdf_files)
    with testit.step("Подпись и проверка данных"):    
        application_page.submit_application()
    with testit.step("Сообщение о успешном составлении заявки"):    
        application_page.verify_submission()