# файл: fetch_one.py
import sys
import json
from playwright.sync_api import sync_playwright

def fetch_cookie_online(cookie_name: str):
    url = f"https://www.cookie.is/{cookie_name}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Создаем контекст с User-Agent, чтобы не выглядеть как бот
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()
        
        try:
            response = page.goto(url, timeout=10000)
            
            # Проверка на 404 или редирект
            if response.status == 404 or page.url == "https://www.cookie.is/":
                return None

            try:
                page.wait_for_selector("text=Category", timeout=5000)
            except:
                return None

            # Логика поиска (соседи)
            category = "Unclassified"
            cat_loc = page.locator("p:text-is('Category') + div p").first
            if cat_loc.count() > 0:
                category = cat_loc.inner_text()

            provider = "Unknown"
            vend_loc = page.locator("p:text-is('Vendor') + div a").first
            if vend_loc.count() == 0:
                vend_loc = page.locator("p:text-is('Service') + div a").first
            if vend_loc.count() > 0:
                provider = vend_loc.inner_text()

            description = ""
            desc_loc = page.locator("p:text-is('Description') + div p").first
            if desc_loc.count() > 0:
                description = desc_loc.inner_text()

            return {
                "category": category.strip(),
                "provider": provider.strip(),
                "description": description.strip()
            }
        except Exception:
            return None
        finally:
            browser.close()

if __name__ == "__main__":
    # Получаем имя куки из аргументов командной строки
    if len(sys.argv) > 1:
        c_name = sys.argv[1]
        result = fetch_cookie_online(c_name)
        # Выводим результат в JSON, чтобы app.py мог его прочитать
        print(json.dumps(result))
    else:
        print("null")