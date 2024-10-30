import pytest
import testit
from pages.login_page import LoginPage
from utils.env import TEST_URL, TEST_PHONE, TEST_PASSWORD

@pytest.mark.auth  # маркер для группировки тестов авторизации

# Добавляем декораторы TestIT:
@testit.nameSpace("WEB Регресс ЛКК.Автотесты")
@testit.className("Авторизация")
@testit.workItemIds(5296)  # Сюда добавим ID тест-кейса после его создания в TestIT
@testit.displayName('Проверка успешной авторизации')
@testit.externalId('gpb_successful_login')
def test_successful_login(page):
    """
    Тест успешной авторизации на сайте
    """
    # Инициализация страницы логина
    login_page = LoginPage(page)

    with testit.step("Открытие страницы авторизации"):
        login_page.navigate_to(TEST_URL)
    
    with testit.step("Ввод учетных данных и успешный вход"):
        assert login_page.login(TEST_PHONE, TEST_PASSWORD)  # метод login возвращает результат is_logged_in()

    