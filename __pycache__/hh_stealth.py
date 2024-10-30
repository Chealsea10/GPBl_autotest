from playwright.async_api import async_playwright
import asyncio
import random
import traceback

async def random_mouse_movement(page, element):
    """Имитация естественного движения мыши"""
    box = await element.bounding_box()
    if not box:
        return

    target_x = box['x'] + box['width'] / 2
    target_y = box['y'] + box['height'] / 2

    steps = random.randint(3, 5)
    for i in range(steps):
        x = target_x + random.uniform(-10, 10)
        y = target_y + random.uniform(-10, 10)
        await page.mouse.move(x, y)
        await asyncio.sleep(random.uniform(0.01, 0.03))

async def click_respond_buttons(page):
    """Функция для обработки кнопок 'Откликнуться' на странице"""
    try:
        # Ждем загрузки страницы
        await page.wait_for_load_state('load')
        await asyncio.sleep(2)

        # Получаем все кнопки "Откликнуться" на странице
        buttons = await page.get_by_role("button", name="Откликнуться").all()
        print(f"Найдено {len(buttons)} кнопок 'Откликнуться' на странице")

        index = 0
        while index < len(buttons):
            try:
                button = buttons[index]

                # Проверяем, находимся ли мы на странице с вакансиями
                if page.url.startswith('https://tula.hh.ru/search/vacancy?text=qa'):
                    await button.scroll_into_view_if_needed()
                    await random_mouse_movement(page, button)

                    # Сохраняем текущий URL
                    current_url = page.url

                    # Кликаем по кнопке
                    await button.click()
                    await asyncio.sleep(random.uniform(2, 3))

                    # Ждем загрузки страницы после возможной навигации
                    await page.wait_for_load_state('load')

                    # Проверяем, изменился ли URL
                    if page.url != current_url:
                        print("Произошел переход на страницу работодателя, возвращаемся назад")
                        await page.go_back()
                        await page.wait_for_load_state('load')
                        await asyncio.sleep(random.uniform(2, 3))

                        # После возврата обновляем список кнопок
                        buttons = await page.get_by_role("button", name="Откликнуться").all()
                        if index >= len(buttons):
                            break  # Выходим из цикла, если индекс больше количества кнопок
                        continue

                    # Закрываем модальное окно, если оно есть
                    close_button = page.locator('[data-qa="vacancy-response-modal-close"]')
                    if await close_button.is_visible():
                        await close_button.click()
                        await asyncio.sleep(random.uniform(1, 2))

                else:
                    # Если мы не на странице с вакансиями, возвращаемся назад
                    print("Не на странице с вакансиями, возвращаемся назад")
                    await page.go_back()
                    await page.wait_for_load_state('load')
                    await asyncio.sleep(random.uniform(2, 3))
                    continue

                # Переходим к следующей кнопке
                index += 1

            except Exception as e:
                print(f"Ошибка при обработке кнопки {index + 1}: {e}")
                traceback.print_exc()
                # Переходим к следующей кнопке в случае ошибки
                index += 1
                continue

    except Exception as e:
        print(f"Ошибка в функции click_respond_buttons: {e}")
        traceback.print_exc()



async def process_all_pages(page):
    """Функция для обработки всех страниц с вакансиями"""
    page_number = 1
    while True:
        try:
            print(f"Обработка страницы {page_number}")

            # Ждем загрузки страницы
            await page.wait_for_load_state('load')
            await asyncio.sleep(random.uniform(2, 3))

            # Обрабатываем все вакансии на текущей странице
            await click_respond_buttons(page)

            # Проверяем наличие кнопки "Следующая страница"
            next_button = page.locator('[data-qa="pager-next"]')
            if await next_button.is_visible():
                await random_mouse_movement(page, next_button)
                await next_button.click()
                await asyncio.sleep(random.uniform(2, 3))
                page_number += 1
            else:
                print("Достигнут конец списка страниц")
                break

        except Exception as e:
            print(f"Ошибка при обработке страницы {page_number}: {e}")
            traceback.print_exc()
            await page.screenshot(path=f'error_page_{page_number}.png')
            break

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins',
                '--disable-automation'
            ]
        )

        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            locale='ru-RU',
            timezone_id='Europe/Moscow'
        )

        page = await context.new_page()

        try:
            # Переход на сайт и ожидание загрузки
            await page.goto('https://hh.ru/', timeout=60000)
            await page.wait_for_selector('text=Войти', state='visible', timeout=60000)
            await asyncio.sleep(random.uniform(1, 2))

            # Клик по кнопке "Войти"
            login_button = page.get_by_role("link", name="Войти")
            await random_mouse_movement(page, login_button)
            await login_button.click()
            await asyncio.sleep(2)  # Ждем загрузку формы

            # Ввод email
            await page.wait_for_selector('[data-qa="account-signup-email"]', state='visible', timeout=60000)
            await asyncio.sleep(1)
            email_element = page.locator('[data-qa="account-signup-email"]')
            await email_element.click()
            await email_element.fill("qwe32.2011@mail.ru")
            await asyncio.sleep(random.uniform(1, 1.5))

            # Переход к вводу пароля
            password_link = page.locator("a").filter(has_text="Войти с паролем")
            await random_mouse_movement(page, password_link)
            await password_link.click()
            await asyncio.sleep(random.uniform(1, 1.5))

            # Ввод пароля
            await page.wait_for_selector('[data-qa="login-input-password"]', state='visible', timeout=60000)
            password_element = page.locator('[data-qa="login-input-password"]')
            await password_element.click()
            await password_element.fill("Spduf5gy")
            await asyncio.sleep(random.uniform(1, 1.5))

            # Клик по кнопке входа
            submit_button = page.get_by_role("button", name="Войти в личный кабинет")
            await random_mouse_movement(page, submit_button)
            await submit_button.click()
            await asyncio.sleep(random.uniform(2, 3))


            # Поиск вакансий
            search_input = page.get_by_label("Профессия, должность или компания")
            await random_mouse_movement(page, search_input)
            await search_input.click()
            await search_input.fill("qa")
            await asyncio.sleep(random.uniform(1, 1.5))

            search_button = page.get_by_role("button", name="Найти")
            await random_mouse_movement(page, search_button)
            await search_button.click()
            await asyncio.sleep(random.uniform(2, 3))

            # Обработка всех страниц с вакансиями
            await process_all_pages(page)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            traceback.print_exc()
            await page.screenshot(path='error_main.png')
        finally:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
