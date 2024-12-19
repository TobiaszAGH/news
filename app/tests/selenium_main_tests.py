from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from app import app
import threading

@pytest.fixture(scope="module")
def driver():
    def run_app():
        app.run(debug=False, use_reloader=False, port=8000)

    thread = threading.Thread(target=run_app)
    thread.daemon = True
    thread.start()

    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_home_page_title(driver):
    driver.get("http://127.0.0.1:8000/") 
    assert driver.title == "Strona Główna"

def test_home_page_theme(driver):
    toggler_value = driver.page_source.split('<head')[0].split('"')[-2]
    toggler = driver.find_element(By.XPATH, "//span[@id='theme-toggler']")
    toggler.click()
    if toggler_value == "light":
        assert 'data-bs-theme="dark"' in driver.page_source    
    elif toggler_value == "dark":
        assert 'data-bs-theme="light"' in driver.page_source    