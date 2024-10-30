from .base_page import BasePage
from playwright.sync_api import expect
import re

class ApplicationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.contractor_card = page.locator(".SelectContractor-module__contractor-card__icon--g8dWF").first
        self.continue_button = page.get_by_role("button", name="Продолжить")
        self.upload_inputs = page.get_by_label("Upload")
        self.sign_button = page.get_by_role("button", name="Подписать")
        self.success_message = 'text="Мой заказ"'
        self.application_number_text = page.locator("text=/Заявка № \d+/").first

    def get_application_number(self) -> str:
        """Получает номер заявки"""
        expect(self.application_number_text).to_be_visible(timeout=10000)
        text = self.application_number_text.inner_text()
        return re.search(r'№\s*(\d+)', text).group(1)

    def select_contractor(self):
        self.contractor_card.click()
        self.continue_button.click()
        self.continue_button.click()

    def upload_documents(self, pdf_files: list):
        self.upload_inputs.first.set_input_files(pdf_files[0])
        self.upload_inputs.nth(1).set_input_files(pdf_files[1])
        self.continue_button.click()

    def submit_application(self):
        self.sign_button.click()
        self.continue_button.click()

    def verify_submission(self):
        self.page.wait_for_selector(self.success_message, timeout=10000)
        expect(self.page.locator("#root")).to_contain_text("Мой заказ")