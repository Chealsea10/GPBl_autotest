import pytest
import json
from pathlib import Path
from playwright.sync_api import Playwright

def pytest_configure(config):
    """Регистрируем кастомные маркеры"""
    config.addinivalue_line(
        "markers", "gpb: mark test as gpb test"
    )
    config.addinivalue_line(
        "markers", "crm: mark test as crm test"
    )

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": True  # всегда False
    }

@pytest.fixture(scope="function")
def browser_context_args(browser_context_args, pytestconfig):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }

class ApplicationNumberManager:
    def __init__(self):
        self.file_path = Path("test_data/application_number.json")
        self.file_path.parent.mkdir(exist_ok=True)
        
    def get(self):
        if not self.file_path.exists():
            pytest.fail("Номер заявки не был установлен. Возможно, тест создания заявки не был выполнен или завершился с ошибкой.")
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            return data.get('number')

    def set(self, value):
        if not value:
            pytest.fail("Попытка установить пустой номер заявки")
        with open(self.file_path, 'w') as f:
            json.dump({'number': value}, f)
            print(f"Сохранен номер заявки: {value}")

@pytest.fixture(scope="session")
def application_number():
    """Фикстура для хранения номера заявки между тестами"""
    return ApplicationNumberManager()