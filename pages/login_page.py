from .base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.phone_input = page.get_by_placeholder("(987) 654 32")
        self.login_button = page.get_by_role("button", name="Войти или Зарегистрироваться")
        self.password_input = page.get_by_role("textbox")
        self.submit_button = page.get_by_role("button", name="Войти")
        self.home_element = page.locator('//*[@id="HOME"]/span')

    def login(self, phone: str, password: str):
        try:
            self.phone_input.click()
            self.phone_input.fill(phone)
            self.login_button.click()
            self.password_input.click()
            self.password_input.fill(password)
            self.submit_button.click()
            self.page.wait_for_timeout(3000)
            
            return self.is_logged_in()
            
        except Exception as e:
            return False

    def is_logged_in(self) -> bool:
        try:
            return self.home_element.is_visible(timeout=10000)
        except Exception as e:
            return False