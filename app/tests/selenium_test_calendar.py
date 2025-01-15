from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

options = webdriver.ChromeOptions()

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url_1 = "http://news.tobiasz.xyz/calendar/calendar_preview"
driver.get(url_1)

def test_calendar():
    initial_date = driver.find_element(By.CLASS_NAME, "day").text
    print(f"Initial date: {initial_date}")
    right_arrow = driver.find_element(By.CLASS_NAME, "next_day").find_element(By.TAG_NAME, "button")
    right_arrow.click()
    time.sleep(2)
    new_date = driver.find_element(By.CLASS_NAME, "day").text
    print(f"New date: {new_date}")
    assert new_date != initial_date, "Data nie zmieniła się po kliknięciu w strzałkę w prawo!"
    left_arrow = driver.find_element(By.CLASS_NAME, "previous_day").find_element(By.TAG_NAME, "button")
    left_arrow.click()
    time.sleep(2)

    final_date = driver.find_element(By.CLASS_NAME, "day").text
    print(f"Final date: {final_date}")
    assert final_date == initial_date, "Data nie wróciła do poprzedniego stanu po kliknięciu w strzałkę w lewo!"
    driver.quit()