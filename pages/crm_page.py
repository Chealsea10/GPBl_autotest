from .base_page import BasePage
from playwright.sync_api import expect


class CrmPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.login_input = page.get_by_role("row", name="preprodmy.autogpbl.ru RU 1").locator("input[name=\"USER_LOGIN\"]")
        self.password_input = page.get_by_role("row", name="preprodmy.autogpbl.ru RU 1").locator("input[name=\"USER_PASSWORD\"]")
        self.submit_button = page.get_by_role("button", name="Submit")
        self.basket_toggle = page.get_by_role("row", name="Корзина: да", exact=True).locator("label").nth(1)
        self.viewed_toggle = page.get_by_role("row", name="UF_VIEWED: да", exact=True).locator("label").nth(1)
        self.apply_button = page.get_by_role("button", name="Применить")
        self.save_button = page.get_by_role("button", name="Сохранить")
        self.title = page.locator("#adm-title")

    def login_to_crm(self, login: str, password: str):
        """Вход в CRM"""
        self.page.wait_for_timeout(3000)
        self.login_input.wait_for(state="visible")
        self.login_input.fill(login)
        self.login_input.press("Tab")
        self.password_input.wait_for(state="visible")
        self.password_input.fill(password)
        self.submit_button.click()

    def delete_application(self, number: str):
        """Удаление заявки по номеру"""
        url = f"https://preprodmy.autogpbl.ru/bitrix/admin/highloadblock_row_edit.php?ENTITY_ID=6&ID={number}&lang=ru"
        print(f"Переход по URL: {url}")
        self.page.goto(url)
    
    # Прокручиваем страницу до чекбоксов
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    
    # Находим сами чекбоксы (input type="checkbox")
        
        basket_checkbox = self.page.locator("input[id='UF_BASKET']")
        viewed_checkbox = self.page.locator("input[id='UF_VIEWED']")
        
    # Проверяем состояние и снимаем галочки если они установлены
        if basket_checkbox.is_checked():
            basket_checkbox.uncheck()
            print("Снята галочка с чекбокса корзины")
        
        if viewed_checkbox.is_checked():
            viewed_checkbox.uncheck()
            print("Снята галочка с чекбокса просмотра")
    
        self.apply_button.click()
        self.save_button.click()

    def verify_deletion(self):
        """Проверка успешного удаления заявки"""
        expect(self.title).to_contain_text("Список записей")
        # Можно добавить дополнительные проверки, если нужно
        print("Удаление заявки подтверждено")    