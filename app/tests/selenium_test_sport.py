from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


# Test dla strony głównej z podglądem sekcji Sport.

def test_sport_main_page():
    url = "http://news.tobiasz.xyz"
    driver.get(url)
    
    # Przejście do sekcji sportowej w iframe
    sport_frame = driver.find_element(By.CLASS_NAME, "iframe-sport")
    driver.switch_to.frame(sport_frame)
    
    # Sprawdzenie elementów karuzeli
    carousel_items = driver.find_elements(By.CLASS_NAME, "carousel-item")
    assert len(carousel_items) > 0, "Nie znaleziono elementów karuzeli na stronie głównej w sekcji Sport!"
    print(f"Znaleziono {len(carousel_items)} elementów karuzeli na stronie głównej w sekcji Sport")

    # Wyjście z iframe
    driver.switch_to.default_content()


# Test dla strony głównej sekcji Sport.

def test_sport_home():
    url = "http://news.tobiasz.xyz/sport"
    driver.get(url)
    
    # Sprawdzenie tabeli artykułów sportowych
    articles = driver.find_elements(By.CSS_SELECTOR, "table tr")
    assert len(articles) > 1, "Brak artykułów na stronie głównej sekcji Sport!"
    print(f"Znaleziono {len(articles)} artykułów na stronie głównej sekcji Sport")
    
    # Przejście na kolejną stronę
    next_page = driver.find_element(By.XPATH, "//a[contains(text(), 'Następna')]")
    driver.execute_script("arguments[0].scrollIntoView();", next_page)
    time.sleep(3)
    next_page.click()
    time.sleep(3)
    
    # Sprawdzenie, czy artykuły na kolejnej stronie są inne
    new_articles = driver.find_elements(By.CSS_SELECTOR, "table tr")
    assert len(new_articles) > 1, "Nie znaleziono artykułów na następnej stronie!"
    print(f"Znaleziono {len(new_articles)} artykułów na następnej stronie")



# Test dla podstrony Sport Preview.

def test_sport_preview():
    url = "http://news.tobiasz.xyz/sport/sport_preview"
    driver.get(url)
    
    # Sprawdzenie elementów karuzeli
    carousel_items = driver.find_elements(By.CLASS_NAME, "carousel-item")
    assert len(carousel_items) > 0, "Nie znaleziono elementów karuzeli na podstronie Sport Preview!"
    print(f"Znaleziono {len(carousel_items)} elementów karuzeli na podstronie Sport Preview")
    
    # Sprawdzenie działania karuzeli
    initial_caption = driver.find_element(By.CLASS_NAME, "carousel-caption").text
    
    next_button = driver.find_element(By.CLASS_NAME, "carousel-control-next")
    next_button.click()
    time.sleep(3)
    
    next_caption = driver.find_element(By.CLASS_NAME, "carousel-caption").text
    assert next_caption != initial_caption, "Karuzela nie przesunęła się po kliknięciu strzałki w prawo!"
    
    prev_button = driver.find_element(By.CLASS_NAME, "carousel-control-prev")
    prev_button.click()
    time.sleep(3)
    
    prev_caption = driver.find_element(By.CLASS_NAME, "carousel-caption").text
    assert prev_caption == initial_caption, "Karuzela nie wróciła do poprzedniego slajdu!"

    driver.quit()


