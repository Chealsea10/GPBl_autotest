import pytest
import testit
from pages.crm_page import CrmPage
from utils.env import CRM_URL, CRM_LOGIN, CRM_PASSWORD

@pytest.mark.order(2)
@pytest.mark.crm
@testit.nameSpace("WEB Регресс ЛКК.Автотесты")
@testit.className("Очистка корзины через CRM")
@testit.workItemIds(5334)  # Сюда добавим ID тест-кейса ручного после его создания в TestIT
@testit.displayName('Очистка корзины через CRM')
@testit.externalId('gpb_delete_application')
@pytest.mark.flaky(reruns=3)
def test_delete_application(page, application_number):
    """
    Тест удаления заявки в CRM
    """
    number = application_number.get()
    print(f"Получен сохраненный номер заявки: {number}")
    
    crm_page = CrmPage(page)
    with testit.step("Открытие страницы авторизации"):
        page.goto(CRM_URL)
    with testit.step("Ввод логина и пароля"):    
        crm_page.login_to_crm(CRM_LOGIN, CRM_PASSWORD)
    with testit.step("Переход на страницу заявки и очистка корзины"):    
        crm_page.delete_application(str(number))
    with testit.step("Сохранение изменений"):    
        crm_page.verify_deletion()