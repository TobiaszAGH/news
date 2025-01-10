import logging
import inspect
import pytest
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

url_2 = "http://news.tobiasz.xyz/weather"


def log_function_name():
    """Loguje nazwę funkcji w czasie jej wykonywania."""
    frame = inspect.currentframe().f_back
    function_name = frame.f_code.co_name
    logging.info(f"Executing function: {function_name}")


@pytest.fixture(scope="module")
def driver():
    """Uruchamia przeglądarkę przed testami i zamyka po zakończeniu."""
    print("Uruchamianie przeglądarki Chrome...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Maksymalizuj okno przeglądarki
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()


def test_weather_page(driver):
    """
    Test weryfikujący działanie podstrony /weather
    """
    log_function_name()


    # Krok 2: Przejdź na podstronę /weather
    driver.get(url_2)
    logging.info(f"Step 2: Załadowano podstronę {driver.title}.")
    assert driver.title == "Weather", f"Expected title 'Weather', but got {driver.title}"

    # Krok 3: Wypełnij formularz
    try:
        logging.info("Step 3: Wypełnianie formularza...")
        input_name1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "city1"))
        )
        input_name1.clear()
        input_name1.send_keys("Kraków")

        input_name3 = driver.find_element(By.NAME, "city3")
        input_name3.clear()
        input_name3.send_keys("dhshdkajhdjkas")

        input_name4 = driver.find_element(By.NAME, "city4")
        input_name4.clear()
        input_name4.send_keys("Szczecin")
        logging.info("Formularz wypełniony.")
    except Exception as e:
        logging.error(f"Błąd podczas wypełniania formularza: {e}")
        pytest.fail(f"Nie udało się wypełnić formularza: {e}")

    # Krok 4: Kliknij przycisk "submit"
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))
        )
        submit_button.click()
        logging.info("Step 4: Kliknięto przycisk 'submit'.")
    except Exception as e:
        logging.error(f"Błąd podczas klikania przycisku 'submit': {e}")
        pytest.fail(f"Nie udało się kliknąć przycisku 'submit': {e}")

    # Krok 5: Zweryfikuj wynik
    time.sleep(3)  # Czekanie na ewentualny wynik
    current_url = driver.current_url
    logging.info(f"Step 5: Po kliknięciu przekierowano na URL: {current_url}")
    assert "/weather" in current_url, "Nie przekierowano prawidłowo po wysłaniu formularza."


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    pytest.main(["-v", __file__])