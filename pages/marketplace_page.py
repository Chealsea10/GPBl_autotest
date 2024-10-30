from .base_page import BasePage

class MarketplacePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def go_to_marketplace(self):
        self.page.get_by_role("link", name="Лизингмаркет").click()
        self.page.get_by_role("link", name="Подробнее").first.click()

    def add_to_application(self):
        self.page.get_by_role("button", name="Добавить в заявку").click()
        self.page.get_by_role("button", name="Оформить заявку").click()
    
    